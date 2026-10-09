export const SPEED_OF_LIGHT_MPS = 299_792_458;

export function calculateDopplerShift({
  velocityMps,
  wavelengthNm,
  resolvingPower = 100_000,
}) {
  const velocity = Number(velocityMps);
  const wavelength = Number(wavelengthNm);
  const resolution = Number(resolvingPower);

  if (!Number.isFinite(velocity)) throw new TypeError('Velocity must be finite.');
  if (!Number.isFinite(wavelength) || wavelength <= 0) {
    throw new RangeError('Wavelength must be greater than zero.');
  }
  if (!Number.isFinite(resolution) || resolution <= 0) {
    throw new RangeError('Resolving power must be greater than zero.');
  }

  const deltaWavelengthNm = wavelength * velocity / SPEED_OF_LIGHT_MPS;
  const resolutionElementNm = wavelength / resolution;

  return {
    shiftedWavelengthNm: wavelength + deltaWavelengthNm,
    deltaWavelengthPm: deltaWavelengthNm * 1_000,
    fractionalShift: velocity / SPEED_OF_LIGHT_MPS,
    resolutionElementPm: resolutionElementNm * 1_000,
    resolutionElementPercent: Math.abs(deltaWavelengthNm / resolutionElementNm) * 100,
    direction: velocity > 0 ? 'redshift' : velocity < 0 ? 'blueshift' : 'no shift',
  };
}
