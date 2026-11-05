import test from 'node:test';
import assert from 'node:assert/strict';
import {Vector3} from 'three';
import {walkable,routeTo,constrainMove} from '../lib/navigation.mjs';
test('camera cannot tunnel through partitions or leave outer walls',()=>{
 for(const [a,b] of [[[3,0,3],[8,0,3]],[[8,0,0],[30,0,0]],[[0,1,-4],[3,1,-8]]]){
  const start=new Vector3(...a),end=constrainMove(start,new Vector3(...b));assert.ok(walkable(end.x,end.z));assert.ok(end.distanceTo(new Vector3(...b))>1);
 }
});
test('camera cannot enter exhibit cabinets while approaching a placard',()=>{
 for(const [x,z] of [[-8.6,0],[8.6,1],[-1.9,-9.8],[2,-9.5],[6.1,-3.4]])assert.equal(walkable(x,z),false);
 for(const [x,z] of [[-8.1,0],[8.1,1],[0,-10],[0,-8],[5.3,-.2]])assert.equal(walkable(x,z),true);
});
test('Abraham paths between galleries use open floor and doorways',()=>{
 for(const [a,b] of [[[-7,0,3],[7,0,3]],[[7,0,0],[0,0,-10]],[[0,0,-10],[-7,0,2]]]){
  const path=routeTo(new Vector3(...a),new Vector3(...b));assert.ok(path.length>0);for(const [x,z] of path)assert.ok(walkable(x,z));const last=path.at(-1);assert.ok(Math.hypot(last[0]-b[0],last[1]-b[2])<.5);
 }
});
