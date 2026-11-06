import test from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from 'three';
import {deviceLookQuaternion,requestDeviceLook,supportsDeviceLook} from '../lib/device-look.mjs';
import {characterTapVolume,neutralLookDirection,rebaseMotionState,recenteredLookTarget} from '../lib/camera-recenter.mjs';

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

test('recenter restores the gallery heading without moving the visitor',()=>{
  const position=[4,2,4],currentTarget=[7,3,8];
  const forward=neutralLookDirection([0,2,4],[0,1,-1]);
  const target=recenteredLookTarget(position,currentTarget,forward);
  assert.deepEqual(position,[4,2,4]);
  assert.ok(Math.abs(Math.hypot(...target.map((value,index)=>value-position[index]))-Math.hypot(3,1,4))<1e-10);
  const actual=neutralLookDirection(position,target);
  actual.forEach((value,index)=>assert.ok(Math.abs(value-forward[index])<1e-10));
});

test('manual look rebases gyro motion and Abraham gets a forgiving tap volume',()=>{
  const sensor={id:'sensor',clone(){return {id:this.id};}},camera={id:'camera',clone(){return {id:this.id};}};
  const motion={current:sensor,baseSensor:null,baseCamera:null,rebase:true};
  rebaseMotionState(motion,camera);
  assert.deepEqual(motion.baseSensor,{id:'sensor'});
  assert.deepEqual(motion.baseCamera,{id:'camera'});
  assert.equal(motion.rebase,false);
  const volume=characterTapVolume([.4,2,.5],.6);
  assert.ok(volume[0]>=.9&&volume[1]>=1.35&&volume[2]>=.9);
});
