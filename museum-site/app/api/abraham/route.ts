import {respond,validBody} from '@/lib/abraham.mjs';
import {getChatGPTUser} from '@/app/chatgpt-auth';
export const dynamic='force-dynamic';
const windows=new Map<string,{count:number,reset:number}>();
export async function POST(request:Request){
  const origin=request.headers.get('origin');
  if(origin && origin!==new URL(request.url).origin)return Response.json({error:'This conversation belongs to the museum.'},{status:403});
  // Private Sites provides the authenticated visitor identity. No anonymous paid endpoint.
  const user=await getChatGPTUser();
  const isLocal=['localhost','127.0.0.1'].includes(new URL(request.url).hostname);
  if(!user&&!isLocal)return Response.json({error:'Please sign in to talk to Abraham.'},{status:401});
  const id=user?.userId||'local';const now=Date.now();
  for(const [key,value] of windows)if(value.reset<now)windows.delete(key);
  const window=windows.get(id)||{count:0,reset:now+60000};
  if(window.count>=8)return Response.json({error:'Give Abraham a moment, then try again.'},{status:429,headers:{'Retry-After':'60'}});
  window.count++;windows.set(id,window);
  if(!request.headers.get('content-type')?.includes('application/json'))return Response.json({error:'Expected JSON.'},{status:415});
  let body;
  try{const reader=request.body?.getReader();if(!reader)throw Error();let size=0;const chunks=[];while(true){const {done,value}=await reader.read();if(done)break;size+=value.byteLength;if(size>20000){await reader.cancel();return Response.json({error:'This message is too long.'},{status:413});}chunks.push(value);}const bytes=new Uint8Array(size);let offset=0;for(const c of chunks){bytes.set(c,offset);offset+=c.length;}body=JSON.parse(new TextDecoder().decode(bytes));}catch{return Response.json({error:'Could not read that message.'},{status:400});}
  if(!validBody(body))return Response.json({error:'Please enter a message of up to 600 characters.'},{status:400});
  const result=await respond(body,{key:process.env.OPENAI_API_KEY,model:process.env.OPENAI_MODEL||'gpt-6-luna'});
  return Response.json(result,{headers:{'Cache-Control':'no-store'}});
}
