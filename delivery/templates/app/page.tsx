'use client';
import {useEffect,useState} from 'react';
import Office from '@/components/Office';
import type {Profile,Project} from '@/data/content';
import {backendOrigin,adminUrl} from '@/lib/site-links';
type Content={projects:Project[];profile:Profile};
export default function Page(){
 const [data,setData]=useState<Content|null>(null),[error,setError]=useState(false),[attempt,setAttempt]=useState(0);
 useEffect(()=>{
  const controller=new AbortController();let live=true;setError(false);
  const timer=setTimeout(()=>controller.abort(),15000);
  fetch(`${backendOrigin}/api/public/content`,{signal:controller.signal,credentials:'omit',cache:'no-store'})
   .then(async response=>{if(!response.ok)throw new Error('Content unavailable');return response.json()})
   .then((value:Content)=>{if(!Array.isArray(value.projects)||typeof value.profile?.name!=='string')throw new Error('Invalid content');
    const projects=value.projects.map(p=>({...p,image_url:p.image_url?.startsWith('/api/media/')?`${backendOrigin}${p.image_url}`:p.image_url}));
    if(live)setData({...value,projects});
   }).catch(()=>{if(live)setError(true)}).finally(()=>clearTimeout(timer));
  return()=>{live=false;clearTimeout(timer);controller.abort()};
 },[attempt]);
 if(data)return <Office {...data}/>;
 return <main className="delivery-status"><h1>Dr. Murat Gökduman</h1>{error?<><p>İçerikler şu anda yüklenemiyor.</p><button onClick={()=>setAttempt(n=>n+1)}>Tekrar dene</button><a href={adminUrl}>Yönetim paneli</a></>:<p role="status">Atölye hazırlanıyor…</p>}</main>;
}
