const fallbackDirection=[0,0,-1];

export function neutralLookDirection(position,target){
  const direction=target.map((value,index)=>value-position[index]);
  const length=Math.hypot(...direction);
  return length>.000001?direction.map(value=>value/length):[...fallbackDirection];
}

export function recenteredLookTarget(position,currentTarget,direction,minDistance=.8){
  const distance=Math.max(minDistance,Math.hypot(...currentTarget.map((value,index)=>value-position[index])));
  return position.map((value,index)=>value+direction[index]*distance);
}
