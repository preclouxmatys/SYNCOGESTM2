"""
Vicon utilities (CSV parsing + marker extraction + kinematic metrics)

This module centralizes reusable functions used across notebooks:
- read_vicon_csv: parse Vicon "Trajectories" CSV exports
- find_xyz_cols: robustly find X/Y/Z columns for a marker token
- motion_quantity_point: compute Quantity of Motion (QdM) for a 3D marker
"""

from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import Iterable, Tuple, Optional

import numpy as np
import pandas as pd


def read_vicon_csv(csv_path: Path) -> pd.DataFrame:
    """
    Parse a Vicon "Trajectories" CSV export.

    Expected layout:
    Row 1: "Trajectories"
    Row 2: sampling frequency (e.g., 100)
    Row 3: marker names (with blanks that must be forward-filled)
    Row 4: axes (Frame/Sub Frame + X/Y/Z)
    Row 5: units (e.g., mm)
    Row 6+: numeric data

    Returns
    -------
    pd.DataFrame
        DataFrame with flattened column names:
        - "Frame", "Sub Frame"
        - "<marker>_X", "<marker>_Y", "<marker>_Z"
    """
    csv_path = Path(csv_path)

    with open(csv_path, "r", encoding="utf-8", errors="replace", newline="") as f:
        reader = csv.reader(f)
        header_lines = [next(reader) for _ in range(5)]

    marker_row = header_lines[2]
    axis_row = header_lines[3]

    n = max(len(marker_row), len(axis_row))
    marker_row += [""] * (n - len(marker_row))
    axis_row += [""] * (n - len(axis_row))

    # Forward-fill marker names (Vicon leaves blanks under the same marker for Y/Z)
    filled = []
    last = ""
    for m in marker_row:
        m = (m or "").strip()
        if m == "":
            filled.append(last)
        else:
            last = m
            filled.append(last)

    # Build flat column names: "<marker>_X", "<marker>_Y", "<marker>_Z"
    colnames = []
    for m, a in zip(filled, axis_row):
        m = (m or "").strip()
        a = (a or "").strip()

        if a in ["Frame", "Sub Frame"]:
            colnames.append(a)
        elif a in ["X", "Y", "Z"]:
            colnames.append(f"{m}_{a}")
        else:
            colnames.append(m if m else a)

    df = pd.read_csv(csv_path, skiprows=5, header=None, names=colnames, engine="python")
    df = df.dropna(axis=1, how="all")  # remove empty trailing columns (e.g., from extra commas)
    return df


def find_xyz_cols(columns: Iterable[str], token: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Find the X/Y/Z column names for a given marker token.

    The Vicon export sometimes prefixes marker names with a subject label,
    e.g. "Patient 1:poignet_D_X". This function matches the token even if
    there is any prefix before ':'.

    Parameters
    ----------
    columns : iterable of str
        DataFrame columns.
    token : str
        Marker token to search (e.g., "poignet_D", "2epaule_G").

    Returns
    -------
    (X, Y, Z) : tuple[str|None, str|None, str|None]
        Column names for X/Y/Z if found, otherwise None.
    """
    pat = re.compile(rf"(?:^|:)\s*{re.escape(token)}_([XYZ])\b", re.IGNORECASE)
    found = {}

    for c in columns:
        c_str = str(c).replace(" ", "")
        m = pat.search(c_str)
        if m:
            axis = m.group(1).upper()
            # If multiple matches exist, keep the shortest name (usually the cleanest one)
            if axis not in found or len(c_str) < len(str(found[axis])):
                found[axis] = c

    return found.get("X"), found.get("Y"), found.get("Z")


def motion_quantity_point(df: pd.DataFrame, X: str, Y: str, Z: str) -> Tuple[float, int]:
    """
    Compute Quantity of Motion (QdM) for a 3D point.

    Definition
    ----------
    QdM = sum over frames of the Euclidean distance between consecutive samples.

    Parameters
    ----------
    df : pd.DataFrame
        Data containing X/Y/Z columns in millimeters.
    X, Y, Z : str
        Column names for the point.

    Returns
    -------
    qdm_mm : float
        Cumulative 3D path length in mm.
    n_steps : int
        Number of valid frame-to-frame steps used in the sum.
    """
    arr = df[[X, Y, Z]].to_numpy(dtype=float)
    d = np.diff(arr, axis=0)
    step = np.sqrt((d ** 2).sum(axis=1))
    step = step[np.isfinite(step)]
    return float(step.sum()), int(step.size)