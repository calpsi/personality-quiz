export default function MuseumTool({kind}) {
 return <svg viewBox="0 0 48 48" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
  {kind==='card'?<><path fill="#f6e7b5" d="m12 8 26 3-3 30-26-3Z"/><path d="m16 17 15 2M15 22l8 1"/><circle cx="27" cy="31" r="6" fill="#a5b58b"/><path d="m24 31 2 2 4-4M12 8l3-4 26 3-3 30"/></>:kind==='map'?<><path fill="#f6e7b5" d="m5 13 12-5 14 5 12-5v28l-12 5-14-5-12 5Z"/><path d="M17 8v28m14-23v28"/><path stroke="#a37246" strokeDasharray="2 4" d="M10 29c4-18 20 11 27-9"/><path d="m34 17 6 6m0-6-6 6"/></>:<><path fill="#afbc91" d="m24 5 4 6 7-1 2 7 6 4-3 7 1 7-7 2-5 6-6-4-8 1-2-7-6-5 4-6-1-8 7-2Z"/><circle cx="24" cy="24" r="8" fill="#f6e7b5"/><circle cx="24" cy="24" r="3"/></>}
 </svg>;
}
