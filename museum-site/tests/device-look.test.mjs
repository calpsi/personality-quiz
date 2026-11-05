import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from 'three';
import {deviceLookQuaternion,requestDeviceLook,supportsDeviceLook} from '../lib/device-look.mjs';

test('device look rejects incomplete sensor readings',()=>{
  assert.equal(deviceLookQuaternion(THREE,{alpha:null,beta:10,gamma:2}),null);
});

test('device look produces a stable normalised orientation',()=>{
  const reading={alpha:35,beta:72,gamma:-8};
  const first=deviceLookQuaternion(THREE,reading,90);
  const second=deviceLookQuaternion(THREE,reading,90);
  assert.ok(Math.abs(first.length()-1)<1e-10);
  assert.ok(first.angleTo(second)<1e-10);
});

test('motion permission works for Android-style and iOS-style APIs',async()=>{
  assert.equal(supportsDeviceLook({DeviceOrientationEvent:function(){}}),true);
  assert.equal(await requestDeviceLook({DeviceOrientationEvent:function(){}}),true);
  assert.equal(await requestDeviceLook({DeviceOrientationEvent:{requestPermission:async()=> 'granted'}}),true);
  assert.equal(await requestDeviceLook({DeviceOrientationEvent:{requestPermission:async()=> 'denied'}}),false);
});
