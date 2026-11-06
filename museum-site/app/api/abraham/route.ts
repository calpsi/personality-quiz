import {respond,validBody} from '@/lib/abraham.mjs';
import {getChatGPTUser} from '@/app/chatgpt-auth';
import {isSameSiteRequest,publicVisitorId} from '@/lib/request-identity.mjs';
export const dynamic='force-dynamic';
const windows=new Map<string,{count:number,reset:number}>();
const previewOrigin='https://preview.p5js.org';
function corsHeaders(){
  return {'Access-Control-Allow-Origin':previewOrigin,'Vary':'Origin'};
}
export function OPTIONS(request:Request){
  if(request.headers.get('origin')!==previewOrigin)return new Response(null,{status:403});
  return new Response(null,{status:204,headers:{...corsHeaders(),'Access-Control-Allow-Methods':'POST','Access-Control-Allow-Headers':'Content-Type, X-Museum-Pass, X-Abraham-Key'}});
}
export async function POST(request:Request){
  if(request.headers.get('origin')===previewOrigin){
    const headers=corsHeaders();
    const browserKey=request.headers.get('x-abraham-key')?.trim();
    if(browserKey){
      if(browserKey.length>512)return Response.json({error:'That museum key could not be read.'},{status:400,headers});
      const response=await conversation(request,`p5-${browserKey.slice(-12)}`,browserKey);
      for(const [name,value] of Object.entries(headers))response.headers.set(name,value);
      return response;
    }
    const pass=process.env.MUSEUM_TEST_PASS;
    if(!pass||request.headers.get('x-museum-pass')!==pass)return Response.json({error:'A museum testing pass is required.'},{status:401,headers});
    const response=await conversation(request,'p5-test');
    for(const [name,value] of Object.entries(headers))response.headers.set(name,value);
    return response;
  }
  if(!isSameSiteRequest(request))return Response.json({error:'This conversation belongs to the museum.'},{status:403});
  const user=await getChatGPTUser();
  const isLocal=['localhost','127.0.0.1'].includes(new URL(request.url).hostname);
  return conversation(request,user?.userId||(isLocal?'local':publicVisitorId(request.headers)));
}
async function conversation(request:Request,id:string,keyOverride?:string){
  const now=Date.now();
  for(const [key,value] of windows)if(value.reset<now)windows.delete(key);
  const window=windows.get(id)||{count:0,reset:now+60000};
  if(window.count>=8)return Response.json({error:'Give Abraham a moment, then try again.'},{status:429,headers:{'Retry-After':'60'}});
  window.count++;windows.set(id,window);
  if(!request.headers.get('content-type')?.includes('application/json'))return Response.json({error:'Expected JSON.'},{status:415});
  let body;
  try{const reader=request.body?.getReader();if(!reader)throw Error();let size=0;const chunks=[];while(true){const {done,value}=await reader.read();if(done)break;size+=value.byteLength;if(size>20000){await reader.cancel();return Response.json({error:'This message is too long.'},{status:413});}chunks.push(value);}const bytes=new Uint8Array(size);let offset=0;for(const c of chunks){bytes.set(c,offset);offset+=c.length;}body=JSON.parse(new TextDecoder().decode(bytes));}catch{return Response.json({error:'Could not read that message.'},{status:400});}
  if(!validBody(body))return Response.json({error:'Please enter a message of up to 600 characters.'},{status:400});
  const result=await respond(body,{key:keyOverride||process.env.OPENAI_API_KEY,model:keyOverride?'gpt-4.1-mini':process.env.OPENAI_MODEL||'gpt-6-luna'});
  return Response.json(result,{headers:{'Cache-Control':'no-store'}});
}
