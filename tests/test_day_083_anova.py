"""
Unit tests for Day 083: Analysis of Variance (ANOVA) Engine
"""

import numpy as np
import pytest
from scipy import stats
from learning.statistics.day_083_anova import (
    OneWayANOVA,
    ANOVAResult,
    AssumptionCheckResult
)


@pytest.fixture
def sample_experiment_data():
    np.random.seed(42)
    return {
        "Control": [85, 88, 90, 93, 86, 89],
        "Treatment_A": [70, 75, 72, 68, 74, 71],
        "Treatment_B": [95, 98, 92, 96, 94, 97]
    }


def test_init_validation():
    with pytest.raises(ValueError, match="Alpha must be strictly between 0 and 1."):
        OneWayANOVA(alpha=0.0)
    with pytest.raises(ValueError, match="Alpha must be strictly between 0 and 1."):
        OneWayANOVA(alpha=1.5)


def test_fit_against_scipy(sample_experiment_data):
    anova = OneWayANOVA(alpha=0.05)
    res = anova.fit(sample_experiment_data)

    f_scipy, p_scipy = stats.f_oneway(
        sample_experiment_data["Control"],
        sample_experiment_data["Treatment_A"],
        sample_experiment_data["Treatment_B"]
    )

    assert pytest.approx(res.f_statistic, rel=1e-5) == f_scipy
    assert pytest.approx(res.p_value, rel=1e-5) == p_scipy
    assert isinstance(res, ANOVAResult)


def test_sum_of_squares_identity(sample_experiment_data):
    anova = OneWayANOVA()
    res = anova.fit(sample_experiment_data)

    assert pytest.approx(res.ss_total, rel=1e-5) == res.ss_between + res.ss_within
    assert res.df_total == res.df_between + res.df_within
    assert res.df_between == 2
    assert res.df_within == 15
    assert res.df_total == 17


def test_effect_sizes(sample_experiment_data):
    anova = OneWayANOVA()
    res = anova.fit(sample_experiment_data)

    assert 0.0 <= res.eta_squared <= 1.0
    assert 0.0 <= res.omega_squared <= 1.0
    assert res.omega_squared <= res.eta_squared


def test_check_assumptions(sample_experiment_data):
    anova = OneWayANOVA()
    assumptions = anova.check_assumptions(sample_experiment_data)

    assert isinstance(assumptions, AssumptionCheckResult)
    assert assumptions.homogeneity_p_value > 0.0
    assert isinstance(assumptions.equal_variances_assumed, bool)
    assert len(assumptions.normality_p_values) == 3


def test_welch_anova():
    np.random.seed(123)
    data = {
        "Group_A": np.random.normal(loc=10.0, scale=1.0, size=30),
        "Group_B": np.random.normal(loc=12.0, scale=5.0, size=30),
        "Group_C": np.random.normal(loc=15.0, scale=10.0, size=30)
    }

    anova = OneWayANOVA()
    f_welch, df1, df2, p_val = anova.welch_anova(data)

    assert f_welch > 0.0
    assert df1 == 2.0
    assert df2 > 0.0
    assert 0.0 <= p_val <= 1.0


def test_tukey_hsd(sample_experiment_data):
    anova = OneWayANOVA()
    tukey_results = anova.tukey_hsd(sample_experiment_data)

    # Number of pair combinations for 3 groups is 3 * 2 / 2 = 3
    assert len(tukey_results) == 3
    for pair in tukey_results:
        assert "group1" in pair
        assert "group2" in pair
        assert "mean_diff" in pair
        assert "p_val" in pair
        assert "reject_null" in pair
        assert 0.0 <= pair["p_val"] <= 1.0


def test_fit_invalid_inputs():
    anova = OneWayANOVA()
    
    with pytest.raises(ValueError, match="ANOVA requires at least 2 comparison groups."):
        anova.fit({"Group1": [1, 2, 3]})

    with pytest.raises(ValueError, match="must be a non-empty 1D array."):
        anova.fit({"Group1": [], "Group2": [1, 2, 3]})
