# Day 082: Chi-Square Test of Independence

## Overview
Implementation of a comprehensive Chi-Square Test of Independence module for categorical data analysis. Calculates expected contingency tables, chi-square test statistics, p-values, Yates' continuity correction, Cramer's V effect size, Haberman's standardized residuals, and Cochran's assumption validity checks.

## Objectives
- Understand practical application of Chi-Square Test of Independence.
- Write executable verification tests.

## Key Concepts
The Chi-Square Test of Independence tests whether two categorical variables are independent. Key components include:
1. Expected Frequencies: $E_{ij} = \frac{R_i \cdot C_j}{N}$, calculated under the null hypothesis of independence.
2. Chi-Square Statistic: $\chi^2 = \sum \frac{(|O_{ij} - E_{ij}| - Y)^2}{E_{ij}}$, where $Y=0.5$ is Yates' continuity correction for $2\times 2$ tables.
3. Effect Size (Cramer's V): $V = \sqrt{\frac{\chi^2}{N \cdot \min(r-1, c-1)}}$, measuring nominal association strength (0 = no association, 1 = complete association).
4. Standardized Residuals: $R_{ij} = \frac{O_{ij} - E_{ij}}{\sqrt{E_{ij}(1 - p_{row,i})(1 - p_{col,j})}}$, indicating individual cell contributions and significance ($|R_{ij}| > 2$ indicates key differences).
5. Cochran's Assumptions: Checks that expected cell counts are not $< 1$ and that no more than 20% of expected cell counts fall below 5.
