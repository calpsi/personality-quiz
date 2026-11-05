import questions from './questions.json' with { type: 'json' };
import copy from './copy.json' with { type: 'json' };
export { questions, copy };
export const dimensions = ['I','C','A','R'];
const pairs=['IC','IA','IR','CA','CR','AR'];
export const concerns={I:'understanding',C:'continuity',A:'room to act',R:'shared participation'};
export function records(answers={}) {
  return questions.flatMap(q=>{ const c=q.choices.find(c=>c.id===answers[q.id]); return c?[{...c,questionId:q.id,title:q.title,gallery:q.gallery}]:[]; });
}
export function scoreVisit(answers={}, finalChoice='none') {
  const entries=records(answers), scores={I:0,C:0,A:0,R:0}, support={I:0,C:0,A:0,R:0};
  for(const e of entries)for(const [d,n] of Object.entries(e.score)){scores[d]+=n;support[d]++;}
  let code='MX';
  if(entries.length<8) return {complete:false,code:null,scores,support,entries};
  const max=Math.max(...pairs.map(p=>scores[p[0]]+scores[p[1]]));
  let candidates=pairs.filter(p=>scores[p[0]]+scores[p[1]]===max);
  if(candidates.length>1 && support[finalChoice]>=2){const narrowed=candidates.filter(p=>p.includes(finalChoice));if(narrowed.length===1)candidates=narrowed;}
  if(candidates.length===1 && [...candidates[0]].every(d=>support[d]>=2))code=candidates[0];
  const ranked=[...dimensions].sort((a,b)=>scores[b]-scores[a]);
  const leading=scores[ranked[0]]-scores[ranked[1]]>=4?ranked[0]:null;
  const evidence=[];
  if(code!=='MX')for(const d of code){const e=entries.find(e=>e.score[d]===2&&!evidence.includes(e));if(e)evidence.push(e);}
  const other=entries.find(e=>!evidence.some(v=>v.gallery===e.gallery));if(other&&!evidence.includes(other))evidence.push(other);
  for(const e of entries)if(evidence.length<3&&!evidence.includes(e))evidence.push(e);
  const contrary=code==='MX'?null:entries.find(e=>!evidence.includes(e)&&Object.entries(e.score).some(([d,n])=>n===2&&!code.includes(d)));
  return {complete:true,code,scores,support,entries,evidence:evidence.slice(0,3),contrary,leading,close:code!=='MX'&&scores[ranked[1]]-scores[ranked[2]]===1,third:ranked[2]};
}
export function profileFor(result) {
  const prefix=`VISIT-${result.code||'MX'}`;
  const get=s=>copy[`${prefix}-${s}`]||'';
  return {name:get('TITLE'),code:prefix,intro:(result.leading&&get(`${result.leading}-LEADING`))||get('BALANCED-INTRO')||get('INTRO'),pattern:get('PATTERN')||get('CONTEXT'),strength:get('STRENGTHS')||get('STRENGTH'),tension:get('TENSION'),complement:get('COMPLEMENT'),friction:get('FRICTION'),closing:get('CLOSING'),label:get('LABEL'),share:get('SHARE')};
}
export const discoveryLabels={clock:'touched the backwards clock',drawer:'opened the drawer of stars',labels:'straightened the floating labels',meteorite:'looked beneath the hovering meteorite',leaves:'gathered the drifting leaves'};
export function fallbackRemark(visit) {
  const result=scoreVisit(visit.answers,visit.finalChoice), profile=profileFor(result);
  const event=(visit.discoveries||[]).find(id=>discoveryLabels[id]);
  const memory=event?`You ${discoveryLabels[event]}, didn't you? `:result.entries.length?`You chose “${result.entries[result.entries.length-1].text}” at ${result.entries[result.entries.length-1].title.toLowerCase()}. `:'';
  const said=(visit.messages||[]).filter(m=>m.role==='user').at(-1);
  const quote=said?`And you told me, “${said.content.slice(0,150)}${said.content.length>150?'…':''}” I'll keep that with your ticket. `:'';
  return `${result.complete?`Here we are! ${profile.name}. `:'Oh, hello! '}${memory}${quote}${event==='drawer'?'Do check your sleeves before you go.':"I'm glad you came to have a look."}`;
}
export function fallbackChat(message) {
  const s=message.toLowerCase();
  if(/clock|backward/.test(s))return copy['AB-DREAM-01'];
  if(/star|drawer/.test(s))return copy['AB-DREAM-02'];
  if(/creep|scary|afraid/.test(s))return copy['AB-DREAM-03'];
  if(/label|float/.test(s))return copy['AB-DREAM-04'];
  if(/where|lost/.test(s))return copy['AB-HELP-02'];
  if(/how|quiz|appraisal/.test(s))return copy['AB-HELP-01'];
  if(/\bai\b|robot/.test(s))return copy['AB-HELP-09'];
  return "Oh! Sorry, I got distracted by a label moving again. What were you asking?";
}
export function newVisit(){return {version:1,name:'',answers:{},finalChoice:'none',reflection:'',discoveries:[],messages:[],finished:false,seed:Math.floor(Math.random()*2147483647)};}
export function restoreVisit(raw){
  if(!raw||raw.version!==1)return null;
  const v=newVisit();v.answers=Object.fromEntries(records(raw.answers).map(e=>[e.questionId,e.id]));
  v.name=typeof raw.name==='string'?raw.name.slice(0,40):'';v.finalChoice=[...dimensions,'none'].includes(raw.finalChoice)?raw.finalChoice:'none';
  v.reflection=typeof raw.reflection==='string'?raw.reflection.slice(0,200):'';
  v.discoveries=Array.isArray(raw.discoveries)?[...new Set(raw.discoveries.filter(id=>id in discoveryLabels))]:[];
  v.messages=Array.isArray(raw.messages)?raw.messages.filter(m=>m&&['user','assistant'].includes(m.role)&&typeof m.content==='string').slice(-20).map(m=>({role:m.role,content:m.content.slice(0,700)})):[];
  v.finished=raw.finished===true&&Object.keys(v.answers).length===8;v.seed=Number.isInteger(raw.seed)?raw.seed:v.seed;return v;
}
export function shuffledChoices(q,seed){
  let x=(seed+q.number*104729)>>>0;const a=[...q.choices];
  for(let i=a.length-1;i>0;i--){x=(Math.imul(x,1664525)+1013904223)>>>0;const j=x%(i+1);[a[i],a[j]]=[a[j],a[i]];}return a;
}
