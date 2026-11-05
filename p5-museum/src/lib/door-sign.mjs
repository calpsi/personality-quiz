import * as THREE from 'three';
export function createDoorSign(scene){
 const canvas=document.createElement('canvas');canvas.width=1536;canvas.height=256;
 const ctx=canvas.getContext('2d'),texture=new THREE.CanvasTexture(canvas);texture.colorSpace=THREE.SRGBColorSpace;
 const sign=new THREE.Mesh(new THREE.PlaneGeometry(1.85,.36),new THREE.MeshBasicMaterial({map:texture,transparent:true,depthWrite:false,side:THREE.DoubleSide}));
 sign.position.set(0,2.4,8.55);sign.rotation.y=Math.PI;scene.add(sign);
 const phrases=['WHERE ARE YOU GOING?','YOU BELONG HERE','STAY A LITTLE LONGER','YOU HAVE BEEN HERE BEFORE','THERE IS NOTHING OUTSIDE'];
 let previous='';
 return {update(time,reduced){
  sign.position.y=2.4+(reduced?0:Math.sin(time*.75)*.035);
  const cycle=Math.floor(time/9),phase=time%9,glitch=!reduced&&phase>8.65;
  const index=reduced?1:cycle%phrases.length;
  const frame=glitch?Math.floor(time*16):0,key=`${index}:${frame}:${reduced}`;if(key===previous)return;previous=key;
  ctx.clearRect(0,0,1536,256);
  ctx.font='500 66px MuseumSerif, Georgia, serif';ctx.textAlign='center';ctx.textBaseline='middle';
  const words=phrases[index],shift=glitch?Math.sin(frame*7)*12:0;
  ctx.fillStyle='#a5b39a';ctx.fillText(words,772-shift,129);ctx.fillStyle='#c08c66';ctx.fillText(words,765+shift,134);
  ctx.fillStyle='#f3e3bd';ctx.fillText(words,768+shift,132);
  if(glitch){ctx.save();ctx.beginPath();ctx.rect(50,100,1436,22);ctx.clip();ctx.clearRect(50,100,1436,22);ctx.fillStyle='#d9bf94';ctx.fillText(words,768-shift*2,132);ctx.restore();}
  texture.needsUpdate=true;
 }};
}
