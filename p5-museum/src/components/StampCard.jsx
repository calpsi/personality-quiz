'use client';
import {useState} from 'react';
import {questions} from '../lib/quiz.mjs';
const shortNames=['Fossil','Skeleton','Traces','Minerals','Meteorite','Two views','Habitat','Field kit'];
const drawings=[
 <path key="f" d="M43 42c-7 13-29 8-29-7 0-13 17-20 26-11 8 8 1 20-8 17-7-2-7-12-1-13 5-1 7 5 3 7M15 31l-6-3m10-5-4-6m12 3-1-7m9 7 3-6m4 13 7-1m-6 11 6 4"/>,
 <g key="s"><path d="M10 38c9-16 25-4 36-16l6 2-2 7-8 1M20 33l-5 15m19-15 6 15M24 30c-7 12 0 15 5 13m3-12c-4 8-1 11 4 10M12 37l-5 5"/><circle cx="47" cy="26" r="1"/></g>,
 <g key="t"><path d="M21 35c-12-3-12 10-3 10 8 0 12-8 3-10Zm20-14c-12-3-12 10-3 10 8 0 12-8 3-10Z"/><path d="m10 30-1-4m9 5 1-6m7 9 3-4m2-14-1-4m9 5 1-6m7 9 3-4"/></g>,
 <path key="m" d="m14 43-2-18 7-10 8 10-2 18Zm-2-18h15m-8-10v28m8 0V23l8-13 8 13v20m-16-20h16m-8-13v33m8 0 1-12 6-8 5 8-2 12M9 47h44"/>,
 <g key="r"><path d="m12 35 8-16 18-5 13 14-6 18-20 3Zm8-16 7 15-2 15m2-15 24-6M38 14l-3 15"/><path d="m8 13 7-5m29 0 5 5m4 37 5 3"/></g>,
 <g key="v"><path d="m9 38 3-16 10-5 9 12-6 15Zm24 2 2-17 11-6 8 13-6 16M12 22l13 22m10-21 13 23M7 49h22m4 1h23"/></g>,
 <g key="h"><path d="M10 45h42M17 43V25m0 9C6 35 7 23 17 25c-2-12 13-12 10-1 12 0 10 13-2 12M39 44V29m0 8c-10 0-9-9 0-8 0-12 13-10 10-1m-15 17 5-7 8 7"/></g>,
 <g key="k"><path d="M12 24h40v24H12Zm13 0v-8h14v8M12 32c10 5 30 5 40 0M27 32h10v8H27Z"/><path d="M17 43h5m21 0h4"/></g>
];
export function StampGraphic({number}){return <svg viewBox="0 0 64 64" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><circle cx="32" cy="32" r="29" strokeDasharray="2 3"/><circle cx="32" cy="32" r="26" strokeWidth=".7"/>{drawings[number-1]}</svg>;}
export default function StampCard({visit,onVisit,filter='hall'}){
 const [expanded,setExpanded]=useState(null);const count=Object.keys(visit.answers).length;
 const stops=questions.filter(q=>filter==='hall'||q.gallery===filter);const selected=stops.find(q=>q.id===expanded);
 return <section className="rally-card" aria-label="Museum stamp rally card"><div className="rally-heading"><div><span className="eyebrow">THE QUIET COLLECTION</span><h3>A record of your visit</h3></div><span className="rally-count"><b>{count}</b> / 8<br/><small>STAMPS</small></span></div><div className="rally-owner"><span>{visit.name||'Item-09'}</span><span>ADMIT ONE · KEEP THIS CARD</span></div><div className="stamp-grid">{stops.map(q=>{const done=!!visit.answers[q.id],open=expanded===q.id;return <button key={q.id} className={'stamp-slot '+(done?'stamped ':'')+(open?'stamp-open':'')} aria-expanded={open} aria-controls={'stamp-detail-'+filter.replaceAll(' ','-')} aria-label={`${q.number}. ${q.title}. ${done?'Stamped':'Not yet visited'}. ${open?'Collapse':'Expand'} details`} onClick={()=>setExpanded(open?null:q.id)}><span className="stamp-number">{String(q.number).padStart(2,'0')}</span><span className="stamp-print" style={{'--stamp-tilt':`${[-7,4,-3,6,-5,3,-6,5][q.number-1]}deg`}}><StampGraphic number={q.number}/>{done&&<span className="stamp-seal">VISITED</span>}</span><span className="stamp-label">{shortNames[q.number-1]}</span><span className="stamp-state">{done?'Collected':'Uncollected'}</span></button>;})}</div>{selected&&<div className="stamp-detail" id={'stamp-detail-'+filter.replaceAll(' ','-')}><div className="section-meta"><span>{selected.gallery}</span><button className="text-button" onClick={()=>setExpanded(null)}>Collapse −</button></div><h3>{selected.title}</h3><p>{selected.choices.find(c=>c.id===visit.answers[selected.id])?.text||'There’s a space here for your next discovery.'}</p><button className="primary" onClick={()=>onVisit(selected.id)}>{visit.answers[selected.id]?'Revisit / change my choice':'Visit this stop'}</button></div>}</section>;
}
