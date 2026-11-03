import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from research.doppler_covariance import ar1_covariance, shift_information  # noqa: E402


def spectrum():
    x = np.linspace(-4000, 4000, 101)
    y = 10000 - 2500 * np.exp(-0.5 * (x / 700) ** 2)
    return x, y


def test_ar1_diagonal_and_off_diagonal():
    c = ar1_covariance([4, 9, 16], 0.5)
    assert np.allclose(np.diag(c), [4, 9, 16])
    assert c[0, 1] == pytest.approx(3)
    assert c[0, 2] == pytest.approx(2)


def test_white_noise_fisher_matches_direct_sum():
    x, y = spectrum()
    sigma = shift_information(x, y, np.eye(x.size) * 100)
    expected = 1 / np.sqrt(np.sum(np.gradient(y, x) ** 2 / 100))
    assert sigma == pytest.approx(expected, rel=1e-10)


def test_nuisance_profiling_never_improves_bound():
    x, y = spectrum()
    c = ar1_covariance(np.full(x.size, 100.), 0.3)
    basic = shift_information(x, y, c)
    profiled = shift_information(x, y, c, np.column_stack([np.ones(x.size), x / 4000]))
    assert profiled >= basic


def test_singular_nuisance_rejected():
    x, y = spectrum()
    with pytest.raises(ValueError):
        shift_information(x, y, np.eye(x.size), np.ones((x.size, 2)))


def test_invalid_correlation_rejected():
    with pytest.raises(ValueError):
        ar1_covariance([1, 1, 1], 1)
