import pytest
import numpy as np
from learning.statistics.day_081_two_sample_ttest import TwoSampleTTest

def test_welch_ttest_significant():
    np.random.seed(42)
    group_a = np.random.normal(loc=10.0, scale=2.0, size=30)
    group_b = np.random.normal(loc=12.5, scale=4.0, size=25)
    result = TwoSampleTTest.welch_ttest(group_a, group_b, alpha=0.05)
    
    assert "t_statistic" in result
    assert "p_value" in result
    assert result["reject_null"] is True
    assert result["p_value"] < 0.05

def test_student_ttest_equal_means():
    np.random.seed(123)
    group_a = np.random.normal(loc=5.0, scale=1.5, size=40)
    group_b = np.random.normal(loc=5.1, scale=1.5, size=40)
    result = TwoSampleTTest.student_ttest(group_a, group_b, alpha=0.05)
    
    assert isinstance(result["degrees_of_freedom"], int)
    assert result["reject_null"] is False
    assert result["p_value"] > 0.05

def test_paired_ttest():
    np.random.seed(77)
    before = np.random.normal(loc=50.0, scale=5.0, size=20)
    after = before + np.random.normal(loc=2.0, scale=1.0, size=20)
    result = TwoSampleTTest.paired_ttest(before, after, alpha=0.05)
    
    assert result["t_statistic"] < 0
    assert result["reject_null"] is True

def test_paired_ttest_dimension_mismatch():
    sample1 = [1, 2, 3]
    sample2 = [1, 2]
    with pytest.raises(ValueError, match="Paired samples must have the same number of observations."):
        TwoSampleTTest.paired_ttest(sample1, sample2)
