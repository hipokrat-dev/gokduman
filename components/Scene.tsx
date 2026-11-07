'use client';
import {Suspense,useEffect,useMemo,useRef,useState} from 'react';
import {Canvas,ThreeEvent,useThree} from '@react-three/fiber';
import {useGLTF} from '@react-three/drei';
import {Box3,Mesh,MeshStandardMaterial,Object3D,PerspectiveCamera,Vector3} from 'three';
import gsap from 'gsap';
import {SectionID} from '@/data/content';
type Props={active:SectionID|null;onReady:()=>void;onLoaded:()=>void;onOpen:(id:SectionID)=>void};
function Room({active,onReady,onLoaded,onOpen}:Props){
 const {camera,size,gl}=useThree();const mobile=size.width<700;
 const asset=useGLTF(`/models/office-${mobile?'mobile':'desktop'}.glb`);
 const room=useMemo(()=>{const clone=asset.scene.clone(true);clone.traverse(o=>{if(o instanceof Mesh){o.material=Array.isArray(o.material)?o.material.map(m=>m.clone()):o.material.clone();}});return clone},[asset]);
 const [hover,setHover]=useState<string|null>(null);const look=useRef(new Vector3(0,2.05,-.3));
 const sections=useMemo(()=>{const nodes=new Map<string,Object3D>();room.traverse(o=>{if(o.userData.section)nodes.set(o.userData.section,o)});return nodes},[room]);
 useEffect(()=>{onLoaded()},[room,onLoaded]);
 useEffect(()=>{room.traverse(o=>{if(o instanceof Mesh){const materials=Array.isArray(o.material)?o.material:[o.material];for(const material of materials){const m=material as MeshStandardMaterial;if(m.emissive)m.emissive.setRGB(o.userData.section===hover?1.65:1,o.userData.section===hover?1.35:1,o.userData.section===hover?1.05:1);}}});gl.domElement.style.cursor=hover?'pointer':'default';return()=>{gl.domElement.style.cursor='default'}},[room,hover,gl]);
 useEffect(()=>{const cam=camera as PerspectiveCamera;const aspect=size.width/size.height;const distance=mobile?8.1:7.5;const height=mobile?4.9:3.1;const width=mobile?3.1:5.8;cam.fov=2*Math.atan(Math.max(height,width/aspect)/2/distance)*180/Math.PI;cam.updateProjectionMatrix();let target=new Vector3(0,mobile?2.22:2.05,-.3),position=new Vector3(0,mobile?2.45:2.13,mobile?7.8:7.2);const node=active?sections.get(active):null;if(node){const box=new Box3().setFromObject(node);target=box.getCenter(new Vector3());const dimensions=box.getSize(new Vector3());const d=Math.max(dimensions.y,dimensions.x/aspect)/2/Math.tan(cam.fov*Math.PI/360)*1.65;position=target.clone().add(new Vector3(0,.05,Math.max(1.4,d)));}const duration=window.matchMedia('(prefers-reduced-motion: reduce)').matches?0:1.25;const tl=gsap.timeline({onUpdate:()=>cam.lookAt(look.current),onComplete:onReady});tl.to(cam.position,{x:position.x,y:position.y,z:position.z,duration,ease:'power2.inOut'},0).to(look.current,{x:target.x,y:target.y,z:target.z,duration,ease:'power2.inOut'},0);return()=>{tl.kill()}},[active,camera,mobile,size.width,size.height,sections,onReady]);
 function section(e:ThreeEvent<PointerEvent|MouseEvent>){let o:Object3D|null=e.object;while(o){if(o.userData.section)return o.userData.section as SectionID;o=o.parent;}return null;}
 return <primitive object={room} onPointerMove={(e:ThreeEvent<PointerEvent>)=>{const id=section(e);setHover(id);if(id)e.stopPropagation()}} onPointerOut={()=>setHover(null)} onClick={(e:ThreeEvent<MouseEvent>)=>{const id=section(e);if(id&&!active){e.stopPropagation();onOpen(id)}}}/>;
}
export default function Scene(props:Props){return <Canvas dpr={[1,1.5]} camera={{position:[0,2.13,7.2],near:.05,far:50}} gl={{antialias:true,alpha:true}}><Suspense fallback={null}><Room {...props}/></Suspense></Canvas>}
