import {test} from 'node:test';import assert from 'node:assert/strict';import {readFileSync} from 'node:fs';import * as THREE from 'three';import {createPatrol,patrolRoute} from '../lib/abraham-walk.mjs';
test('exported rig legs and feet move, without adding bones or changing skin weights',()=>{
 const b=readFileSync(new URL('../public/assets/abraham.glb',import.meta.url));const json=JSON.parse(b.subarray(20,20+b.readUInt32LE(12)).toString());const rig=new THREE.Group();rig.position.set(2.1,.12,.6);
 for(const index of json.skins[0].joints){const n=json.nodes[index];const bone=new THREE.Bone();bone.name=THREE.PropertyBinding.sanitizeNodeName(n.name);if(n.rotation)bone.quaternion.fromArray(n.rotation);rig.add(bone);}
 const patrol=createPatrol(rig);const leg=rig.getObjectByName('legL'),foot=rig.getObjectByName('footL');assert.ok(leg&&foot);const before=leg.quaternion.clone(),footBefore=foot.quaternion.clone();patrol.update(2);patrol.update(.1);assert.ok(leg.quaternion.angleTo(before)>.01);assert.ok(foot.quaternion.angleTo(footBefore)>.001);assert.ok(rig.position.distanceTo(new THREE.Vector3(2.1,.12,.6))>.01);
 const p=rig.position.clone();patrol.update(1,true);assert.deepEqual(rig.position,p);assert.ok(leg.quaternion.angleTo(before)<.00001);
});
test('patrol crosses gallery walls only within doorway openings',()=>{
 for(let i=0;i<patrolRoute.length;i++){const a=patrolRoute[i],b=patrolRoute[(i+1)%patrolRoute.length];for(const wall of [-4,4])if((a[0]-wall)*(b[0]-wall)<0){const t=(wall-a[0])/(b[0]-a[0]);assert.ok(Math.abs(a[1]+t*(b[1]-a[1]))<1.2);}if((a[1]+5)*(b[1]+5)<0){const t=(-5-a[1])/(b[1]-a[1]);assert.ok(Math.abs(a[0]+t*(b[0]-a[0]))<1.2);}}
});
