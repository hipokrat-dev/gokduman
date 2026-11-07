import Office from '@/components/Office';
import {content} from '@/lib/store';
import {demoProjects,demoProfile} from '@/data/content';
export const dynamic='force-dynamic';
export default async function Page(){let data={projects:demoProjects,profile:demoProfile};try{data=await content();}catch{console.error('Portfolio database unavailable; showing explicitly marked demo content.');}return <Office {...data}/>;}
