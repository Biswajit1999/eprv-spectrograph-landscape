"""Conditional Doppler information with correlated noise and continuum nuisances.

Synthetic linearized experiments only; not an achieved instrument RV precision.
"""
import numpy as np


def ar1_covariance(variance, rho):
    """Stationary AR(1) covariance with supplied marginal pixel variances."""
    v = np.asarray(variance, dtype=float)
    if v.ndim != 1 or v.size < 3 or not np.all(np.isfinite(v)) or np.any(v <= 0):
        raise ValueError('variance must be a positive finite vector of length >=3')
    if not np.isfinite(rho) or abs(rho) >= 1:
        raise ValueError('AR(1) correlation must satisfy |rho| < 1')
    idx = np.arange(v.size)
    return np.sqrt(np.outer(v, v)) * rho ** np.abs(idx[:, None] - idx[None, :])


def shift_information(velocity_mps, expected_counts, covariance, nuisance=None):
    """Schur-complement RV Fisher bound after profiling linear nuisance columns.

    Covariance is assumed known and independent of the RV parameter. The
    derivative uses np.gradient on the provided velocity coordinate.
    """
    x = np.asarray(velocity_mps, dtype=float)
    y = np.asarray(expected_counts, dtype=float)
    c = np.asarray(covariance, dtype=float)
    if x.ndim != 1 or y.shape != x.shape or x.size < 3 or not np.all(np.diff(x) > 0):
        raise ValueError('velocity grid must be increasing and match expected counts')
    if not np.all(np.isfinite(y)) or c.shape != (x.size, x.size) or not np.all(np.isfinite(c)):
        raise ValueError('invalid model or covariance')
    if not np.allclose(c, c.T, atol=1e-10, rtol=1e-10):
        raise ValueError('covariance must be symmetric')
    try:
        np.linalg.cholesky(c)
    except np.linalg.LinAlgError as exc:
        raise ValueError('covariance must be positive definite') from exc
    derivative = -np.gradient(y, x)
    if nuisance is None:
        design = derivative[:, None]
    else:
        n = np.asarray(nuisance, dtype=float)
        if n.ndim != 2 or n.shape[0] != x.size or not np.all(np.isfinite(n)):
            raise ValueError('nuisance must be a finite n-by-k matrix')
        design = np.column_stack((derivative, n))
    fisher = design.T @ np.linalg.solve(c, design)
    try:
        covariance_parameters = np.linalg.inv(fisher)
    except np.linalg.LinAlgError as exc:
        raise ValueError('RV and nuisance directions are not identifiable') from exc
    variance_rv = covariance_parameters[0, 0]
    if not np.isfinite(variance_rv) or variance_rv <= 0:
        raise ValueError('non-positive RV information')
    return float(np.sqrt(variance_rv))
