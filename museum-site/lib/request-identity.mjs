function hash(value){
  let result=2166136261;
  for(let index=0;index<value.length;index++){
    result^=value.charCodeAt(index);
    result=Math.imul(result,16777619);
  }
  return (result>>>0).toString(36);
}

export function publicVisitorId(headers){
  const forwarded=headers.get('x-forwarded-for')?.split(',')[0]?.trim()||'unknown';
  const agent=headers.get('user-agent')?.slice(0,160)||'unknown';
  return `web-${hash(`${forwarded}|${agent}`)}`;
}

export function isSameSiteRequest(request){
  const ownOrigin=new URL(request.url).origin;
  const origin=request.headers.get('origin');
  const fetchSite=request.headers.get('sec-fetch-site');
  return (!origin||origin===ownOrigin)&&(!fetchSite||fetchSite==='same-origin'||fetchSite==='none');
}
