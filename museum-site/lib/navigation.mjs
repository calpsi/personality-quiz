// Floor plan in exported GLB coordinates, with clearance around walls and cases.
export function walkable(x,z){
 const inside=(Math.abs(x)<11.55&&z>-4.55&&z<4.55)||(Math.abs(x)<3.55&&z>-12.55&&z<4.55)||(Math.abs(x)<2.55&&z>=4.5&&z<8.5);
 if(!inside)return false;
 if(Math.abs(Math.abs(x)-4)<.45&&Math.abs(z)>1.05)return false;
 if(Math.abs(z+5)<.45&&Math.abs(x)>1.05)return false;
 if(Math.abs(z-5)<.45&&Math.abs(x)>1.05)return false;
 if(Math.abs(x)<1.65&&z>-2.35&&z<1.35)return false;
 return true;
}
export function constrainMove(from,to){
 const out=from.clone();const n=Math.max(1,Math.ceil(from.distanceTo(to)/.12));
 for(let i=1;i<=n;i++){const x=from.x+(to.x-from.x)*i/n,z=from.z+(to.z-from.z)*i/n;if(walkable(x,z)){out.x=x;out.z=z;}else break;}
 out.y=Math.max(.85,Math.min(2.5,to.y));return out;
}
export function routeTo(from,to){
 const step=.4,key=(x,z)=>`${x},${z}`;const start=[Math.round(from.x/step),Math.round(from.z/step)];
 const queue=[start],parents=new Map([[key(...start),null]]);let best=start,bestD=Infinity;
 for(let i=0;i<queue.length&&i<5000;i++){const p=queue[i],d=Math.hypot(p[0]*step-to.x,p[1]*step-to.z);if(d<bestD){bestD=d;best=p;}if(d<.3)break;
 for(const [dx,dz] of [[1,0],[-1,0],[0,1],[0,-1]]){const n=[p[0]+dx,p[1]+dz],k=key(...n);if(!parents.has(k)&&walkable(n[0]*step,n[1]*step)){parents.set(k,p);queue.push(n);}}}
 const path=[];let p=best;while(p&&parents.get(key(...p))){path.unshift([p[0]*step,p[1]*step]);p=parents.get(key(...p));}return path;
}
