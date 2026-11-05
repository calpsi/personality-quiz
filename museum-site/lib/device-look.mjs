const radians = degrees => degrees * Math.PI / 180;

export function supportsDeviceLook(scope = globalThis) {
  return typeof scope?.DeviceOrientationEvent !== 'undefined';
}

export async function requestDeviceLook(scope = globalThis) {
  const DeviceOrientation = scope?.DeviceOrientationEvent;
  if (!DeviceOrientation) return false;
  if (typeof DeviceOrientation.requestPermission !== 'function') return true;
  try {
    return await DeviceOrientation.requestPermission() === 'granted';
  } catch {
    return false;
  }
}

// Mirrors the coordinate conversion used by Three.js' DeviceOrientationControls,
// but leaves the camera under the museum's existing collision/navigation system.
export function deviceLookQuaternion(THREE, event, screenAngle = 0) {
  if (event?.alpha == null || event?.beta == null || event?.gamma == null) return null;
  const alpha = Number(event?.alpha);
  const beta = Number(event?.beta);
  const gamma = Number(event?.gamma);
  if (![alpha, beta, gamma].every(Number.isFinite)) return null;

  const euler = new THREE.Euler(radians(beta), radians(alpha), -radians(gamma), 'YXZ');
  const sensor = new THREE.Quaternion().setFromEuler(euler);
  const faceForward = new THREE.Quaternion(-Math.sqrt(.5), 0, 0, Math.sqrt(.5));
  const screen = new THREE.Quaternion().setFromAxisAngle(
    new THREE.Vector3(0, 0, 1),
    -radians(Number(screenAngle) || 0)
  );
  return sensor.multiply(faceForward).multiply(screen).normalize();
}
