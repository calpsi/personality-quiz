import * as THREE from 'three';
// Floor-space route goes through door centres and around the central display.
export const patrolRoute=[[2.1,.6],[3,0],[5,0],[7,0],[7,-2],[5,0],[3,0],[2.2,-2.7],[0,-3.3],[0,-5.8],[0,-8],[0,-6],[0,-3.3],[-2.2,-2.7],[-2.3,0],[-5,0],[-6.3,0],[-6.3,2.8],[-5,0],[-2.3,0],[-2.2,2],[0,2],[2.1,.6]];
export function createPatrol(character){
 const bones={};character.traverse(o=>{if(o.isBone)bones[o.name]={bone:o,rest:o.quaternion.clone()};});
 const axis=new THREE.Vector3(1,0,0),q=new THREE.Quaternion();let segment=0,wait=1.5,phase=0;
 const baseY=character.position.y;const originOffset=new THREE.Vector3(character.position.x-patrolRoute[0][0],0,character.position.z-patrolRoute[0][1]);
 function pose(name,angle){const b=bones[name]||bones[THREE.PropertyBinding.sanitizeNodeName(name)];if(b){q.setFromAxisAngle(axis,angle);b.bone.quaternion.copy(b.rest).multiply(q);}}
 return {bones:Object.keys(bones),update(dt,reduced=false){
  if(reduced){for(const b of Object.values(bones))b.bone.quaternion.copy(b.rest);return;}
  if(wait>0){wait-=dt;pose('leg.L',0);pose('leg.R',0);pose('foot.L',0);pose('foot.R',0);character.position.y=baseY;return;}
  const next=patrolRoute[(segment+1)%patrolRoute.length],target=new THREE.Vector3(next[0]+originOffset.x,baseY,next[1]+originOffset.z),delta=target.clone().sub(character.position);delta.y=0;
  const distance=delta.length(),step=Math.min(distance,dt*.42);
  if(distance>.001){character.position.addScaledVector(delta.normalize(),step);const desired=new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(0,1,0),Math.atan2(delta.x,delta.z));character.quaternion.slerp(desired,1-Math.exp(-dt*6));}
  phase+=step*20;const swing=Math.sin(phase)*.23;
  pose('leg.L',swing);pose('leg.R',-swing);pose('foot.L',-.4*swing);pose('foot.R',.4*swing);pose('upper_arm.L',-.25*swing);pose('upper_arm.R',.25*swing);
  character.position.y=baseY+Math.abs(Math.sin(phase))*.012;
  if(distance<.025){segment=(segment+1)%patrolRoute.length;if([3,10,17].includes(segment))wait=2.5;}
 }};
}
