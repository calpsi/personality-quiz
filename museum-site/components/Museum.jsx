'use client';
import {useEffect,useRef,useState} from 'react';
import * as THREE from 'three';
import Joystick from './Joystick';
import {constrainMove} from '../lib/navigation.mjs';
import {createDoorSign} from '../lib/door-sign.mjs';
import {addMuseumDetails} from '../lib/museum-details.mjs';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {createPatrol} from '../lib/abraham-walk.mjs';
import {DRACOLoader} from 'three/addons/loaders/DRACOLoader.js';
import {deviceLookQuaternion,requestDeviceLook,supportsDeviceLook} from '../lib/device-look.mjs';

const views={hall:[[0,2.05,4.4],[0,1.65,-.7]],'Deep Time':[[-5.5,2.1,3.8],[-9,1.6,-1.4]],'Earth & Space':[[5.4,2.05,3.5],[9,1.5,-1.9]],'Living Systems':[[0,1.9,-5.8],[0,1.6,-10]],q1:[[-8.1,1.95,4.3],[-10.1,1.65,2.8]],q2:[[-7,2.1,.6],[-9,1.5,-1.8]],q3:[[-8.5,2,1],[-8.5,2.1,-4.65]],q4:[[8,1.9,4.6],[10,1.4,2.8]],q5:[[8,2,1.2],[10,1.7,-1.4]],q6:[[5.3,1.9,-.2],[6.1,1.55,-3.4]],q7:[[-1.9,1.9,-6.8],[-1.9,1.5,-9.8]],q8:[[2,1.9,-6.8],[2,1.2,-9.5]]};

import {specimen} from '../lib/result-specimens.mjs';
export default function Museum({view='hall',resultCode=null,reduced=false,onInteract=()=>{},discoveries=[],reception=false,speaking=false,talking=false,choice=null}){
 const talkingRef=useRef(talking);talkingRef.current=talking;
 const thought=useRef(null),speech=useRef(speaking);speech.current=speaking;
 const host=useRef(null),control=useRef(null),callback=useRef(onInteract);callback.current=onInteract;
 const [motionAvailable,setMotionAvailable]=useState(false),[motionEnabled,setMotionEnabled]=useState(false),[motionDenied,setMotionDenied]=useState(false);
 const [thoughtText,setThoughtText]=useState('Now, where did I put my pencil?');
 useEffect(()=>{setMotionAvailable(supportsDeviceLook(window)&&window.matchMedia('(pointer: coarse)').matches);},[]);
 useEffect(()=>{control.current?.setMotion?.(motionEnabled);},[motionEnabled]);
 const toggleMotion=async()=>{
  if(motionEnabled){setMotionEnabled(false);return;}
  const allowed=await requestDeviceLook(window);setMotionDenied(!allowed);if(allowed)setMotionEnabled(true);
 };
 useEffect(()=>{if(resultCode||reception)return;const lines=['I hope the stars stay in the drawer.','Was that label always over there?','One stamp, two stamps… oh, a pencil!','The clock seems quite pleased today.','I should dust that. When it comes down.'];let last=-1;const id=setInterval(()=>{let next=Math.floor(Math.random()*lines.length);if(next===last)next=(next+1)%lines.length;last=next;setThoughtText(lines[next]);},11000);return()=>clearInterval(id);},[resultCode,reception]);
 const [status,setStatus]=useState('Opening the museum…');
 useEffect(()=>{
  const el=host.current;let renderer;try{renderer=new THREE.WebGLRenderer({antialias:true,alpha:!!resultCode,powerPreference:'low-power'});}catch{setStatus('The museum could not open. Please reload or try another browser.');return;}
  renderer.setPixelRatio(Math.min(window.devicePixelRatio,2));renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.12;renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;el.appendChild(renderer.domElement);
  const scene=new THREE.Scene();if(!resultCode)scene.background=new THREE.Color('#251a16');
  const doorSign=!resultCode?createDoorSign(scene):null;
  const details=!resultCode?addMuseumDetails(scene):null;
  const camera=new THREE.PerspectiveCamera(resultCode?35:63,1,.08,100);const look=new THREE.Vector3();
  let targetPos=new THREE.Vector3(),targetLook=new THREE.Vector3(),yaw=0,disposed=false,frame,model,hamster,mixer,patrol,caseTitle;const moving=[];
  scene.add(new THREE.HemisphereLight(0xffedcf,0x635442,1.45));const light=new THREE.DirectionalLight(0xffdfb0,2.3);light.position.set(-3,8,4);scene.add(light);
  light.castShadow=true;light.shadow.mapSize.set(2048,2048);Object.assign(light.shadow.camera,{left:-14,right:14,top:14,bottom:-14,near:.5,far:35});light.shadow.normalBias=.04;light.shadow.bias=-.00015;light.shadow.radius=3;
  if(!resultCode)scene.fog=new THREE.FogExp2('#30271f',.018);
  for(const p of [[0,3,0],[-9,3,-1],[9,3,-1],[0,3,-10]]){const l=new THREE.PointLight(0xffcf84,17,8,1.5);l.position.set(...p);scene.add(l);}
  if(!resultCode&&!reception){
   const stops=[[-10.1,2.3,2.8],[-9,2.9,-1.8],[-8.5,2.9,-4.3],[10,2.3,2.8],[10,2.6,-1.4],[6.1,2.5,-3.4],[-1.9,2.4,-9.8],[2,2,-9.5]];
   stops.forEach((p,i)=>{const canvas=document.createElement('canvas');canvas.width=128;canvas.height=128;const ctx=canvas.getContext('2d');ctx.fillStyle='#e3c995';ctx.beginPath();ctx.arc(64,64,44,0,Math.PI*2);ctx.fill();ctx.strokeStyle='#68563a';ctx.lineWidth=3;ctx.stroke();ctx.fillStyle='#39402b';ctx.font='46px Georgia';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(String(i+1).padStart(2,'0'),64,65);const texture=new THREE.CanvasTexture(canvas);texture.colorSpace=THREE.SRGBColorSpace;const marker=new THREE.Sprite(new THREE.SpriteMaterial({map:texture,depthTest:true}));marker.position.set(...p);marker.scale.set(.55,.55,1);marker.userData.interaction_id='q'+(i+1);scene.add(marker);});
  }
  if(!resultCode){
   // Milky panels are built separately from the merged architecture export.
   const frost=new THREE.MeshPhysicalMaterial({color:'#c9d0bd',roughness:.94,metalness:0,transparent:true,opacity:.83,transmission:.16,thickness:.12,side:THREE.DoubleSide,depthWrite:false});
   for(let i=0;i<8;i++){const angle=i*Math.PI/4+Math.PI/8;const pane=new THREE.Mesh(new THREE.PlaneGeometry(.82,1.12),frost);pane.position.set(1.02*Math.cos(angle),1.83,-.3-1.02*Math.sin(angle));pane.rotation.y=angle+Math.PI/2;scene.add(pane);}
   if(!reception){const canvas=document.createElement('canvas');canvas.width=1024;canvas.height=160;const context=canvas.getContext('2d');const paint=()=>{context.clearRect(0,0,1024,160);context.textAlign='center';context.textBaseline='middle';context.font='62px MuseumSerif, Georgia, serif';context.fillStyle='#a4b59d';context.fillText('WHAT ARE YOU?',516,77);context.fillStyle='#b57a59';context.fillText('WHAT ARE YOU?',508,83);context.fillStyle='#f3e3bd';context.fillText('WHAT ARE YOU?',512,80);};paint();const texture=new THREE.CanvasTexture(canvas);texture.colorSpace=THREE.SRGBColorSpace;document.fonts.ready.then(()=>{if(!disposed){paint();texture.needsUpdate=true;}});caseTitle=new THREE.Sprite(new THREE.SpriteMaterial({map:texture,depthTest:true,transparent:true}));caseTitle.position.set(0,3.24,-.3);caseTitle.scale.set(3.1,.48,1);scene.add(caseTitle);}
  }
  const draco=new DRACOLoader();draco.setDecoderPath('/assets/draco/');const loader=new GLTFLoader().setDRACOLoader(draco);
  if(resultCode){model=specimen(resultCode);scene.add(model);
   const cabinet=new THREE.Group();scene.add(cabinet);
   const brass=new THREE.MeshStandardMaterial({color:'#a88a54',roughness:.55,metalness:.35}),wood=new THREE.MeshStandardMaterial({color:'#493322',roughness:.85});
   const part=(w,h,d,x,y,z,material)=>{const m=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),material);m.position.set(x,y,z);m.castShadow=true;m.receiveShadow=true;cabinet.add(m);};
   part(2.2,.18,1.4,0,-.89,0,wood);part(2.25,.04,1.45,0,-.78,0,brass);
   for(const x of [-1.06,1.06])for(const z of [-.66,.66])part(.035,1.85,.035,x,.12,z,brass);
   part(2.2,.06,1.4,0,1.05,0,brass);
   const glass=new THREE.MeshPhysicalMaterial({color:'#c9dfcf',transparent:true,opacity:.12,roughness:.18,metalness:.05,side:THREE.DoubleSide,depthWrite:false});
   part(2.1,1.8,.008,0,.12,.67,glass);part(.008,1.8,1.3,-1.07,.12,0,glass);part(.008,1.8,1.3,1.07,.12,0,glass);
   camera.position.set(0,.22,4.5);targetPos.copy(camera.position);targetLook.set(0,0,0);setStatus('');}
  else{
   const v=reception?[[-1.6,1.55,7.85],[-1.6,1.10,6.1]]:(views[view]||views.hall);camera.position.set(...v[0]);look.set(...v[1]);targetPos.copy(camera.position);targetLook.copy(look);
   loader.load('/assets/museum.glb',g=>{if(disposed)return;model=g.scene;scene.add(model);model.traverse(o=>{if(o.isMesh){o.castShadow=true;o.receiveShadow=true;o.frustumCulled=true;const mats=Array.isArray(o.material)?o.material:[o.material];for(const m of mats){if(m.opacity<.1)o.visible=false;}}if(o.name.includes('Web_Dream')||o.name.includes('Web Dream'))moving.push({object:o,position:o.position.clone(),rotation:o.rotation.clone()});});setStatus('');},undefined,()=>{if(!disposed)setStatus('The display could not load. You can still use the gallery buttons below.');});
   loader.load('/assets/abraham.glb',g=>{if(disposed)return;hamster=g.scene;const box=new THREE.Box3().setFromObject(hamster);const size=box.getSize(new THREE.Vector3());const center=box.getCenter(new THREE.Vector3());const scale=1.2/size.y;hamster.scale.setScalar(scale);hamster.position.set(2.15-center.x*scale,.12-box.min.y*scale,.75-center.z*scale);if(reception)hamster.position.set(-1.6-center.x*scale,.42-box.min.y*scale,6.1-center.z*scale);hamster.rotation.y=reception?0:.22;hamster.traverse(o=>{o.userData.interaction_id='abraham';if(o.isMesh){o.castShadow=true;o.receiveShadow=true;}});scene.add(hamster);mixer=new THREE.AnimationMixer(hamster);patrol=createPatrol(hamster);for(const name of ['Face_Idle']){const clip=g.animations.find(c=>c.name===name);if(clip)mixer.clipAction(clip).play();}},undefined,()=>{});
  }
  const resize=()=>{const w=el.clientWidth,h=el.clientHeight;renderer.setSize(w,h);camera.aspect=w/h;camera.updateProjectionMatrix();};resize();const ro=new ResizeObserver(resize);ro.observe(el);
  const orbit=new OrbitControls(camera,renderer.domElement);
  orbit.enabled=!reception;orbit.target.copy(resultCode?new THREE.Vector3():look);orbit.enableDamping=false;orbit.dampingFactor=.09;
  orbit.minDistance=resultCode?1.5:.3;orbit.maxDistance=resultCode?7:32;orbit.maxPolarAngle=Math.PI*.49;orbit.minPolarAngle=.08;
  orbit.screenSpacePanning=false;orbit.zoomToCursor=false;orbit.panSpeed=.8;orbit.rotateSpeed=.65;
  orbit.enableRotate=!!resultCode;
  if(!resultCode){orbit.minPolarAngle=.2;orbit.maxPolarAngle=Math.PI-.2;}
  renderer.domElement.tabIndex=0;renderer.domElement.setAttribute('aria-label','Museum navigation. Drag to orbit, right-drag or two fingers to pan, pinch or scroll to zoom. Arrow keys pan.');

  const motion={active:false,current:null,baseSensor:null,baseCamera:null,rebase:false};
  const readOrientation=e=>{
   if(!motion.active)return;
   const screenAngle=window.screen?.orientation?.angle??window.orientation??0;
   const sensor=deviceLookQuaternion(THREE,e,screenAngle);if(!sensor)return;
   motion.current=sensor;
   if(!motion.baseSensor){motion.baseSensor=sensor.clone();motion.baseCamera=camera.quaternion.clone();}
  };
  window.addEventListener('deviceorientation',readOrientation,true);
  const raycaster=new THREE.Raycaster();let down=null;const pointers=new Set();let multi=false;
  let lookDrag=null;
  const pointerDown=e=>{pointers.add(e.pointerId);if(pointers.size>1){multi=true;lookDrag=null;}else{multi=false;down={x:e.clientX,y:e.clientY};if(!resultCode&&!reception&&!talkingRef.current&&!motion.active&&e.button===0)lookDrag={x:e.clientX,y:e.clientY};}renderer.domElement.focus({preventScroll:true});};
  const pointerMove=e=>{
   if(!lookDrag||multi||talkingRef.current)return;
   const dx=e.clientX-lookDrag.x,dy=e.clientY-lookDrag.y;lookDrag={x:e.clientX,y:e.clientY};
   const direction=orbit.target.clone().sub(camera.position),distance=direction.length();
   const spherical=new THREE.Spherical().setFromVector3(direction);
   spherical.theta-=dx*.0022;
   spherical.phi=THREE.MathUtils.clamp(spherical.phi-dy*.0022,.25,Math.PI-.25);
   orbit.target.copy(camera.position).add(new THREE.Vector3().setFromSpherical(spherical).setLength(distance));
   camera.lookAt(orbit.target);
  };
  renderer.domElement.addEventListener('pointermove',pointerMove);
  const endLook=()=>{lookDrag=null;};
  renderer.domElement.addEventListener('pointerup',endLook);
  renderer.domElement.addEventListener('pointercancel',endLook);
  const pointerUp=e=>{pointers.delete(e.pointerId);if(down&&!multi&&Math.hypot(e.clientX-down.x,e.clientY-down.y)<6){const rect=renderer.domElement.getBoundingClientRect();raycaster.setFromCamera(new THREE.Vector2((e.clientX-rect.left)/rect.width*2-1,-(e.clientY-rect.top)/rect.height*2+1),camera);const hit=raycaster.intersectObjects(scene.children,true).find(h=>h.object.visible&&h.object.userData.interaction_id);if(hit)callback.current(hit.object.userData.interaction_id);}down=null;};
  const cancel=e=>{pointers.delete(e.pointerId);down=null;};
  renderer.domElement.addEventListener('pointerdown',pointerDown);renderer.domElement.addEventListener('pointerup',pointerUp);renderer.domElement.addEventListener('pointercancel',cancel);
  const setView=v=>{const vv=views[v]||views.hall;camera.position.set(...vv[0]);orbit.target.set(...vv[1]);orbit.update();lastCamera.copy(camera.position);motion.baseSensor=null;motion.baseCamera=null;};
  const move=(x,z)=>{const forward=orbit.target.clone().sub(camera.position);forward.y=0;forward.normalize();const right=new THREE.Vector3().crossVectors(forward,camera.up).normalize();const offset=right.multiplyScalar(x).addScaledVector(forward,z);const destination=constrainMove(camera.position,camera.position.clone().add(offset));const actual=destination.clone().sub(camera.position);camera.position.copy(destination);orbit.target.add(actual);orbit.update();};
  const lastCamera=camera.position.clone();
  const clock=new THREE.Clock();let time=0;let conversationCamera=null;control.current={setView,move,zoom(factor){camera.position.sub(orbit.target).multiplyScalar(factor).add(orbit.target);orbit.update();},setMotion(active){motion.active=active;motion.current=null;motion.baseSensor=null;motion.baseCamera=null;motion.rebase=false;},events:discoveries};
  control.current.setMotion(motionEnabled);
  const tick=()=>{frame=requestAnimationFrame(tick);if(document.hidden)return;const dt=Math.min(clock.getDelta(),.05);if(!reduced){time+=dt;mixer?.update(dt);}if(!reception)patrol?.update(dt,reduced,talkingRef.current?camera.position:null);orbit.enabled=!reception&&!talkingRef.current;if(talkingRef.current&&hamster){
    if(motion.active)motion.rebase=true;
    if(!conversationCamera)conversationCamera={position:camera.position.clone(),target:orbit.target.clone()};
    const blend=reduced?1:1-Math.exp(-dt*4);
    camera.position.y=THREE.MathUtils.lerp(camera.position.y,1.05,blend);
    // Look below his face to place him in the clear upper part of the frame.
    const framing=new THREE.Vector3(hamster.position.x,.25,hamster.position.z);
    orbit.target.lerp(framing,blend);
   }else if(conversationCamera){camera.position.copy(conversationCamera.position);orbit.target.copy(conversationCamera.target);conversationCamera=null;}
   if(motion.active&&motion.current&&!talkingRef.current){
    if(motion.rebase||!motion.baseSensor){motion.baseSensor=motion.current.clone();motion.baseCamera=camera.quaternion.clone();motion.rebase=false;}
    const delta=motion.current.clone().multiply(motion.baseSensor.clone().invert());
    const cameraOrientation=delta.multiply(motion.baseCamera);
    const forward=new THREE.Vector3(0,0,-1).applyQuaternion(cameraOrientation).normalize();
    const distance=Math.max(.8,orbit.target.distanceTo(camera.position));
    orbit.target.copy(camera.position).addScaledVector(forward,distance);
   }
   orbit.update();
   if(hamster){if(reception){hamster.traverse(o=>{const index=o.morphTargetDictionary?.Mouth_Open;if(index!==undefined)o.morphTargetInfluences[index]=speech.current&&!reduced&&Math.sin(time*15)>.1?1:0;});}else if(thought.current){const head=hamster.getObjectByName('head');const point=new THREE.Vector3();(head||hamster).getWorldPosition(point);point.y+=.8;const ahead=point.clone().sub(camera.position).dot(camera.getWorldDirection(new THREE.Vector3()))>0;point.project(camera);const visible=ahead&&Math.abs(point.x)<.85&&Math.abs(point.y)<.8&&point.z<1&&(time%11)<5;thought.current.style.display=visible?'block':'none';thought.current.style.left=(point.x*.5+.5)*el.clientWidth+'px';thought.current.style.top=(-point.y*.5+.5)*el.clientHeight+'px';}}
   if(resultCode&&model&&!reduced){model.rotation.y=Math.sin(time*.35)*.22;model.position.y=Math.sin(time*1.1)*.045;}
   for(const {object:o,position:p,rotation:r} of moving){const n=o.name.toLowerCase();if(/label|leaf|fragment|mote/.test(n)&&!/cabinet/.test(n)&&!reduced)o.position.y=p.y+Math.sin(time*.7+p.x)*.055;if(/(?:hour|minute)_? ?hand/.test(n)&&!reduced)o.rotation.z=r.z+time*(n.includes('minute')?.8:.8/12);if(n.includes('sliding')&&n.includes('tray'))o.position.z=p.z+(control.current.events.includes('drawer')?-.4:0);}
   if(caseTitle){caseTitle.position.y=3.24+(reduced?0:Math.sin(time*.8)*.035);const glitch=!reduced&&time%4.7>4.35;caseTitle.position.x=glitch?Math.sin(time*80)*.035:0;caseTitle.material.opacity=glitch?.65+Math.abs(Math.sin(time*35))*.35:1;}
   if(!resultCode&&!reception){const safe=constrainMove(lastCamera,camera.position);orbit.target.add(safe.clone().sub(camera.position));camera.position.copy(safe);lastCamera.copy(safe);camera.lookAt(orbit.target);}
   doorSign?.update(time,reduced);
   details?.update(time,reduced);
   renderer.render(scene,camera);
  };tick();
  return()=>{disposed=true;window.removeEventListener('deviceorientation',readOrientation,true);renderer.domElement.removeEventListener('pointermove',pointerMove);renderer.domElement.removeEventListener('pointerup',endLook);renderer.domElement.removeEventListener('pointercancel',endLook);cancelAnimationFrame(frame);ro.disconnect();orbit.dispose();renderer.domElement.removeEventListener('pointerdown',pointerDown);renderer.domElement.removeEventListener('pointerup',pointerUp);renderer.domElement.removeEventListener('pointercancel',cancel);scene.traverse(o=>{o.geometry?.dispose();if(o.material)for(const m of (Array.isArray(o.material)?o.material:[o.material])){for(const v of Object.values(m))if(v?.isTexture)v.dispose();m.dispose();}});mixer?.stopAllAction();draco.dispose();renderer.dispose();el.replaceChildren();control.current=null;};
 },[resultCode,reduced,reception]);
 useEffect(()=>{if(!resultCode&&!reception)control.current?.setView(view);},[view,resultCode,reception]);
 useEffect(()=>{if(control.current)control.current.events=discoveries;},[discoveries]);
 return <div className={'museum-canvas '+(resultCode?'specimen-canvas':'')}><div className="webgl-host" ref={host} role="region" aria-label={resultCode?'Your specimen, gently floating above its plinth':'Interactive 3D natural history museum. Orbit, pan and zoom freely; gallery buttons are optional shortcuts.'}/>{!resultCode&&!reception&&<Joystick onMove={(x,z)=>control.current?.move(x,z)}/>}{motionAvailable&&!resultCode&&!reception&&<button className={'motion-look '+(motionEnabled?'active':'')} onClick={toggleMotion} aria-pressed={motionEnabled} aria-label={motionEnabled?'Turn off motion look':'Use phone motion to look around'}><span aria-hidden="true">◎</span><small>{motionEnabled?'TILT ON':'TILT'}</small></button>}{motionDenied&&<span className="motion-denied" role="status">Motion access is off</span>}{!resultCode&&!reception&&<div ref={thought} className="hamster-thought" style={{display:'none'}}>{thoughtText}<i/><b/></div>}{choice&&<div className="exhibit-preview"><span>DISPLAY NOTE</span><p>{choice}</p></div>}{status&&<div className="load-state" role="status">{status}</div>}</div>;
}
