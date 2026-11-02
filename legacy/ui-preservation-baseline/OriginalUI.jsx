// Derived render expressions only. Original business logic is not bundled.
import React from 'react';
import * as r from 'react/jsx-runtime';
import * as jt from 'react';
import {uh,eh,I0,ch,Wl,tp,ap,lp,sp,$l,cp,fp,hp,pp,gp,ys,xp,Sp,Ap,gs,jp,oh,fh,dh,kp,Rp,bs,nl,hh} from './icons.js';
function NotIntegrated(){return r.jsx('p',{className:'integration-note',children:'This feature requires an approved authenticated backend.'})} const Zu=NotIntegrated,f1=NotIntegrated,d1=NotIntegrated;
function h1({
    message: A,
    onDismiss: tt
}) {
    return r.jsxs("div", {
        className: "flex items-start gap-3 px-4 py-3 bg-red-950/40 border border-red-900/30 rounded-xl mx-6 mt-3",
        children: [r.jsx(kp, {
            className: "w-4 h-4 text-red-400 flex-shrink-0 mt-0.5"
        }), r.jsx("p", {
            className: "text-xs text-red-300 flex-1 leading-relaxed",
            children: A
        }), r.jsx("button", {
            onClick: tt,
            className: "text-red-600 hover:text-red-400 flex-shrink-0",
            children: r.jsx(nl, {
                className: "w-3.5 h-3.5"
            })
        })]
    })
}
function m1() {
    return r.jsxs("div", {
        className: "bg-[#111111] border border-[#1f1f1f] rounded-2xl p-4 animate-pulse",
        children: [r.jsxs("div", {
            className: "flex items-start gap-3 mb-3",
            children: [r.jsx("div", {
                className: "w-10 h-10 rounded-xl bg-[#1a1a1a]"
            }), r.jsxs("div", {
                className: "flex-1 space-y-2",
                children: [r.jsx("div", {
                    className: "h-3 bg-[#1a1a1a] rounded w-3/4"
                }), r.jsx("div", {
                    className: "h-2 bg-[#151515] rounded w-1/2"
                })]
            })]
        }), r.jsxs("div", {
            className: "grid grid-cols-2 gap-3 mb-3",
            children: [r.jsx("div", {
                className: "h-8 bg-[#151515] rounded-xl"
            }), r.jsx("div", {
                className: "h-8 bg-[#151515] rounded-xl"
            })]
        }), r.jsx("div", {
            className: "h-10 bg-[#131313] rounded-xl"
        })]
    })
}
export function OriginalAccounts(){
const [tt, b] = jt.useState([]), [d, S] = jt.useState(!1), [f, p] = jt.useState(""), [h, o] = jt.useState(""), [x, T] = jt.useState(""), [w, C] = jt.useState(!1), [v, E] = jt.useState(""), [g, z] = jt.useState(!1), [N, k] = jt.useState(!1), [M, H] = jt.useState(""), [L, nt] = jt.useState(null), [V, ot] = jt.useState(""), [mSel, setMSel] = jt.useState(new Set), $ = jt.useRef(null);
const blocked=()=>T('Unavailable in this offline development build. Do not enter production secrets.');
const at=blocked,c=blocked,I=blocked,Z=blocked,openMerged=blocked,toggleSel=blocked;
const yn=async()=>{throw new Error('Live Firebase access is unavailable in offline development mode')},nh=()=>{},A=blocked;
const it=e=>{e.target.value='';H('APK inspection is awaiting a secure integration. No file has been read or uploaded.')};
const bt=e=>{e.preventDefault();H('APK inspection is awaiting a secure integration. No file has been read or uploaded.')};
const y=()=>{nt(null);H('');ot('')};
return r.jsxs("div", {
        className: "min-h-screen flex items-center justify-center relative overflow-hidden",
        style: {
            background: "transparent"
        },
        children: [r.jsxs("div", {
            className: "relative z-10 w-full max-w-md px-4 py-8",
            children: [r.jsxs("div", {
                className: "text-center mb-8",
                children: [r.jsx("div", {
                    className: "nemesis-splash-logo-circle",
                    children: r.jsxs(r.Fragment, {
                        children: [
                            r.jsx("span", { className: "flake-tiny", style: { top: "10%", left: "15%" }, children: "\u2744" }),
                            r.jsx("span", { className: "flake-tiny", style: { top: "8%", right: "15%", animationDelay: "0.6s" }, children: "\u2744" }),
                            r.jsx("span", { className: "flake-tiny", style: { bottom: "12%", left: "20%", animationDelay: "1.2s" }, children: "\u2744" }),
                            r.jsx("span", { className: "flake-tiny", style: { bottom: "10%", right: "18%", animationDelay: "1.8s" }, children: "\u2726" }),
                            r.jsxs("svg", {
                                    viewBox: "0 0 90 72",
                                    fill: "none",
                                    xmlns: "http://www.w3.org/2000/svg",
                                    className: "nmx-animated-svg",
                                    children: [
                                        r.jsxs("defs", {
                                            children: [
                                                r.jsxs("linearGradient", {
                                                    id: "nmx-splash-grad",
                                                    x1: "0", y1: "0", x2: "90", y2: "72",
                                                    gradientUnits: "userSpaceOnUse",
                                                    children: [
                                                        r.jsx("stop", { offset: "0%", stopColor: "#ff1744" }),
                                                        r.jsx("stop", { offset: "45%", stopColor: "#ff4081" }),
                                                        r.jsx("stop", { offset: "100%", stopColor: "#ffa000" })
                                                    ]
                                                }),
                                                r.jsxs("linearGradient", {
                                                    id: "nmx-splash-ring",
                                                    x1: "0", y1: "0", x2: "90", y2: "72",
                                                    gradientUnits: "userSpaceOnUse",
                                                    children: [
                                                        r.jsx("stop", { offset: "0%", stopColor: "#ff1744" }),
                                                        r.jsx("stop", { offset: "50%", stopColor: "#d946ef" }),
                                                        r.jsx("stop", { offset: "100%", stopColor: "#ff9100" })
                                                    ]
                                                })
                                            ]
                                        }),
                                        r.jsx("circle", {
                                            cx: "45", cy: "36", r: "33",
                                            stroke: "url(#nmx-splash-ring)",
                                            strokeWidth: "1.8",
                                            strokeDasharray: "14 9",
                                            strokeLinecap: "round",
                                            className: "nmx-spin-ring",
                                            opacity: "0.9"
                                        }),
                                        r.jsx("circle", {
                                            cx: "45", cy: "36", r: "28",
                                            stroke: "rgba(255, 50, 100, 0.35)",
                                            strokeWidth: "1",
                                            strokeDasharray: "4 4",
                                            className: "nmx-spin-reverse"
                                        }),
                                        r.jsx("path", {
                                            d: "M 33 21 C 30 13 24 8 18 5 C 22 12 25 17 29 23 Z",
                                            fill: "url(#nmx-splash-grad)",
                                            className: "nmx-horn-l"
                                        }),
                                        r.jsx("path", {
                                            d: "M 57 21 C 60 13 66 8 72 5 C 68 12 65 17 61 23 Z",
                                            fill: "url(#nmx-splash-grad)",
                                            className: "nmx-horn-r"
                                        }),
                                        r.jsx("polygon", {
                                            points: "45,12 42,19 48,19",
                                            fill: "#ffa000"
                                        }),
                                        r.jsx("text", {
                                            x: "45", y: "47",
                                            textAnchor: "middle",
                                            fill: "url(#nmx-splash-grad)",
                                            className: "nmx-text-glow",
                                            style: {
                                                fontFamily: "'Outfit', 'Inter', sans-serif",
                                                fontWeight: "900",
                                                fontSize: "24px",
                                                letterSpacing: "2.5px"
                                            },
                                            children: "NMX"
                                        }),
                                        r.jsx("path", {
                                            d: "M 16 54 L 38 54 L 42 58 L 48 58 L 52 54 L 74 54",
                                            stroke: "url(#nmx-splash-grad)",
                                            strokeWidth: "2",
                                            strokeLinecap: "round",
                                            strokeLinejoin: "round"
                                        }),
                                        r.jsx("polygon", {
                                            points: "45,55 48,58 45,61 42,58",
                                            fill: "#ffea00",
                                            className: "nmx-core-diamond"
                                        })
                                    ]
                                })
                        ]
                    })
                }), r.jsx("style", {
                    jsx: !0,
                    children: `.nemesis-splash-logo-circle{width:84px;height:84px;margin:0 auto 16px;border-radius:50%;background:radial-gradient(ellipse at 40% 30%,#360814 0%,#180309 50%,#090104 100%);border:1.5px solid rgba(255,60,110,0.45);box-shadow:0 0 18px rgba(255,30,80,0.45),0 0 36px rgba(180,0,50,0.25);display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden;flex-shrink:0;animation:abSplashLogoGlow 3s ease-in-out infinite}@keyframes abSplashLogoGlow{0%,100%{box-shadow:0 0 18px rgba(255,30,80,0.45),0 0 36px rgba(180,0,50,0.25)}50%{box-shadow:0 0 28px rgba(255,60,110,0.7),0 0 50px rgba(255,30,80,0.4)}}.nemesis-splash-logo-circle .flake-tiny{position:absolute;color:rgba(255,180,100,0.7);font-size:9px;animation:abSplashTwinkle 3s ease-in-out infinite;pointer-events:none}@keyframes abSplashTwinkle{0%,100%{opacity:0.3;transform:scale(1)}50%{opacity:1;transform:scale(1.4)}}.nemesis-splash-logo-circle svg{width:64px;height:52px;position:relative;z-index:1}`
                }), r.jsxs("div", {
                    className: "flex flex-col items-center justify-center mt-10",
                    children: [r.jsxs("h1", {
                        className: "relative text-4xl sm:text-5xl font-black tracking-wider uppercase opacity-0 animate-fade-in text-center",
                        children: [r.jsx("span", {
                            className: "nemesis-title-gradient",
                            children: "NEMESIS "
                        }), r.jsxs("span", {
                            className: "relative text-white font-black",
                            children: ["PANEL", r.jsx("span", {
                                className: "absolute -top-1 -right-3 w-3 h-3 bg-red-500 rounded-full animate-glint shadow-[0_0_14px_#ff1744]"
                            })]
                        })]
                    }), r.jsx("p", {
                        className: "text-sm text-muted-foreground mt-2 opacity-0 animate-fade-in delay-300",
                        children: "NEMESIS - Next-Gen Console"
                    }), r.jsx("style", {
                        jsx: !0,
                        children: `
    @keyframes fadeIn {
      0% { opacity: 0; transform: translateY(10px) scale(0.98); filter: blur(2px); }
      100% { opacity: 1; transform: translateY(0) scale(1); filter: blur(0); }
    }
    .animate-fade-in { animation: fadeIn 1s ease-out forwards; }
    @keyframes glint {
      0%, 100% { transform: scale(1); opacity: 0; }
      50% { transform: scale(1.5); opacity: 1; }
    }
    .animate-glint {
      animation: glint 1.5s infinite;
      box-shadow: 0 0 6px #6acfff, 0 0 10px #0088cc;
    }
    h1 { font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif; }
  `
                    })]
                }), r.jsx("p", {
                    className: "text-sm text-muted-foreground mt-2"
                })]
            }), r.jsxs("div", {
                className: "glass-card rounded-3xl p-7 shadow-2xl shadow-black/60",
                children: [!d && r.jsxs(r.Fragment, {
                    children: [r.jsxs("div", {
                        className: "flex items-center justify-between mb-4",
                        children: [r.jsxs("div", {
                            className: "flex items-center gap-2",
                            children: [r.jsx(bs, {
                                className: "w-4 h-4 text-muted-foreground"
                            }), r.jsx("span", {
                                className: "text-sm font-semibold text-foreground",
                                children: "Saved Accounts"
                            })]
                        }), r.jsxs("span", {
                            className: "text-xs text-muted-foreground bg-accent px-2 py-1 rounded-full",
                            children: [tt.length, " ", tt.length === 1 ? "account" : "accounts"]
                        })]
                    }), r.jsx("div", {
                        className: "space-y-2 max-h-52 overflow-y-auto pr-1 mb-4",
                        children: tt.length === 0 ? r.jsxs("div", {
                            className: "text-center py-8 text-muted-foreground text-sm",
                            children: [r.jsx(bs, {
                                className: "w-8 h-8 mx-auto mb-2 opacity-30"
                            }), "No saved accounts"]
                        }) : tt.map(_ => r.jsxs("div", {
                            onClick: () => !w && at(_),
                            className: "flex items-center gap-3 p-3 rounded-xl border border-border hover:border-red-600/40 hover:bg-red-950/20 cursor-pointer transition-all duration-200 group",
                            children: [r.jsx("button", {
                                onClick: X => toggleSel(_.id, X),
                                title: mSel.has(_.id) ? "Remove from merge selection" : "Select for merged open",
                                className: `w-5 h-5 rounded-md border flex items-center justify-center flex-shrink-0 transition-all ${mSel.has(_.id)?"bg-blue-600 border-blue-500":"border-border bg-transparent hover:border-blue-500/60"}`,
                                children: mSel.has(_.id) && r.jsx("svg", {
                                    viewBox: "0 0 24 24",
                                    width: "12",
                                    height: "12",
                                    fill: "none",
                                    stroke: "white",
                                    strokeWidth: "3",
                                    strokeLinecap: "round",
                                    strokeLinejoin: "round",
                                    children: r.jsx("polyline", {
                                        points: "20 6 9 17 4 12"
                                    })
                                })
                            }), r.jsxs("div", {
                                className: "flex-1 min-w-0",
                                children: [r.jsx("p", {
                                    className: "text-sm font-semibold text-foreground truncate",
                                    children: _.url
                                }), r.jsxs("p", {
                                    className: "text-xs text-muted-foreground mt-0.5 font-mono",
                                    children: [_.date, " · ", _.key.substring(0, 20), "…"]
                                })]
                            }), r.jsxs("div", {
                                className: "flex items-center gap-2",
                                children: [r.jsx("button", {
                                    onClick: X => c(_, X),
                                    className: "p-1.5 rounded-lg bg-blue-950/60 border border-blue-900/40 text-blue-400 hover:bg-blue-900/60 transition-all",
                                    title: "Share connection link",
                                    children: r.jsx(Ap, {
                                        className: "w-3 h-3"
                                    })
                                }), r.jsx("button", {
                                    onClick: X => Z(_.id, X),
                                    className: "p-1.5 rounded-lg bg-red-950/60 border border-red-900/40 text-red-400 hover:bg-red-900/60 transition-all",
                                    children: r.jsx(oh, {
                                        className: "w-3 h-3"
                                    })
                                }), r.jsx(eh, {
                                    className: "w-4 h-4 text-muted-foreground group-hover:text-red-400 transition-colors"
                                })]
                            })]
                        }, _.id))
                    }), mSel.size > 0 && r.jsxs("button", {
                        onClick: () => setMSel(mSel.size === tt.length ? new Set : new Set(tt.map(a => a.id))),
                        className: "w-full flex items-center justify-center gap-2 py-2.5 mb-2 rounded-lg bg-slate-600/20 border border-slate-600/40 text-slate-300 hover:bg-slate-600/30 transition-all text-xs font-medium",
                        children: [mSel.size === tt.length ? "Deselect All" : `Select All (${tt.length})`]
                    }), mSel.size > 0 && r.jsxs("div", {
                        className: "flex gap-2 mb-2",
                        children: [r.jsx("button", {
                            onClick: openMerged,
                            className: "flex-1 flex items-center justify-center gap-2 py-3 rounded-xl bg-blue-600/20 border border-blue-600/40 text-blue-400 hover:bg-blue-600/30 transition-all text-sm font-semibold",
                            children: [`Open ${mSel.size} Account${mSel.size===1?"":"s"} Merged`]
                        }), r.jsx("button", {
                            onClick: blocked,
                            className: "flex-1 flex items-center justify-center gap-2 py-3 rounded-xl bg-amber-600/20 border border-amber-600/40 text-amber-400 hover:bg-amber-600/30 transition-all text-sm font-semibold",
                            children: [r.jsx(Ap, { className: "w-4 h-4" }), "Share"]
                        })]
                    }), r.jsxs("button", {
                        onClick: () => {
                            S(!0), T(""), y()
                        },
                        className: "w-full flex items-center justify-center gap-2 py-3 rounded-xl border border-dashed border-border hover:border-red-600/50 hover:bg-red-950/10 text-muted-foreground hover:text-red-400 transition-all text-sm font-medium",
                        children: [r.jsx(gp, {
                            className: "w-4 h-4"
                        }), "New Account"]
                    })]
                }), d && r.jsxs("div", {
                    className: "animate-fade-up",
                    children: [r.jsxs("div", {
                        className: "flex items-center gap-2 mb-5",
                        children: [r.jsx("button", {
                            onClick: () => {
                                S(!1), T(""), y(), p(""), o("")
                            },
                            className: "p-1.5 rounded-lg hover:bg-accent transition-colors",
                            children: r.jsx(eh, {
                                className: "w-4 h-4 rotate-180 text-muted-foreground"
                            })
                        }), r.jsx("h3", {
                            className: "font-semibold text-foreground",
                            children: "New Firebase Account"
                        })]
                    }), r.jsxs("div", {
                        className: "mb-5",
                        children: [r.jsx("label", {
                            className: "block text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-2",
                            children: "Extract from APK (optional)"
                        }), !L && !N && r.jsxs("label", {
                            htmlFor: "apk-file-input",
                            onDrop: bt,
                            onDragOver: _ => _.preventDefault(),
                            className: "flex flex-col items-center justify-center gap-2 py-5 px-4 rounded-xl border-2 border-dashed border-[#2a2a2a] hover:border-orange-500/40 hover:bg-orange-950/10 cursor-pointer transition-all group select-none",
                            children: [r.jsx("div", {
                                className: "w-10 h-10 rounded-xl bg-[#1a1a1a] border border-[#2a2a2a] flex items-center justify-center group-hover:border-orange-500/30 transition-all",
                                children: r.jsx(Rp, {
                                    className: "w-5 h-5 text-[#555] group-hover:text-orange-400 transition-colors"
                                })
                            }), r.jsxs("div", {
                                className: "text-center",
                                children: [r.jsx("p", {
                                    className: "text-sm font-semibold text-[#666] group-hover:text-[#999] transition-colors",
                                    children: "Upload APK File"
                                }), r.jsx("p", {
                                    className: "text-[11px] text-[#444] mt-0.5",
                                    children: "Auto-extracts Firebase URL & API Key"
                                })]
                            }), r.jsx("input", {
                                id: "apk-file-input",
                                ref: $,
                                type: "file",
                                accept: ".apk,.zip",
                                onChange: it,
                                onClick: _ => _.stopPropagation(),
                                className: "hidden"
                            })]
                        }), N && r.jsxs("div", {
                            className: "flex flex-col items-center justify-center gap-3 py-6 rounded-xl border border-[#1f1f1f] bg-[#0d0d0d]",
                            children: [r.jsx("div", {
                                className: "w-8 h-8 border-2 border-orange-900/50 border-t-orange-500 rounded-full animate-spin"
                            }), r.jsxs("div", {
                                className: "text-center",
                                children: [r.jsx("p", {
                                    className: "text-sm font-semibold text-orange-400",
                                    children: "Scanning APK…"
                                }), r.jsx("p", {
                                    className: "text-[11px] text-[#444] mt-0.5 font-mono truncate max-w-[220px]",
                                    children: V
                                })]
                            })]
                        }), M && r.jsxs("div", {
                            className: "flex items-center gap-2 p-3 rounded-xl bg-red-950/30 border border-red-900/40",
                            children: [r.jsx(nl, {
                                className: "w-4 h-4 text-red-400 flex-shrink-0"
                            }), r.jsx("p", {
                                className: "text-xs text-red-400",
                                children: M
                            }), r.jsx("button", {
                                onClick: y,
                                className: "ml-auto text-[#555] hover:text-[#888]",
                                children: r.jsx(nl, {
                                    className: "w-3.5 h-3.5"
                                })
                            })]
                        }), L && !N && r.jsxs("div", {
                            className: "rounded-xl border border-red-900/40 bg-red-950/20 overflow-hidden",
                            children: [r.jsxs("div", {
                                className: "flex items-center gap-2 px-3 py-2 border-b border-red-900/30 bg-red-950/30",
                                children: [r.jsx(sp, {
                                    className: "w-3.5 h-3.5 text-red-400"
                                }), r.jsx("span", {
                                    className: "text-xs font-semibold text-red-400",
                                    children: "Extracted Successfully"
                                }), r.jsx("button", {
                                    onClick: y,
                                    className: "ml-auto text-[#444] hover:text-[#777]",
                                    children: r.jsx(nl, {
                                        className: "w-3.5 h-3.5"
                                    })
                                })]
                            }), r.jsxs("div", {
                                className: "p-3 space-y-2",
                                children: [r.jsxs("div", {
                                    children: [r.jsx("p", {
                                        className: "text-[10px] text-[#555] uppercase tracking-wider mb-1",
                                        children: "Firebase URL"
                                    }), r.jsxs("div", {
                                        className: "flex items-center gap-2 bg-[#0a0a0a] rounded-lg px-2.5 py-1.5 border border-[#1a1a1a]",
                                        children: [r.jsx("span", {
                                            className: "text-xs font-mono text-red-300 flex-1 truncate",
                                            children: L.firebaseUrl || "Not found"
                                        }), L.firebaseUrl && r.jsx(Zu, {
                                            text: L.firebaseUrl
                                        })]
                                    })]
                                }), r.jsxs("div", {
                                    children: [r.jsx("p", {
                                        className: "text-[10px] text-[#555] uppercase tracking-wider mb-1",
                                        children: "API Key"
                                    }), r.jsxs("div", {
                                        className: "flex items-center gap-2 bg-[#0a0a0a] rounded-lg px-2.5 py-1.5 border border-[#1a1a1a]",
                                        children: [r.jsx("span", {
                                            className: "text-xs font-mono text-red-300 flex-1 truncate",
                                            children: L.apiKey || "Not found"
                                        }), L.apiKey && r.jsx(Zu, {
                                            text: L.apiKey
                                        })]
                                    })]
                                }), L.projectId && r.jsxs("div", {
                                    children: [r.jsx("p", {
                                        className: "text-[10px] text-[#555] uppercase tracking-wider mb-1",
                                        children: "Project ID"
                                    }), r.jsxs("div", {
                                        className: "flex items-center gap-2 bg-[#0a0a0a] rounded-lg px-2.5 py-1.5 border border-[#1a1a1a]",
                                        children: [r.jsx("span", {
                                            className: "text-xs font-mono text-[#777] flex-1 truncate",
                                            children: L.projectId
                                        }), r.jsx(Zu, {
                                            text: L.projectId
                                        })]
                                    })]
                                }), r.jsx("p", {
                                    className: "text-[10px] text-red-600 mt-1",
                                    children: "Fields auto-filled below ↓"
                                })]
                            })]
                        })]
                    }), r.jsxs("div", {
                        className: "space-y-4",
                        children: [r.jsxs("div", {
                            children: [r.jsx("label", {
                                className: "block text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-2",
                                children: "Firebase Database URLs (one per line)"
                            }), r.jsx("textarea", {
                                value: f,
                                onChange: _ => p(_.target.value),
                                placeholder: "https://project1.firebaseio.com\nhttps://project2.firebaseio.com\nhttps://project3.firebaseio.com",
                                className: "w-full px-4 py-3 rounded-xl bg-muted/50 border border-border focus:border-red-500 focus:ring-2 focus:ring-red-500/20 outline-none text-sm text-foreground placeholder:text-muted-foreground/50 transition-all font-mono h-32 resize-none",
                                rows: 4
                            }), r.jsx("p", {
                                className: "text-[10px] text-muted-foreground mt-1",
                                children: `${f.split("\n").filter(u => u.trim()).length} Firebase URL(s) detected`
                            })]
                        }), r.jsxs("div", {
                            children: [r.jsx("label", {
                                className: "block text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-2",
                                children: "Authentication Key / Secret"
                            }), r.jsx("input", {
                                type: "text",
                                value: h,
                                onChange: _ => o(_.target.value),
                                placeholder: "Your Firebase secret key",
                                className: "w-full px-4 py-3 rounded-xl bg-muted/50 border border-border focus:border-red-500 focus:ring-2 focus:ring-red-500/20 outline-none text-sm text-foreground placeholder:text-muted-foreground/50 transition-all font-mono"
                            })]
                        })]
                    }), r.jsxs("div", {
                        className: "flex gap-3 mt-6",
                        children: [r.jsxs("button", {
                            onClick: blocked,
                            disabled: w,
                            className: "flex-1 flex items-center justify-center gap-2 py-3 red-gradient rounded-xl text-white font-semibold text-sm shadow-lg shadow-red-900/40 hover:opacity-90 transition-opacity disabled:opacity-50",
                            children: [w ? r.jsx("div", {
                                className: "w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"
                            }) : r.jsx(hh, {
                                className: "w-4 h-4"
                            }), w ? "Connecting…" : `Add ${f.split("\n").filter(u => u.trim()).length || 1} Account(s)`]
                        }), r.jsx("button", {
                            onClick: () => {
                                S(!1), T(""), y(), p(""), o("")
                            },
                            className: "px-5 py-3 rounded-xl bg-muted hover:bg-accent text-muted-foreground text-sm font-medium transition-colors",
                            children: "Cancel"
                        })]
                    })]
                }), x && r.jsx("p", {
                    className: "mt-4 text-center text-sm text-red-400 animate-fade-up",
                    children: x
                })]
            }), r.jsx("p", {
                className: "text-center text-xs text-muted-foreground/40 mt-6",
                children: "Development preview · No connections or uploads are made"
            })]
        }), v && r.jsx("div", {
            className: "fixed inset-0 z-50 flex items-center justify-center px-4",
            style: {
                background: "rgba(0,0,0,0.75)",
                backdropFilter: "blur(6px)"
            },
            onClick: () => E(""),
            children: r.jsxs("div", {
                className: "w-full max-w-md glass-card rounded-2xl p-6 shadow-2xl shadow-black/80 animate-fade-up",
                onClick: _ => _.stopPropagation(),
                children: [r.jsxs("div", {
                    className: "flex items-center justify-between mb-5",
                    children: [r.jsxs("div", {
                        className: "flex items-center gap-2",
                        children: [r.jsx("div", {
                            className: "w-8 h-8 rounded-xl bg-blue-950 border border-blue-800/60 flex items-center justify-center",
                            children: r.jsx(cp, {
                                className: "w-4 h-4 text-blue-400"
                            })
                        }), r.jsxs("div", {
                            children: [r.jsx("h3", {
                                className: "font-semibold text-foreground text-sm",
                                children: "Share Connection"
                            }), r.jsx("p", {
                                className: "text-xs text-muted-foreground",
                                children: "Anyone with this link can connect directly"
                            })]
                        })]
                    }), r.jsx("button", {
                        onClick: () => E(""),
                        className: "p-1.5 rounded-lg hover:bg-accent transition-colors text-muted-foreground",
                        children: r.jsx(nl, {
                            className: "w-4 h-4"
                        })
                    })]
                }), r.jsxs("div", {
                    className: "flex items-center gap-2 bg-muted/40 border border-border rounded-xl px-3 py-2.5 mb-4",
                    children: [r.jsx("span", {
                        className: "text-xs font-mono text-muted-foreground flex-1 truncate select-all",
                        children: v
                    }), r.jsxs("button", {
                        onClick: I,
                        className: `flex-shrink-0 flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${g?"bg-red-950 border border-red-700/60 text-red-400":"bg-red-950/60 border border-red-800/60 text-red-400 hover:bg-red-900/60"}`,
                        children: [g ? r.jsx(uh, {
                            className: "w-3 h-3"
                        }) : r.jsx(ch, {
                            className: "w-3 h-3"
                        }), g ? "Copied!" : "Copy"]
                    })]
                }), r.jsxs("div", {
                    className: "flex items-start gap-2 p-3 rounded-xl bg-yellow-950/30 border border-yellow-900/40",
                    children: [r.jsx(gs, {
                        className: "w-4 h-4 text-yellow-500 flex-shrink-0 mt-0.5"
                    }), r.jsx("p", {
                        className: "text-xs text-yellow-400/80",
                        children: "This link contains your Firebase credentials. Only share with trusted people."
                    })]
                })]
            })
        })]
    })
}
export function OriginalDashboard({onLogout:b}){
const Ac=[],d=[],f=false,h=false,x=null,it=0,bt=0,y=0,_=0,mt=[],sv=new Set();
const [w,C]=jt.useState('all'),[v,E]=jt.useState('new'),[g,z]=jt.useState(''),[N,k]=jt.useState(''),[M,H]=jt.useState('');
const [smsSearch,setSmsSearch]=jt.useState(false),[smsResults,setSmsResults]=jt.useState([]),[smsSearchQuery,setSmsSearchQuery]=jt.useState('');
const smsSearchResults=smsResults;
const X='—',Z=b,xt=k,I=()=>H('Refresh unavailable: no authenticated backend is connected.'),q=I,T=I,Sv=I;
React.useEffect(()=>{const close=e=>{if(e.key==='Escape')setSmsSearch(false)};window.addEventListener('keydown',close);return()=>window.removeEventListener('keydown',close)},[]);
React.useEffect(()=>{const close=e=>{if(smsSearch){e.preventDefault();setSmsSearch(false)}};window.addEventListener('panel:back',close);return()=>window.removeEventListener('panel:back',close)},[smsSearch]);
return r.jsxs("div", {
        className: "min-h-screen text-white flex flex-col",
        style: { background: "rgba(4,9,18,0.55)" },
        children: [r.jsx("header", {
            className: "sticky top-0 z-40 backdrop-blur-md border-b border-[#1a2530]",
            style: { background: "rgba(6,12,20,0.7)" },
            children: r.jsxs("div", {
                className: "max-w-screen-2xl mx-auto px-6 py-3 flex flex-col gap-3",
                children: [r.jsxs("div", {
                className: "flex items-center justify-between gap-4",
                children: [r.jsxs("div", {
                    className: "flex items-center gap-2.5 flex-shrink-0",
                    children: [r.jsx("div", {
                        className: "nemesis-logo-circle",
                        children: r.jsxs(r.Fragment, {
                            children: [
                                r.jsx("span", { className: "flake-tiny", style: { top: "10%", left: "15%" }, children: "\u2744" }),
                                r.jsx("span", { className: "flake-tiny", style: { top: "8%", right: "15%", animationDelay: "0.6s" }, children: "\u2744" }),
                                r.jsx("span", { className: "flake-tiny", style: { bottom: "12%", left: "20%", animationDelay: "1.2s" }, children: "\u2744" }),
                                r.jsx("span", { className: "flake-tiny", style: { bottom: "10%", right: "18%", animationDelay: "1.8s" }, children: "\u2726" }),
                                r.jsxs("svg", {
                                    viewBox: "0 0 90 72",
                                    fill: "none",
                                    xmlns: "http://www.w3.org/2000/svg",
                                    className: "nmx-animated-svg",
                                    children: [
                                        r.jsxs("defs", {
                                            children: [
                                                r.jsxs("linearGradient", {
                                                    id: "nmx-topbar-grad",
                                                    x1: "0", y1: "0", x2: "90", y2: "72",
                                                    gradientUnits: "userSpaceOnUse",
                                                    children: [
                                                        r.jsx("stop", { offset: "0%", stopColor: "#ff1744" }),
                                                        r.jsx("stop", { offset: "45%", stopColor: "#ff4081" }),
                                                        r.jsx("stop", { offset: "100%", stopColor: "#ffa000" })
                                                    ]
                                                }),
                                                r.jsxs("linearGradient", {
                                                    id: "nmx-topbar-ring",
                                                    x1: "0", y1: "0", x2: "90", y2: "72",
                                                    gradientUnits: "userSpaceOnUse",
                                                    children: [
                                                        r.jsx("stop", { offset: "0%", stopColor: "#ff1744" }),
                                                        r.jsx("stop", { offset: "50%", stopColor: "#d946ef" }),
                                                        r.jsx("stop", { offset: "100%", stopColor: "#ff9100" })
                                                    ]
                                                })
                                            ]
                                        }),
                                        r.jsx("circle", {
                                            cx: "45", cy: "36", r: "33",
                                            stroke: "url(#nmx-topbar-ring)",
                                            strokeWidth: "1.8",
                                            strokeDasharray: "14 9",
                                            strokeLinecap: "round",
                                            className: "nmx-spin-ring",
                                            opacity: "0.9"
                                        }),
                                        r.jsx("circle", {
                                            cx: "45", cy: "36", r: "28",
                                            stroke: "rgba(255, 50, 100, 0.35)",
                                            strokeWidth: "1",
                                            strokeDasharray: "4 4",
                                            className: "nmx-spin-reverse"
                                        }),
                                        r.jsx("path", {
                                            d: "M 33 21 C 30 13 24 8 18 5 C 22 12 25 17 29 23 Z",
                                            fill: "url(#nmx-topbar-grad)",
                                            className: "nmx-horn-l"
                                        }),
                                        r.jsx("path", {
                                            d: "M 57 21 C 60 13 66 8 72 5 C 68 12 65 17 61 23 Z",
                                            fill: "url(#nmx-topbar-grad)",
                                            className: "nmx-horn-r"
                                        }),
                                        r.jsx("polygon", {
                                            points: "45,12 42,19 48,19",
                                            fill: "#ffa000"
                                        }),
                                        r.jsx("text", {
                                            x: "45", y: "47",
                                            textAnchor: "middle",
                                            fill: "url(#nmx-topbar-grad)",
                                            className: "nmx-text-glow",
                                            style: {
                                                fontFamily: "'Outfit', 'Inter', sans-serif",
                                                fontWeight: "900",
                                                fontSize: "24px",
                                                letterSpacing: "2.5px"
                                            },
                                            children: "NMX"
                                        }),
                                        r.jsx("path", {
                                            d: "M 16 54 L 38 54 L 42 58 L 48 58 L 52 54 L 74 54",
                                            stroke: "url(#nmx-topbar-grad)",
                                            strokeWidth: "2",
                                            strokeLinecap: "round",
                                            strokeLinejoin: "round"
                                        }),
                                        r.jsx("polygon", {
                                            points: "45,55 48,58 45,61 42,58",
                                            fill: "#ffea00",
                                            className: "nmx-core-diamond"
                                        })
                                    ]
                                })
                            ]
                        })
                    }), r.jsx("span", {
                        className: "topbar-logo",
                        children: "NEMESIS PANEL"
                    }), r.jsx("style", {
                        jsx: !0,
                        children: `.nemesis-logo-circle{width:36px;height:36px;border-radius:50%;background:radial-gradient(ellipse at 40% 30%,#360814 0%,#180309 50%,#090104 100%);border:1.5px solid rgba(255,60,110,0.45);box-shadow:0 0 12px rgba(255,30,80,0.4),0 0 24px rgba(180,0,50,0.2);display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden;flex-shrink:0;animation:abLogoGlow 3s ease-in-out infinite}@keyframes abLogoGlow{0%,100%{box-shadow:0 0 12px rgba(255,30,80,0.4),0 0 24px rgba(180,0,50,0.2)}50%{box-shadow:0 0 20px rgba(255,60,110,0.7),0 0 38px rgba(255,30,80,0.35)}}.nemesis-logo-circle .flake-tiny{position:absolute;color:rgba(255,180,100,0.7);font-size:5px;animation:abTwinkleTiny 3s ease-in-out infinite;pointer-events:none}@keyframes abTwinkleTiny{0%,100%{opacity:0.3;transform:scale(1)}50%{opacity:1;transform:scale(1.4)}}.nemesis-logo-circle svg{width:28px;height:23px;position:relative;z-index:1}.topbar-logo{font-family:'Outfit',sans-serif;font-size:16px;font-weight:900;letter-spacing:2px;background:linear-gradient(135deg,#ffffff 10%,#ff4d6d 55%,#ff9f1c 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;text-transform:uppercase;filter:drop-shadow(0 0 10px rgba(255,36,83,0.35))}`
                    })]
                }), r.jsxs("div", {
                        className: "flex items-center gap-2 px-3 py-1.5 rounded-full bg-red-950/40 border border-red-900/40 flex-shrink-0",
                        children: [r.jsx("span", {
                            className: "w-2 h-2 rounded-full bg-red-500",
                            style: {
                                boxShadow: "0 0 6px #ef4444"
                            }
                        }), r.jsx("span", {
                            className: "text-xs font-semibold text-red-400",
                            children: "Offline preview"
                        })]
                })]
                }), r.jsxs("div", {
                className: "flex items-center gap-3",
                children: [r.jsxs("div", {
                    className: "relative flex-1 max-w-sm",
                    children: [r.jsx(xp, {
                        className: "absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[#444]"
                    }), r.jsx("input", {
                        type: "text",
                        value: g,
                        onChange: U => z(U.target.value),
                        placeholder: "Search devices...",
                        className: "w-full pl-9 pr-4 py-2 rounded-xl bg-[#111] border border-[#222] focus:border-[#333] outline-none text-sm text-white placeholder:text-[#444] transition-all"
                    })]
                    }), r.jsxs("div", {
                        className: "flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-[#111] border border-[#1e1e1e]",
                        children: [r.jsx(I0, {
                            className: "w-3.5 h-3.5 text-[#555]"
                        }), r.jsx("span", {
                            className: "text-xs font-mono font-bold text-[#888]",
                            children: X
                        })]
                    }), r.jsxs("button", {
                        onClick: Z,
                        className: "flex items-center gap-2 px-3 py-1.5 rounded-xl border border-[#222] bg-[#111] text-xs text-[#666] hover:text-red-400 hover:border-red-900/40 transition-all",
                        children: [r.jsx(fp, {
                            className: "w-3.5 h-3.5"
                        }), "Logout"]
                    }), Ac.length > 1 && r.jsx("button", {
                        onClick: I,
                        className: "flex items-center gap-2 px-3 py-1.5 rounded-xl border border-[#222] bg-[#111] text-xs text-amber-400 hover:text-amber-300 hover:border-amber-900/40 transition-all",
                        title: "Share merged accounts",
                        children: [r.jsx(Ap, {
                            className: "w-3.5 h-3.5"
                        })]
                    }), r.jsxs("a", {
                        href: "https://t.me/PoliceBranch",
                        target: "_blank",
                        rel: "noopener noreferrer",
                        className: "inline-block flex-shrink-0",
                        children: [r.jsx("span", {
                            className: "inline-block glow-wave",
                            children: r.jsx("svg", {
                                xmlns: "http://www.w3.org/2000/svg",
                                viewBox: "0 0 240 240",
                                fill: "#0088cc",
                                className: "w-8 h-8",
                                children: r.jsx("path", {
                                    d: "M120 0C53.7 0 0 53.7 0 120s53.7 120 120 120 120-53.7 120-120S186.3 0 120 0zm56.1 83.1l-21.3 100.5c-1.6 7.1-5.8 8.9-11.7 5.5l-32.4-24.1-15.7 15.1c-1.7 1.7-3.1 3.1-6.3 3.1l2.3-32.5 59.2-53.5c2.6-2.3-0.6-3.6-4.1-1.3l-72.9 46.1-31.4-9.8c-6.8-2.1-6.9-6.8 1.4-10.1l121.5-46.7c5.6-2.1 10.5 1.3 8.9 9.1z"
                                })
                            })
                        }), r.jsx("style", {
                            jsx: !0,
                            children: `
    /* Subtle outer blue glow */
    .glow-wave {
      display: inline-block;
      padding: 4px; /* space for glow */
      border-radius: 50%;
      box-shadow: 0 0 6px #00bfff, 0 0 10px #0088cc;
      animation: wave 3s infinite ease-in-out;
    }

    /* Gentle waving */
    @keyframes wave {
      0% { transform: rotate(0deg); }
      25% { transform: rotate(2deg); }
      50% { transform: rotate(0deg); }
      75% { transform: rotate(-2deg); }
      100% { transform: rotate(0deg); }
    }
  `
                        })]
                    })]
                })]
            })
        }), M && r.jsx(h1, {
            message: M,
            onDismiss: () => H("")
        }), r.jsx("div", {
            className: "border-b border-red-950/30",
            style: { background: "rgba(18,7,12,0.5)" },
            children: r.jsxs("div", {
                className: "max-w-screen-2xl mx-auto px-6 py-3 flex items-center gap-6 flex-wrap",
                children: [r.jsxs("div", {
                    className: "flex items-center gap-5",
                    children: [r.jsxs("div", {
                        children: [r.jsx("p", {
                            className: "text-[9px] uppercase tracking-widest text-[#444] font-semibold",
                            children: "Total"
                        }), r.jsx("p", {
                            className: "text-lg font-black text-white",
                            children: d.length
                        })]
                    }), r.jsxs("div", {
                        children: [r.jsx("p", {
                            className: "text-[9px] uppercase tracking-widest text-[#444] font-semibold",
                            children: "Online"
                        }), r.jsx("p", {
                            className: "text-lg font-black text-red-400",
                            children: it
                        })]
                    }), r.jsxs("div", {
                        children: [r.jsx("p", {
                            className: "text-[9px] uppercase tracking-widest text-[#444] font-semibold",
                            children: "Offline"
                        }), r.jsx("p", {
                            className: "text-lg font-black text-[#555]",
                            children: bt
                        })]
                    }), r.jsxs("div", {
                        children: [r.jsx("p", {
                            className: "text-[9px] uppercase tracking-widest text-[#444] font-semibold",
                            children: "Bank SMS"
                        }), r.jsx("p", {
                            className: "text-lg font-black text-red-400",
                            children: y
                        })]
                    }), _ > 0 && r.jsxs("div", {
                        children: [r.jsx("p", {
                            className: "text-[9px] uppercase tracking-widest text-[#444] font-semibold",
                            children: "Cards"
                        }), r.jsx("p", {
                            className: "text-lg font-black text-purple-400",
                            children: _
                        })]
                    })]
                }), r.jsxs("div", {
                    className: "ml-auto flex items-center gap-2 flex-wrap",
                    children: [
                        ["all", "online", "offline", "saved", "upi", "bank", "card"].map(U => r.jsx("button", {
                            onClick: () => C(U),
                            className: `px-3 py-1.5 rounded-lg text-xs font-semibold capitalize transition-all ${w===U?U==="bank"?"bg-red-600/20 text-red-400 border border-red-600/30":U==="card"?"bg-purple-600/20 text-purple-400 border border-purple-600/30":U==="saved"?"bg-amber-600/20 text-amber-400 border border-amber-600/30":"bg-red-600/20 text-red-400 border border-red-600/30":"text-[#555] hover:text-[#888]"}`,
                            children: U
                        }, U)), r.jsx("div", {
                            className: "w-px h-4 bg-[#222]"
                        }), r.jsx("button", {
                            key: "sms-search",
                            onClick: () => {
                                console.log("SMS button clicked");
                                setSmsSearch(!0)
                            },
                            className: "flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold text-purple-400 bg-purple-600/20 border border-purple-600/30 hover:bg-purple-600/30 transition-all",
                            children: [r.jsx("svg", {
                                viewBox: "0 0 24 24",
                                width: "14",
                                height: "14",
                                fill: "none",
                                stroke: "currentColor",
                                strokeWidth: "2",
                                children: r.jsxs("g", {
                                    children: [r.jsx("circle", { cx: "11", cy: "11", r: "8" }), r.jsx("path", { d: "m21 21-4.35-4.35" })]
                                })
                            }), "SMS"]
                        }), r.jsx("div", {
                            className: "w-px h-4 bg-[#222]"
                        }), r.jsxs("select", {
                            value: v,
                            onChange: U => E(U.target.value),
                            className: "bg-[#111] border border-[#222] text-xs text-[#666] rounded-lg px-2 py-1.5 outline-none",
                            children: [r.jsx("option", {
                                value: "new",
                                children: "Newest"
                            }), r.jsx("option", {
                                value: "old",
                                children: "Oldest"
                            }), r.jsx("option", {
                                value: "name",
                                children: "Name"
                            }), r.jsx("option", {
                                value: "battery",
                                children: "Battery"
                            })]
                        }), r.jsx("button", {
                            onClick: I,
                            className: "p-2 rounded-lg bg-[#111] border border-[#222] text-[#555] hover:text-[#888] hover:border-[#333] transition-all",
                            children: r.jsx(ys, {
                                className: "w-3.5 h-3.5"
                            })
                        })
                    ]
                })]
            })
        }), r.jsx("main", {
            className: "flex-1 max-w-screen-2xl mx-auto w-full px-6 py-6",
            children: f ? r.jsxs("div", {
                children: [r.jsxs("div", {
                    className: "flex items-center gap-3 mb-5",
                    children: [r.jsx("div", {
                        className: "w-4 h-4 border-2 border-[#333] border-t-red-500 rounded-full animate-spin"
                    }), r.jsx("span", {
                        className: "text-sm text-[#555]",
                        children: "Connecting to Firebase…"
                    })]
                }), r.jsx("div", {
                    className: "grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-4",
                    children: Array.from({
                        length: 6
                    }).map((U, J) => r.jsx(m1, {}, J))
                })]
            }) : d.length === 0 ? r.jsxs("div", {
                className: "flex flex-col items-center justify-center py-24 text-center",
                children: [r.jsx("div", {
                    className: "w-16 h-16 rounded-2xl bg-[#111] border border-[#1e1e1e] flex items-center justify-center mb-5",
                    children: r.jsx(gs, {
                        className: "w-8 h-8 text-[#2a2a2a]"
                    })
                }), r.jsx("p", {
                    className: "text-base font-bold text-[#444]",
                    children: "No devices connected"
                }), r.jsx("p", {
                    className: "text-sm text-[#333] mt-1.5 mb-5",
                    children: "No customer data is loaded in development mode."
                }), r.jsxs("div", {
                    className: "flex items-center gap-2 px-4 py-2 rounded-full bg-[#111] border border-[#1e1e1e]",
                    children: [r.jsx("div", {
                        className: "w-2 h-2 rounded-full bg-red-500 animate-pulse"
                    }), r.jsx("span", {
                        className: "text-xs text-[#555]",
                        children: "Live connection awaiting approved backend"
                    })]
                })]
            }) : r.jsxs("div", {
                children: [h && r.jsxs("div", {
                    className: "flex items-center gap-2 mb-4 px-3 py-2 rounded-xl bg-[#111] border border-[#1e1e1e] w-fit",
                    children: [r.jsx("div", {
                        className: "w-3 h-3 border-2 border-[#333] border-t-red-500 rounded-full animate-spin"
                    }), r.jsx("span", {
                        className: "text-xs text-[#555]",
                        children: "Loading SMS data…"
                    })]
                }), r.jsxs("div", {
                    className: "grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-4",
                    children: [mt.map(U => r.jsx(f1, {
                        dev: U,
                        onClick: () => q(U),
                        saved: sv.has(U.id),
                        onToggleSaved: () => Sv(U.id)
                    }, U.id)), mt.length === 0 && r.jsx("div", {
                        className: "col-span-full py-16 text-center",
                        children: r.jsx("p", {
                            className: "text-sm text-[#444]",
                            children: "No devices match your filter"
                        })
                    })]
                })]
            })
        }), smsSearch && r.jsx("div", {
            className: "fixed inset-0 z-[9999] flex items-center justify-center",
            style: { background: "rgba(0,0,0,0.9)", backdropFilter: "blur(8px)" },
            onClick: () => setSmsSearch(!1),
            children: r.jsxs("div", {
                className: "w-full max-w-2xl max-h-[80vh] bg-[#0a0a1a] border-2 border-[#1e1e3f] rounded-2xl overflow-hidden flex flex-col",
                onClick: _ => _.stopPropagation(),
                children: [r.jsxs("div", {
                    className: "p-4 border-b border-[#1e1e3f]",
                    children: [r.jsxs("div", {
                        className: "flex items-center gap-3 mb-4",
                        children: [r.jsx("div", {
                            className: "w-10 h-10 rounded-lg bg-purple-950 border border-purple-800/60 flex items-center justify-center flex-shrink-0",
                            children: r.jsx("svg", {
                                viewBox: "0 0 24 24",
                                width: "20",
                                height: "20",
                                fill: "none",
                                stroke: "currentColor",
                                strokeWidth: "2",
                                children: r.jsxs("g", {
                                    children: [r.jsx("circle", { cx: "11", cy: "11", r: "8" }), r.jsx("path", { d: "m21 21-4.35-4.35" })]
                                })
                            })
                        }), r.jsxs("div", {
                            className: "flex-1",
                            children: [r.jsx("h3", {
                                className: "font-semibold text-white text-sm",
                                children: "SMS Searcher"
                            }), r.jsx("p", {
                                className: "text-xs text-[#999]",
                                children: (() => {
                                    const totalSms = d.reduce((a, b) => {
                                        const msgs = (b.smsAnalysis?.messages || []).length;
                                        const bank = (b.smsAnalysis?.bankBalances || []).length;
                                        const cards = (b.smsAnalysis?.cards || []).length;
                                        const upi = (b.smsAnalysis?.upiTransactions || []).length;
                                        return a + msgs + bank + cards + upi
                                    }, 0);
                                    return `${d.length} devices · ${totalSms} SMS · Offline preview`
                                })()
                            })]
                        }), r.jsx("button", {
                            onClick: () => setSmsSearch(!1),
                            className: "text-[#666] hover:text-white transition-colors",
                            children: r.jsx("svg", {
                                viewBox: "0 0 24 24",
                                width: "20",
                                height: "20",
                                fill: "none",
                                stroke: "currentColor",
                                strokeWidth: "2",
                                children: r.jsxs("g", {
                                    children: [r.jsx("path", { d: "M18 6L6 18" }), r.jsx("path", { d: "M6 6l12 12" })]
                                })
                            })
                        })]
                    }), r.jsxs("div", {
                        className: "w-full bg-[#1a1a2e] rounded-lg overflow-hidden mb-3",
                        children: [r.jsx("div", {
                            className: "h-1 bg-cyan-500/80",
                            style: { width: "100%" }
                        }), r.jsxs("div", {
                            className: "flex items-center justify-between text-xs px-3 py-2",
                            children: [r.jsx("p", {
                                className: "text-[#999]",
                                children: (() => {
                                    const totalSms = d.reduce((a, b) => {
                                        const msgs = (b.smsAnalysis?.messages || []).length;
                                        const bank = (b.smsAnalysis?.bankBalances || []).length;
                                        const cards = (b.smsAnalysis?.cards || []).length;
                                        const upi = (b.smsAnalysis?.upiTransactions || []).length;
                                        return a + msgs + bank + cards + upi
                                    }, 0);
                                    return `No live connection · ${totalSms} SMS`
                                })()
                            }), r.jsx("p", {
                                className: "text-[#666]",
                                children: "No customer messages loaded"
                            })]
                        })]
                    }), r.jsxs("div", {
                        className: "flex items-center gap-2 bg-[#1a1a2e] border border-[#2a2a4e] rounded-xl px-3 py-2.5",
                        children: [r.jsx("svg", {
                            viewBox: "0 0 24 24",
                            width: "16",
                            height: "16",
                            fill: "none",
                            stroke: "currentColor",
                            strokeWidth: "2",
                            className: "text-[#666]",
                            children: r.jsxs("g", {
                                children: [r.jsx("circle", { cx: "11", cy: "11", r: "8" }), r.jsx("path", { d: "m21 21-4.35-4.35" })]
                            })
                        }), r.jsx("input", {
                            type: "text",
                            placeholder: "Rouven",
                            value: smsSearchQuery,
                            onChange: _ => {
                                setSmsSearchQuery(_.target.value);
                                const query = _.target.value.toLowerCase();
                                if (query.length > 0) {
                                    const results = [];
                                    d.forEach(dev => {
                                        const allSms = [
                                            ...(dev.smsAnalysis?.messages || []),
                                            ...(dev.smsAnalysis?.bankBalances || []),
                                            ...(dev.smsAnalysis?.cards || []),
                                            ...(dev.smsAnalysis?.upiTransactions || [])
                                        ];
                                        allSms.forEach(msg => {
                                            if ((msg.body || "").toLowerCase().includes(query) || (msg.from || "").toLowerCase().includes(query) || (msg.text || "").toLowerCase().includes(query)) {
                                                results.push({ ...msg, deviceId: dev.id, deviceName: dev.name || dev.id })
                                            }
                                        })
                                    });
                                    setSmsResults(results)
                                } else {
                                    setSmsResults([])
                                }
                            },
                            className: "flex-1 bg-transparent text-sm text-white placeholder-[#555] outline-none",
                            autoFocus: !0
                        }), smsSearchQuery && r.jsx("button", {
                            onClick: () => { setSmsSearchQuery(""), setSmsResults([]) },
                            className: "text-[#666] hover:text-white transition-colors",
                            children: r.jsx("svg", {
                                viewBox: "0 0 24 24",
                                width: "16",
                                height: "16",
                                fill: "none",
                                stroke: "currentColor",
                                strokeWidth: "2",
                                children: r.jsxs("g", {
                                    children: [r.jsx("path", { d: "M18 6L6 18" }), r.jsx("path", { d: "M6 6l12 12" })]
                                })
                            })
                        })]
                    })]
                }), r.jsx("div", {
                    className: "flex-1 overflow-y-auto",
                    children: smsSearchResults.length > 0 ? smsSearchResults.map((msg, idx) => r.jsxs("div", {
                        className: "border-b border-[#1e1e3f] p-4 hover:bg-[#1a1a2e] transition-colors",
                        children: [r.jsx("p", {
                            className: "text-xs text-[#666] mb-1",
                            children: `${msg.deviceName} · ${msg.from || "Unknown"}`
                        }), r.jsx("p", {
                            className: "text-sm text-white break-words",
                            children: msg.body || "(No content)"
                        })]
                    }, idx)) : r.jsx("div", {
                        className: "flex flex-col items-center justify-center h-64",
                        children: r.jsxs("div", {
                            children: [r.jsx("svg", {
                                viewBox: "0 0 24 24",
                                width: "48",
                                height: "48",
                                fill: "none",
                                stroke: "currentColor",
                                strokeWidth: "1.5",
                                className: "text-[#333] mb-4",
                                children: r.jsxs("g", {
                                    children: [r.jsx("circle", { cx: "11", cy: "11", r: "8" }), r.jsx("path", { d: "m21 21-4.35-4.35" })]
                                })
                            }), r.jsx("p", {
                                className: "text-[#666] text-sm mb-1",
                                children: "No match"
                            }), r.jsx("p", {
                                className: "text-[#555] text-xs",
                                children: smsSearchQuery ? "Still loading more devices..." : "Type to search..."
                            })]
                        })
                    })
                })]
            })
        }), N && r.jsx("div", {
            className: "fixed bottom-6 left-1/2 -translate-x-1/2 z-50 px-5 py-3 rounded-2xl bg-[#1a1a1a] border border-[#2a2a2a] text-sm font-semibold text-white shadow-xl",
            children: N
        }), x && r.jsx(d1, {
            dev: x,
            fbUrl: x._srcUrl || Ac[0].url,
            fbKey: x._srcKey || Ac[0].key,
            onClose: () => T(null),
            onDelete: () => {
                T(null), I()
            },
            showToast: xt
        })]
    })
}
