'use client';
import { Canvas, useThree } from '@react-three/fiber';
import { ContactShadows, Html, RoundedBox, useGLTF } from '@react-three/drei';
import { Suspense, useEffect, useRef, useState } from 'react';
import gsap from 'gsap';
import { Group, Mesh, MeshStandardMaterial, Vector3 } from 'three';
import {SectionID} from '@/data/content';
const targets:Record<SectionID,[number,number,number]>={projects:[0,1.65,1.8],vr:[-2,2.4,2.2],design:[2.05,2.25,2.2],about:[1.5,1.15,2.1],contact:[-1.7,1.1,2.1]};
function Camera({active,onReady}:{active:SectionID|null;onReady:()=>void}){
 const {camera,size}=useThree();
 useEffect(()=>{const mobile=size.width<700;const start=mobile?[0,2.8,9]:[0,2.6,6.5];const p=active?[...targets[active]]:start;if(active==='projects')p[2]=Math.max(2.7,1.38/(Math.tan(43*Math.PI/360)*(size.width/size.height)))-.45;const look=new Vector3(0,1.35,0);const destination=active?new Vector3(p[0],p[1]-.1,-.3):new Vector3(0,1.35,0);let state={t:0};const duration=matchMedia('(prefers-reduced-motion: reduce)').matches?0:1.25;const timeline=gsap.timeline({onComplete:onReady});timeline.to(camera.position,{x:p[0],y:p[1],z:p[2],duration,ease:'power2.inOut'},0);timeline.to(state,{t:1,duration,onUpdate:()=>{camera.lookAt(look.clone().lerp(destination,state.t))}},0);return()=>{timeline.kill()}},[active,camera,size.width,onReady]);return null;
}
function Box({position,size,color='#40362c',metal=0}:{position:[number,number,number];size:[number,number,number];color?:string;metal?:number}){return <RoundedBox args={size} radius={.025} smoothness={3} position={position} castShadow receiveShadow><meshStandardMaterial color={color} roughness={metal?.32:.68} metalness={metal}/></RoundedBox>}
function Hit({id,position,children,onOpen}:{id:SectionID;position:[number,number,number];children:React.ReactNode;onOpen:(id:SectionID)=>void}){
 const group=useRef<Group>(null);const [hovered,setHovered]=useState(false);
 useEffect(()=>{
  if(!hovered||!group.current)return;
  const originals=new Map<MeshStandardMaterial,{color:MeshStandardMaterial['emissive'];intensity:number}>();
  group.current.traverse(object=>{if(!(object instanceof Mesh))return;const materials=Array.isArray(object.material)?object.material:[object.material];materials.forEach(material=>{if(!(material instanceof MeshStandardMaterial)||originals.has(material))return;originals.set(material,{color:material.emissive.clone(),intensity:material.emissiveIntensity});material.emissive.set('#ffcf88');material.emissiveIntensity=.65;});});
  document.body.style.cursor='pointer';
  return()=>{originals.forEach((original,material)=>{material.emissive.copy(original.color);material.emissiveIntensity=original.intensity;});document.body.style.cursor='auto';};
 },[hovered]);
 return <group ref={group} position={position} onClick={e=>{e.stopPropagation();setHovered(false);onOpen(id)}} onPointerOver={e=>{e.stopPropagation();setHovered(true)}} onPointerOut={()=>setHovered(false)}>{children}</group>
}
function Plant({position}:{position:[number,number,number]}){return <group position={position}><mesh castShadow><cylinderGeometry args={[.18,.13,.3,24]}/><meshStandardMaterial color="#afa08c" roughness={.9}/></mesh>{Array.from({length:9},(_,i)=><mesh key={i} position={[Math.sin(i*2.4)*.12,.32+Math.sin(i)*.08,Math.cos(i*2.4)*.12]} rotation={[Math.sin(i)*.7,i,.35]} castShadow><sphereGeometry args={[1,12,8]}/><meshStandardMaterial color={i%2?'#384936':'#506044'} roughness={.9}/><group/></mesh>).map((el,i)=>({...el,props:{...el.props,scale:[.065,.32,.055]}}))}</group>}
function RoomAsset(){ const {scene}=useGLTF("/models/office-room.glb");return <primitive object={scene}/> }
function Room({active,ready,onOpen,children}:{active:SectionID|null;ready:boolean;onOpen:(id:SectionID)=>void;children:React.ReactNode}){return <>
<color attach="background" args={['#201c18']}/><fog attach="fog" args={['#201c18',11,24]}/>
<ambientLight intensity={.65}/><hemisphereLight args={['#c9d8e6','#775139',1.5]}/><directionalLight position={[-4,6,3]} intensity={2.6} color="#ffdfb4" castShadow shadow-mapSize={[2048,2048]}/><pointLight position={[-2,2.4,.4]} intensity={10} color="#ffbb6e" distance={6}/>
<RoomAsset/>
{[2.55,3.6].map(y=><group key={y}>{Array.from({length:12},(_,i)=><Box key={i} position={[(i<6?-2.55:1.1)+(i%6)*.23,y+.28,-1.28]} size={[.18,.47+(i%3)*.06,.28]} color={['#343f47','#775440','#c0ab83','#574d42'][i%4]}/>)}</group>)}
<Hit id="projects" position={[0,1.65,-.45]} onOpen={onOpen}><Box position={[0,0,0]} size={[2.3,1.35,.12]} color="#171b1e" metal={.4}/><Box position={[0,-.7,.1]} size={[.14,.35,.12]} color="#22272b" metal={.7}/><Box position={[0,-.78,.2]} size={[.65,.04,.4]} color="#22272b" metal={.7}/><mesh position={[0,0,.071]}><planeGeometry args={[2.17,1.22]}/><meshStandardMaterial color="#163038" emissive="#204b58" emissiveIntensity={.8}/></mesh>{active==='projects'&&ready?<Html transform position={[0,0,.09]} distanceFactor={1.12} style={{width:740,height:410}}>{children}</Html>:null}</Hit>
<Box position={[0,.97,.55]} size={[1.1,.045,.35]} color="#252829"/>{Array.from({length:40},(_,i)=><Box key={i} position={[-.47+(i%10)*.105,1.005,.43+Math.floor(i/10)*.075]} size={[.08,.025,.045]} color="#454744"/>)}<Box position={[.9,.98,.55]} size={[.18,.07,.28]} color="#252829"/>
<Hit id="contact" position={[-1.7,1.15,.2]} onOpen={onOpen}><group rotation={[-.15,0,0]}><Box position={[0,0,0]} size={[.28,.52,.035]} color="#161a1c"/><Box position={[0,0,.025]} size={[.24,.46,.01]} color="#64858d"/></group></Hit>
<Hit id="about" position={[1.65,.99,.4]} onOpen={onOpen}><Box position={[0,0,0]} size={[.7,.08,.45]} color="#303c37"/></Hit>
<Hit id="vr" position={[-2,2.95,-1.15]} onOpen={onOpen}><Box position={[0,0,0]} size={[.75,.37,.35]} color="#d5d3c9"/><mesh position={[0,0,-.13]} rotation={[Math.PI/2,0,0]}><torusGeometry args={[.3,.055,12,30]}/><meshStandardMaterial color="#242828"/></mesh></Hit>
<Hit id="design" position={[2.05,2.99,-1.1]} onOpen={onOpen}>{[-.34,.34].map(x=><Box key={x} position={[x,0,0]} size={[.05,.75,.45]} color="#252a2b" metal={.7}/>)}<Box position={[0,.36,0]} size={[.75,.07,.45]} color="#252a2b"/><Box position={[0,-.36,0]} size={[.75,.07,.45]} color="#252a2b"/><mesh><icosahedronGeometry args={[.2,0]}/><meshStandardMaterial color="#e8b76d" metalness={.3} roughness={.35}/></mesh><pointLight intensity={1} distance={1.3} color="#ffd49b"/></Hit>
<Plant position={[-1.05,1.08,-.5]}/><Plant position={[2.45,1.08,-.4]}/><Plant position={[0,3.8,-1.2]}/>
<Box position={[-2.5,1.45,-.3]} size={[.04,1,.04]} color="#252b2b" metal={.8}/><mesh position={[-2.35,1.95,-.3]} rotation={[0,0,-.5]}><coneGeometry args={[.25,.3,32,1,true]}/><meshStandardMaterial color="#303536" metalness={.6} roughness={.4} side={2}/></mesh>
<ContactShadows position={[0,.001,0]} opacity={.3} scale={12} blur={2} far={4}/>
</>}
export default function Scene(props:{active:SectionID|null;ready:boolean;onReady:()=>void;onOpen:(id:SectionID)=>void;children:React.ReactNode}){return <Canvas shadows dpr={[1,1.5]} camera={{position:[0,2.6,6.5],fov:43}}><Suspense fallback={null}><Camera active={props.active} onReady={props.onReady}/><Room {...props}/></Suspense></Canvas>}
