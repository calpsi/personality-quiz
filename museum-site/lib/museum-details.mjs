import * as THREE from 'three';
export function addMuseumDetails(scene){
 const group=new THREE.Group();group.name='Small museum stories';scene.add(group);
 const mat=c=>new THREE.MeshStandardMaterial({color:c,roughness:.92,flatShading:true});
 const wood=mat('#60432d'),paper=mat('#d9c79d'),brass=mat('#b99959'),green=mat('#63734b'),clay=mat('#946446');
 const mesh=(geo,m,x,y,z)=>{const o=new THREE.Mesh(geo,m);o.position.set(x,y,z);group.add(o);return o;};
 const box=(x,y,z,w,h,d,m)=>mesh(new THREE.BoxGeometry(w,h,d),m,x,y,z);
 // Reception: worn field guides, a brass bell, pencils and a forgotten cup.
 for(let i=0;i<4;i++){const b=box(-2.15,1.09+i*.055,6.65,.33,.045,.25,i%2?green:wood);b.rotation.y=i*.13;box(-2.15,1.09+i*.055,6.645,.3,.027,.255,paper);}
 mesh(new THREE.CylinderGeometry(.12,.15,.035,16),brass,-1.0,1.065,6.65);
 mesh(new THREE.SphereGeometry(.11,12,8,0,Math.PI*2,0,Math.PI/2),brass,-1,1.08,6.65);
 mesh(new THREE.SphereGeometry(.025,8,6),wood,-1,1.21,6.65);
 mesh(new THREE.CylinderGeometry(.07,.055,.13,12),clay,-1.35,1.12,6.9);
 for(let i=0;i<3;i++){const p=box(-1.39+i*.035,1.26,6.9,.012,.22,.012,brass);p.rotation.z=(i-1)*.15;}
 // Ferns sit at room edges, leaving doorways and routes clear.
 for(const [x,z] of [[-2.45,7.7],[2.4,7.7],[-10.9,-3.8],[10.9,-3.8],[3,-11.8]]){
  mesh(new THREE.CylinderGeometry(.22,.15,.34,9),clay,x,.24,z);
  mesh(new THREE.CylinderGeometry(.2,.2,.025,9),wood,x,.415,z);
  for(let i=0;i<9;i++){const a=i*2.4;const leaf=mesh(new THREE.SphereGeometry(1,5,4),green,x+Math.cos(a)*.14,.55+(i%3)*.12,z+Math.sin(a)*.14);leaf.scale.set(.075,.3,.035);leaf.rotation.set(Math.sin(a)*.6,a,Math.cos(a)*.6);}
 }
 // Framed pressed plants on the side walls of reception.
 for(const z of [5.9,7.05]){
  box(2.81,1.95,z,.07,.65,.48,wood);box(2.765,1.95,z,.012,.55,.38,paper);
  box(2.75,1.96,z,.014,.36,.014,green);
  for(let i=0;i<5;i++){const leaf=mesh(new THREE.SphereGeometry(1,5,4),green,2.73,1.83+i*.055,z+(i%2?1:-1)*.065);leaf.scale.set(.015,.035,.075);leaf.rotation.x=i%2?.5:-.5;}
 }
 // A small stack of accession boxes, with cream labels.
 for(let i=0;i<3;i++){box(10.8,.2+i*.31,3.8,.6,.28,.42,i%2?wood:green);box(10.8,.2+i*.31,3.575,.21,.09,.015,paper);}
 const dust=new THREE.BufferGeometry(),points=[];for(let i=0;i<55;i++)points.push(Math.sin(i*12.7)*2.6,.5+(i%13)*.2,Math.cos(i*7.9)*3.5);
 dust.setAttribute('position',new THREE.Float32BufferAttribute(points,3));const motes=new THREE.Points(dust,new THREE.PointsMaterial({color:'#e5c791',size:.018,transparent:true,opacity:.38,depthWrite:false}));group.add(motes);
 return {update(t,reduced){motes.position.y=reduced?0:Math.sin(t*.2)*.07;}};
}
