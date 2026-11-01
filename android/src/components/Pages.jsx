import React from 'react';
import {Icon} from './Icon.jsx';
export function PageHeader({title,description}){return <header className="simple-header"><div><p className="section-eyebrow">NEMESIS PANEL</p><h1>{title}</h1>{description&&<p className="section-description">{description}</p>}</div><img className="small-emblem" src="/nemesis-mark.png" alt="" width="46" height="46"/></header>}
export function Future(){return <main className="page utility-page"><PageHeader title="Future feature"/><section className="reserved-card"><div className="reserved-icon"><Icon name="diamond" size={34}/></div><span className="mini-tag">TAB 03</span><h2>Room for what's next.</h2><p>This space is reserved for the functionality you specify later.</p><span className="quiet-pill">Reserved</span></section></main>}
