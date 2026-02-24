# SYNCOGESTM2
Repository for the defense Python/R in M2

**Python–R–Git Project ** 
Matys Précloux — Master IEAP — 2026  

## 1. Project Overview

This project investigates the effect of **postural configuration**  
(SEATED vs SEMI-STANDING vs STANDING) on global body movement dynamics during dyadic interaction.

Movement is quantified using:

- **Vicon optical motion capture system**
- 3D marker trajectories
- Quantity of Motion (QdM)
- Shoulder-width normalization
- Repeated-measures ANOVA (Greenhouse–Geisser correction)

The objective is to demonstrate both:

- Technical skills (Python, R, Git, reproducible pipelines)
- Scientific skills (signal processing, normalization, statistics, interpretation)

---

## 2. Project Structure
SYNCOGESTM2/
│
├── data/
│   ├── test/           # Small dataset for reproducibility
│   └── raw/            # Full dataset
│
├── results/
│   ├── test/           # Generated test results
│   └── raw/            # Generated full results
│
├── notebooks/          # Python processing notebooks
│
├── src/                # Reusable Python functions
│
├── main.ipynb          # Python entry point
├── main.Rmd            # R entry point
├── R.Rproj             # RStudio project file
│
├── README.md
└── LICENSE

---

## 3. Python Pipeline

The Python workflow computes:

1. Quantity of Motion (QdM) for wrists and head
2. Shoulder width (median distance between left and right shoulders)
3. Normalized QdM (QdM / shoulder width)

### Entry point

Run:main.ipynb to execute the full pipeline on the test dataset.
Set: python
MODE = "test"   # or "raw"
Outputs are written to:
results/<MODE>/

## 4. R Statistical Analysis

The R workflow performs:
	•	Repeated-measures ANOVA
	•	Greenhouse–Geisser correction
	•	Bonferroni post-hoc comparisons
	•	Effect size (partial eta squared)

Entry point

Open in RStudio:main.Rmd and run the full notebook to perform the analysis on the test results.
Set: R_MODE = "test"   # or "raw"
results/<MODE>/vicon_QDM_wrists_head_normByShoulders.xlsx is the input for the R analysis.

## 5. Scientific Question

Does postural configuration influence global body movement dynamics?

# Hypothesis:

Standing posture induces higher indice of movement quantity.

## 6. Reproducibility
	•	All file paths are OS-independent (Path / here)
	•	No hard-coded absolute paths
	•	Full pipeline can be executed from main.ipynb and main.Rmd
	•	Results are automatically regenerated

## 7. Required Libraries

Python
	•	pandas
	•	numpy
	•	pathlib
	•	jupyter

R
	•	dplyr
	•	tidyr
	•	readxl
	•	ggplot2
	•	afex
	•	emmeans
	•	lme4
	•	lmerTest
	•	here
	•	stringr

⸻

8. Author

Matys Précloux
Master IEAP
University of Montpellier
2026