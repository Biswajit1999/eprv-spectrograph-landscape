# Doppler covariance and nuisance sensitivity (2026-11-03)

Independent synthetic validation of a **local** radial-velocity Fisher bound. No changes to instrument claims, the atlas, or the published information experiment.

The model differentiates expected counts with respect to velocity and uses a supplied positive-definite pixel covariance. The AR(1) helper preserves supplied marginal variances, with covariance C_ij = sqrt(v_i v_j) rho^|i-j|. A linear continuum nuisance design is marginalized through the inverse Fisher matrix (equivalent to a Schur complement).

Reproduce from repository root: `python -m pytest -q tests/test_doppler_covariance.py`. The five targeted tests verify the AR(1) entries, the independent-pixel limit, nuisance-information monotonicity, singularity rejection, and invalid-correlation rejection.

Illustrative Gaussian absorption line, 101 samples over ±4000 m/s, 100 count² marginal variance, rho=0.3: RV conditional standard deviation 1.366626 m/s with known continuum, 1.404833 m/s with constant and slope nuisances. These are numerical model outputs, **not** an EXOhSPEC or other instrument precision measurement.

Limitations: known covariance, linearized shift, fixed continuum model, finite-difference derivatives, no stellar variability, calibration drift, or barycentric corrections. Nuisance model rank must be checked. No independent observational validation is claimed.
