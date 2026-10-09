import test from 'node:test';
import assert from 'node:assert/strict';

import { calculateDopplerShift, SPEED_OF_LIGHT_MPS } from '../src/doppler.js';

test('a 1 m/s recession at 550 nm produces the expected first-order shift', () => {
  const result = calculateDopplerShift({ velocityMps: 1, wavelengthNm: 550 });

  assert.ok(Math.abs(result.deltaWavelengthPm - 550_000 / SPEED_OF_LIGHT_MPS) < 1e-12);
  assert.equal(result.direction, 'redshift');
  assert.ok(Math.abs(result.resolutionElementPercent - 100_000 / SPEED_OF_LIGHT_MPS * 100) < 1e-12);
});

test('approaching motion preserves the sign and reports a blueshift', () => {
  const result = calculateDopplerShift({ velocityMps: -12.5, wavelengthNm: 1_000 });

  assert.ok(result.deltaWavelengthPm < 0);
  assert.equal(result.direction, 'blueshift');
});

test('zero velocity leaves the wavelength unchanged', () => {
  const result = calculateDopplerShift({ velocityMps: 0, wavelengthNm: 400 });

  assert.equal(result.shiftedWavelengthNm, 400);
  assert.equal(result.deltaWavelengthPm, 0);
  assert.equal(result.direction, 'no shift');
});

test('invalid wavelength and resolving power inputs are rejected', () => {
  assert.throws(
    () => calculateDopplerShift({ velocityMps: 1, wavelengthNm: 0 }),
    /Wavelength/,
  );
  assert.throws(
    () => calculateDopplerShift({ velocityMps: 1, wavelengthNm: 550, resolvingPower: 0 }),
    /Resolving power/,
  );
});
