import * as THREE from 'three';
// Shared museum palette and deliberately visible, softly lit facets.
export function specimen(code){
 const g=new THREE.Group();g.name=`Specimen ${code}`;
 const material=(color,extra={})=>new THREE.MeshStandardMaterial({color,roughness:.83,flatShading:true,...extra});
 const ivory=material('#e5d4a7'),ochre=material('#ae7845'),dark=material('#65462e'),sage=material('#829181'),brass=material('#ad8b52',{metalness:.35,roughness:.55});
 const add=(geometry,m,p=[0,0,0])=>{const o=new THREE.Mesh(geometry,m);o.position.set(...p);o.castShadow=true;o.receiveShadow=true;g.add(o);return o;};
 const rod=(a,b,r,m=brass)=>{const av=new THREE.Vector3(...a),bv=new THREE.Vector3(...b),v=bv.clone().sub(av);const o=add(new THREE.CylinderGeometry(r*.8,r,v.length(),7),m);o.position.copy(av.add(bv).multiplyScalar(.5));o.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),v.normalize());return o;};
 const curve=(points,r,m)=>add(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(points.map(p=>new THREE.Vector3(...p))),48,r,6,false),m);
 // A small common mount, with the specimen itself above it.
 add(new THREE.CylinderGeometry(.42,.46,.055,24),dark,[0,-.68,0]);
 rod([0,-.66,0],[0,-.28,0],.018);
 if(code==='IC'){
  // Paper nautilus eggcase: thin, flared spiral with radial ribs and an open mouth.
  const vertices=[],indices=[];const n=110;
  for(let i=0;i<=n;i++){const t=i/n*Math.PI*2.05,r=.055+.57*Math.pow(i/n,1.35),w=.02+.16*i/n;for(const side of [-1,1])vertices.push(Math.cos(t)*r,Math.sin(t)*r+.08,side*w);}
  for(let i=0;i<n;i++){const k=i*2;indices.push(k,k+1,k+2,k+1,k+3,k+2);}
  const geo=new THREE.BufferGeometry();geo.setAttribute('position',new THREE.Float32BufferAttribute(vertices,3));geo.setIndex(indices);geo.computeVertexNormals();
  ivory.side=THREE.DoubleSide;add(geo,ivory);
  for(let i=15;i<=n;i+=3){const t=i/n*Math.PI*2.05,r=.055+.57*Math.pow(i/n,1.35),w=.02+.16*i/n;curve([[Math.cos(t)*r,Math.sin(t)*r+.08,-w],[Math.cos(t)*(r+.018),Math.sin(t)*(r+.018)+.08,0],[Math.cos(t)*r,Math.sin(t)*r+.08,w]],.008,ivory);}
 }else if(code==='CA'){
  // Caddisfly case: a hollow, tapered tube clad in collected twigs and pebbles.
  const tube=add(new THREE.CylinderGeometry(.14,.22,.95,12,1,true),dark,[0,.03,0]);tube.rotation.z=-.2;
  for(let i=0;i<65;i++){const t=i*2.399,y=(i/65-.5)*.9,r=.18-y*.07;const o=add(new THREE.IcosahedronGeometry(.055+(i%3)*.008,0),[ivory,ochre,sage,dark][i%4],[Math.cos(t)*r+y*.2,y+.03,Math.sin(t)*r]);o.scale.set(1,1.5,1);}
  for(let i=0;i<9;i++){const a=i*.7;rod([Math.cos(a)*.2,-.33,Math.sin(a)*.2],[Math.cos(a)*.17+.09,.35,Math.sin(a)*.17],.014,dark);}
 }else if(code==='AR'){
  // Sea bean: polished drift seed with a broad, dark equatorial band.
  const bean=add(new THREE.SphereGeometry(.48,24,12),ochre,[0,.05,0]);bean.scale.set(1,.72,.62);
  const band=add(new THREE.TorusGeometry(.463,.035,6,48),dark,[0,.05,0]);band.rotation.x=Math.PI/2;band.scale.set(1,.63,1);
  const seam=add(new THREE.TorusGeometry(.456,.009,5,48),ivory,[0,.085,0]);seam.rotation.x=Math.PI/2;seam.scale.set(1,.63,1);
 }else if(code==='CR'){
  // Glass sponge skeleton: open lattice basket, never an opaque solid tube.
  for(let j=0;j<12;j++){const pts=[];for(let i=0;i<=26;i++){const y=-.35+i/26*1.05,a=j/12*Math.PI*2+i/26*.4,r=.19+.09*i/26;pts.push([Math.cos(a)*r,y,Math.sin(a)*r]);}curve(pts,.009,ivory);}
  for(let j=0;j<15;j++){const r=.19+j/14*.09;const ring=add(new THREE.TorusGeometry(r,.009,5,24),ivory,[0,-.35+j/14*1.05,0]);ring.rotation.x=Math.PI/2;}
  for(const sign of [-1,1])for(let j=0;j<6;j++){const pts=[];for(let i=0;i<=40;i++){const t=i/40,r=.19+.09*t,a=j/6*Math.PI*2+sign*t*Math.PI*2;pts.push([Math.cos(a)*r,-.35+t*1.05,Math.sin(a)*r]);}curve(pts,.007,sage);}
 }else if(code==='IA'){
  // Fulgurite: irregular branching, hollow sand-glass tubes.
  const sand=material('#b49a70');
  const branch=(points,r)=>{const c=new THREE.CatmullRomCurve3(points.map(p=>new THREE.Vector3(...p)));add(new THREE.TubeGeometry(c,22,r,7,false),sand);const end=points.at(-1);add(new THREE.SphereGeometry(r*.75,8,6),dark,end);};
  branch([[0,-.4,0],[-.1,-.15,.02],[.02,.12,0],[-.04,.38,.03],[.1,.67,0]],.075);
  branch([[0,.08,0],[.2,.19,.02],[.31,.4,.03],[.45,.48,0]],.045);
  branch([[-.08,-.12,0],[-.28,.01,.03],[-.42,.22,0]],.04);
  for(let i=0;i<24;i++){const y=-.36+i/24*.95;add(new THREE.IcosahedronGeometry(.035,0),ochre,[Math.sin(i*3)*.08,y,Math.cos(i*3)*.065]);}
 }else if(code==='IR'){
  // Starling feather: asymmetric vanes, pale flecks and restrained iridescence.
  const feather=material('#354d48',{metalness:.3,roughness:.45}),purple=material('#5a515b',{metalness:.2});
  rod([-.12,-.52,0],[.12,.7,0],.012,ivory);
  for(let i=0;i<35;i++){const t=i/35,y=-.29+t*.95,x=-.08+t*.2,w=Math.sin(t*Math.PI)*.25;
   for(const side of [-1,1]){const pts=[new THREE.Vector3(x,y,0),new THREE.Vector3(x+side*w*(side===1?1:.73),y+.1,.015),new THREE.Vector3(x+.006,y+.038,.008)];const geo=new THREE.BufferGeometry().setFromPoints(pts);geo.computeVertexNormals();const m=i%4===0?purple:feather;m.side=THREE.DoubleSide;add(geo,m);if(i%4===0&&i>7)add(new THREE.SphereGeometry(.012,5,4),ivory,[x+side*w*.8,y+.08,.025]);}
  }
 }else{
  // Unresolved classifications remain explicitly unassigned, not an invented specimen.
  const tag=add(new THREE.BoxGeometry(.55,.72,.015),ivory,[0,.12,0]);tag.rotation.z=-.08;
  rod([-.18,.43,.02],[.18,.43,.02],.008,dark);
 }
 return g;
}
