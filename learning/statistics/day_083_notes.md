# Day 083: Analysis of Variance (ANOVA) Engine

## Overview
Implementation of standard One-Way ANOVA, Welch's robust ANOVA (for heteroscedastic data), assumption diagnostics (Shapiro-Wilk and Levene tests), effect size calculations (Eta-squared and Omega-squared), and post-hoc Tukey HSD pairwise comparisons.

## Objectives
- Understand practical application of ANOVA (Analysis of Variance).
- Write executable verification tests.

## Key Concepts
ANOVA (Analysis of Variance) tests whether the population means of several groups are equal by partitioning total variance into variation between groups (due to factor effects) and variation within groups (random sampling error). This engine calculates standard sum of squares (SS_total, SS_between, SS_within), mean squares, and F-ratio. It also includes Welch's ANOVA to handle heteroscedasticity (unequal group variances), measures effect sizes using Eta-squared (sample variance explained) and Omega-squared (population variance explained bias-corrected), and computes Tukey HSD for post-hoc pairwise comparisons.
