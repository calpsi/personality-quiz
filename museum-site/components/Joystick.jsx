import {useRef,useState,useEffect} from 'react';
export default function Joystick({onMove}){
 const [offset,setOffset]=useState([0,0]);const held=useRef(false),value=useRef([0,0]),smooth=useRef([0,0]),move=useRef(onMove);move.current=onMove;
 useEffect(()=>{let id,last=performance.now();const tick=t=>{const dt=Math.min((t-last)/1000,.05);last=t;const target=held.current?value.current:[0,0],blend=1-Math.exp(-dt*14);smooth.current[0]+=(target[0]-smooth.current[0])*blend;smooth.current[1]+=(target[1]-smooth.current[1])*blend;if(Math.hypot(...smooth.current)>.008)move.current(smooth.current[0]*dt*3.25,-smooth.current[1]*dt*3.25);id=requestAnimationFrame(tick);};id=requestAnimationFrame(tick);return()=>cancelAnimationFrame(id);},[]);
 const update=e=>{const r=e.currentTarget.getBoundingClientRect();let x=(e.clientX-r.left-r.width/2)/30,y=(e.clientY-r.top-r.height/2)/30;const n=Math.max(1,Math.hypot(x,y));x/=n;y/=n;value.current=[x,y];setOffset([x*26,y*26]);};
 const release=()=>{held.current=false;value.current=[0,0];setOffset([0,0]);};
 return <div className="joystick" role="group" aria-label="Movement joystick" tabIndex={0} onKeyDown={e=>{const d={ArrowUp:[0,.2],ArrowDown:[0,-.2],ArrowLeft:[-.2,0],ArrowRight:[.2,0]}[e.key];if(d){e.preventDefault();move.current(...d);}}} onPointerDown={e=>{held.current=true;e.currentTarget.setPointerCapture(e.pointerId);update(e);}} onPointerMove={e=>{if(held.current)update(e);}} onPointerUp={release} onPointerCancel={release} onLostPointerCapture={release}><span style={{transform:`translate(${offset[0]}px,${offset[1]}px)`}}/></div>;
}
