import math
import pytest
from learning.statistics.day_077_probability_distributions import (
    NormalDistribution,
    BinomialDistribution,
    PoissonDistribution,
)


def test_normal_distribution_properties():
    norm = NormalDistribution(mean=10.0, std_dev=2.0)
    assert norm.mean == 10.0
    assert norm.std_dev == 2.0
    assert norm.variance == 4.0

    expected_pdf_mean = 1.0 / (2.0 * math.sqrt(2.0 * math.pi))
    assert pytest.approx(norm.pdf(10.0), rel=1e-6) == expected_pdf_mean
    assert pytest.approx(norm.cdf(10.0), rel=1e-6) == 0.5

    p_1sig = norm.probability_range(8.0, 12.0)
    assert pytest.approx(p_1sig, rel=1e-4) == 0.682689

    with pytest.raises(ValueError):
        NormalDistribution(mean=0, std_dev=-1.0)
    with pytest.raises(ValueError):
        norm.probability_range(10.0, 5.0)


def test_binomial_distribution_properties():
    binom = BinomialDistribution(trials=10, p=0.5)
    assert binom.mean == 5.0
    assert binom.variance == 2.5

    assert pytest.approx(binom.pmf(5), rel=1e-6) == 0.24609375
    assert binom.pmf(-1) == 0.0
    assert binom.pmf(11) == 0.0

    assert pytest.approx(binom.cdf(10), rel=1e-6) == 1.0
    assert binom.cdf(-1) == 0.0

    with pytest.raises(ValueError):
        BinomialDistribution(trials=-5, p=0.5)
    with pytest.raises(ValueError):
        BinomialDistribution(trials=10, p=1.5)


def test_poisson_distribution_properties():
    pois = PoissonDistribution(rate=3.0)
    assert pois.mean == 3.0
    assert pois.variance == 3.0

    assert pytest.approx(pois.pmf(0), rel=1e-6) == math.exp(-3.0)
    assert pytest.approx(pois.pmf(3), rel=1e-6) == 4.5 * math.exp(-3.0)

    cdf_3 = pois.pmf(0) + pois.pmf(1) + pois.pmf(2) + pois.pmf(3)
    assert pytest.approx(pois.cdf(3), rel=1e-6) == cdf_3
    assert pois.cdf(-1) == 0.0

    with pytest.raises(ValueError):
        PoissonDistribution(rate=0.0)


def test_summary_dictionaries():
    norm_summary = NormalDistribution(0, 1).summary()
    assert norm_summary["mean"] == 0.0
    assert norm_summary["std_dev"] == 1.0

    binom_summary = BinomialDistribution(20, 0.2).summary()
    assert binom_summary["trials"] == 20.0
    assert binom_summary["mean"] == 4.0

    pois_summary = PoissonDistribution(4.0).summary()
    assert pois_summary["rate"] == 4.0
    assert pytest.approx(pois_summary["skewness"], rel=1e-6) == 0.5
