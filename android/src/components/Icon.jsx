import React from 'react';
const icons={
 user:<><path d="M20 21v-2a7 7 0 0 0-14 0v2"/><circle cx="13" cy="7" r="4"/></>,
 lock:<><rect x="5" y="10" width="14" height="11" rx="3"/><path d="M8 10V7a4 4 0 0 1 8 0v3M12 14v3"/></>,
 eye:<><path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/></>,
 hide:<><path d="m3 3 18 18M10.5 5.1A12 12 0 0 1 22 12a16 16 0 0 1-3 4M6 6c-2.5 1.8-4 6-4 6s3.5 7 10 7a12 12 0 0 0 4-1"/></>,
 arrow:<path d="M4 12h16m-6-6 6 6-6 6"/>,back:<path d="m14 6-6 6 6 6"/>,
 telegram:<><path d="m21 3-5 18-5-8-8-4 18-6Z"/><path d="m11 13 5-5"/></>,
 grid:<><rect x="3" y="3" width="7" height="7" rx="2"/><rect x="14" y="3" width="7" height="7" rx="2"/><rect x="3" y="14" width="7" height="7" rx="2"/><rect x="14" y="14" width="7" height="7" rx="2"/></>,
 box:<><path d="m12 2 9 5v10l-9 5-9-5V7l9-5Z"/><path d="m3 7 9 5 9-5m-9 5v10M7.5 4.5l9 5"/></>,
 diamond:<><path d="m12 3 9 9-9 9-9-9 9-9Z"/><path d="M12 8v8m-4-4h8"/></>,
 settings:<><path d="m9 3-1 3-3 1-2 3 2 2-1 3 2 3 3-1 2 3h3l1-3 3-1 2-3-2-2 1-3-2-3-3 1-2-3H9Z"/><circle cx="12" cy="12" r="3"/></>,
 shield:<><path d="M12 3 3 7v5c0 5 9 9 9 9s9-4 9-9V7l-9-4Z"/><path d="m8 12 3 3 5-6"/></>,
 chevron:<path d="m9 5 7 7-7 7"/>,clock:<><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></>,
 devices:<><rect x="3" y="3" width="13" height="13" rx="3"/><path d="M8 21h8m-4-5v5"/><rect x="16" y="8" width="6" height="13" rx="2"/></>,
 logout:<><path d="M9 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h4m6-16 5 7-5 7M9 12h12"/></>,
 info:<><circle cx="12" cy="12" r="9"/><path d="M12 11v6m0-10h.01"/></>,
};
export function Icon({name,size=20,...rest}){return <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" {...rest}>{icons[name]||icons.info}</svg>}
