'use client';
import {Suspense,useEffect,useMemo,useRef,useState,RefObject} from 'react';
import {Canvas,useFrame,useThree} from '@react-three/fiber';
import {Html} from '@react-three/drei';
import {MathUtils} from 'three';
import {Project} from '@/data/content';
const accents=['#64d8e7','#98aaff','#efbd75'];
const projectAngle=(i:number,count:number)=>(i-(count-1)/2)*Math.min(.66,2.3/Math.max(1,count-1));
function media(value:string|null){if(!value)return undefined;if(/^\/previews\/[a-zA-Z0-9_.-]+$/.test(value)||/^\/api\/media\/[a-f0-9-]{36}$/.test(value))return value;try{const u=new URL(value);return ['https:','http:'].includes(u.protocol)?u.href:undefined}catch{return undefined}}
function LookAround({angle,locked}:{angle:number;locked:boolean}){
 const {camera,gl}=useThree();const aim=useRef({yaw:-angle,pitch:0});const current=useRef({yaw:-angle,pitch:0});
 useEffect(()=>{aim.current={yaw:-angle,pitch:0}},[angle]);
 useEffect(()=>{const canvas=gl.domElement;let pointer:{id:number;x:number;y:number}|null=null;canvas.style.touchAction='none';canvas.style.cursor=locked?'default':'grab';
 const down=(e:PointerEvent)=>{if(locked||e.button>0)return;pointer={id:e.pointerId,x:e.clientX,y:e.clientY};canvas.setPointerCapture(e.pointerId);canvas.style.cursor='grabbing'};
 const move=(e:PointerEvent)=>{if(!pointer||e.pointerId!==pointer.id)return;aim.current.yaw=MathUtils.clamp(aim.current.yaw+(e.clientX-pointer.x)*.0035,-1.45,1.45);aim.current.pitch=MathUtils.clamp(aim.current.pitch+(e.clientY-pointer.y)*.0025,-.30,.30);pointer.x=e.clientX;pointer.y=e.clientY};
 const up=()=>{pointer=null;canvas.style.cursor=locked?'default':'grab'};canvas.addEventListener('pointerdown',down);canvas.addEventListener('pointermove',move);canvas.addEventListener('pointerup',up);canvas.addEventListener('pointercancel',up);return()=>{canvas.removeEventListener('pointerdown',down);canvas.removeEventListener('pointermove',move);canvas.removeEventListener('pointerup',up);canvas.removeEventListener('pointercancel',up);canvas.style.cursor='default'}},[gl,locked]);
 useFrame((_,delta)=>{const reduced=window.matchMedia('(prefers-reduced-motion: reduce)').matches;const t=reduced?1:1-Math.exp(-delta*7);current.current.yaw=MathUtils.lerp(current.current.yaw,aim.current.yaw,t);current.current.pitch=MathUtils.lerp(current.current.pitch,aim.current.pitch,t);camera.rotation.set(current.current.pitch,current.current.yaw,0,'YXZ')});return null;
}
function Space({projects,focus,selected,onSelect,onFocusIndex,portal}:{projects:Project[];focus:number;selected:boolean;onSelect:(p:Project)=>void;onFocusIndex:(i:number)=>void;portal:RefObject<HTMLDivElement>}){
 const dots=useMemo(()=>{const points=new Float32Array(240*3);for(let i=0;i<240;i++){const a=i*2.39996,r=13+(i%7),y=3+(i%19)*.32;points.set([Math.sin(a)*r,y,Math.cos(a)*r],i*3)}return points},[]);
 return <><color attach="background" args={['#060d19']}/><fog attach="fog" args={['#060d19',9,27]}/><ambientLight intensity={.65}/><pointLight position={[0,4,-2]} intensity={35} color="#8ed9ff"/><pointLight position={[-5,3,1]} intensity={20} color="#7678d8"/>
 <LookAround angle={projectAngle(focus,projects.length)} locked={selected}/>
 <mesh rotation={[-Math.PI/2,0,0]} position={[0,-.03,0]}><circleGeometry args={[22,96]}/><meshStandardMaterial color="#142337" metalness={.55} roughness={.34}/></mesh>
 {[2.6,5.3,8].map((r,i)=><mesh key={r} rotation={[-Math.PI/2,0,0]} position={[0,.006,0]}><torusGeometry args={[r,.014,6,128]}/><meshBasicMaterial color={i===1?'#5db8ce':'#274f68'}/></mesh>)}
 <mesh position={[0,4.5,-1]} rotation={[Math.PI/2,0,0]}><torusGeometry args={[6.8,.025,8,96]}/><meshBasicMaterial color="#5b7a9b"/></mesh>
 {Array.from({length:16},(_,i)=>{const a=i*Math.PI/8;return <group key={i} position={[Math.sin(a)*8.5,0,Math.cos(a)*8.5]}><mesh position={[0,2.3,0]}><cylinderGeometry args={[.045,.075,4.6,8]}/><meshStandardMaterial color="#294356" metalness={.6} roughness={.4}/></mesh><mesh position={[0,2.5,.08]}><boxGeometry args={[.014,3.8,.014]}/><meshBasicMaterial color="#4b8fa5"/></mesh></group>})}
 <points><bufferGeometry><bufferAttribute attach="attributes-position" args={[dots,3]}/></bufferGeometry><pointsMaterial color="#9dcde9" size={.025} sizeAttenuation transparent opacity={.65}/></points>
 {projects.map((p,i)=>{const a=projectAngle(i,projects.length);const accent=accents[i%accents.length];return <group key={p.id} position={[Math.sin(a)*4.1,1.65,-Math.cos(a)*4.1]} rotation={[0,-a,0]}>
 <mesh position={[0,-.23,-.035]}><boxGeometry args={[2.22,1.98,.065]}/><meshStandardMaterial color="#12273a" metalness={.55} roughness={.3}/></mesh><mesh position={[0,-1.25,-.02]}><boxGeometry args={[.035,.55,.035]}/><meshBasicMaterial color={accent}/></mesh><mesh position={[0,-1.56,-.02]}><cylinderGeometry args={[.35,.40,.06,48]}/><meshStandardMaterial color="#1d3b50" metalness={.65} roughness={.3}/></mesh>
 <Html portal={portal} transform distanceFactor={2} position={[0,-.23,.01]} zIndexRange={[12,3]}><div className="vr-world-card" style={{borderColor:accent}} onPointerDown={e=>e.stopPropagation()} onPointerUp={e=>e.stopPropagation()} onClick={e=>e.stopPropagation()}><button aria-label={`${p.title} projesini aç`} onFocus={()=>onFocusIndex(i)} onClick={()=>onSelect(p)}><div className="vr-card-image">{media(p.image_url)?<img src={media(p.image_url)} alt={p.title}/>:<div className="vr-image-placeholder">◈</div>}<span>{String(i+1).padStart(2,'0')}</span></div><div className="vr-card-copy"><small style={{color:accent}}>{p.demo?'DEMO DENEYİM':'VR PROJESİ'}</small><h2>{p.title}</h2><div className="vr-card-bottom"><span>Sanal eğitim</span><span aria-hidden="true">↗</span></div></div></button></div></Html>
 </group>})}</>;
}
export default function VRGallery({projects,onExit}:{projects:Project[];onExit:()=>void}){
 const portal=useRef<HTMLDivElement>(null!);const [focus,setFocus]=useState(Math.floor(projects.length/2));const [selected,setSelected]=useState<Project|null>(null);const [entering,setEntering]=useState(true);const root=useRef<HTMLDivElement>(null);const sheet=useRef<HTMLElement>(null);const lastFocus=useRef<HTMLElement|null>(null);
 useEffect(()=>{root.current?.focus();const timer=setTimeout(()=>setEntering(false),window.matchMedia('(prefers-reduced-motion: reduce)').matches?0:750);return()=>clearTimeout(timer)},[]);
 useEffect(()=>{if(selected)sheet.current?.focus()},[selected]);
 const select=(p:Project)=>{lastFocus.current=document.activeElement as HTMLElement;setSelected(p)};
 const back=()=>{setSelected(null);lastFocus.current?.focus()};
 const shift=(delta:number)=>setFocus(i=>(i+delta+projects.length)%projects.length);
 return <div ref={root} tabIndex={-1} className="vr-experience" role="dialog" aria-modal="true" aria-label="Sanal gerçeklik proje alanı" onKeyDown={e=>{if(e.key==='Escape'){e.stopPropagation();if(selected)back();else onExit()}if(!selected&&(e.key==='ArrowLeft'||e.key==='ArrowRight')){e.preventDefault();if(projects.length)shift(e.key==='ArrowRight'?1:-1)}if(e.key==='Tab'){const region=selected?sheet.current:root.current;const elements=region?.querySelectorAll<HTMLElement>('button:not([disabled]),a[href]');if(elements?.length){const first=elements[0],last=elements[elements.length-1];if(e.shiftKey&&(document.activeElement===first||document.activeElement===region)){e.preventDefault();last.focus()}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus()}}}}}>
 <div className="vr-canvas" ref={portal}/><div className="vr-canvas"><Canvas dpr={[1,1.5]} camera={{position:[0,1.65,0],fov:65,near:.05,far:60}} gl={{antialias:true}}><Suspense fallback={null}><Space projects={projects} focus={focus} selected={!!selected} onSelect={select} onFocusIndex={setFocus} portal={portal}/></Suspense></Canvas></div>
 <div className="vr-lens-edge" aria-hidden="true"/>
 <header className="vr-hud"><div><span className="vr-status-dot"/><small>SANAL EĞİTİM ALANI</small></div><button className="vr-exit" onClick={onExit} aria-label="VR alanından çık ve atölyeye dön">✕ <span>Atölye</span></button></header>
 {!projects.length?<div className="vr-empty">Bu alanda henüz yayınlanmış proje yok.</div>:<nav className="vr-project-nav" aria-label="VR projeleri"><button className="vr-nav-arrow" onClick={()=>shift(-1)} aria-label="Önceki VR projesine bak">←</button><div>{projects.map((p,i)=><button key={p.id} aria-current={focus===i?'true':undefined} className={focus===i?'active':''} onClick={()=>setFocus(i)}>{p.title}</button>)}</div><button className="vr-nav-arrow" onClick={()=>shift(1)} aria-label="Sonraki VR projesine bak">→</button></nav>}
 {selected&&<div className="vr-sheet-backdrop" onPointerDown={e=>{if(e.target===e.currentTarget)back()}}><section ref={sheet} tabIndex={-1} className="vr-project-sheet" role="dialog" aria-modal="true" aria-labelledby="vr-project-title"><button className="vr-sheet-close" onClick={back} aria-label="VR proje alanına dön">✕</button>{media(selected.image_url)&&<img src={media(selected.image_url)} alt={selected.title}/>}<div className="vr-sheet-copy"><small>{selected.demo?'DEMO PROJE':'VR PROJESİ'}</small><h1 id="vr-project-title">{selected.title}</h1><p>{selected.description}</p>{selected.external_url&&media(selected.external_url)&&<a href={media(selected.external_url)} target="_blank" rel="noopener noreferrer">Projeyi aç ↗</a>}</div></section></div>}
 {entering&&<div className="vr-entry-mask" aria-hidden="true"><i/><i/></div>}
 </div>;
}
