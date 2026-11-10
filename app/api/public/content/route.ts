import {content} from '@/lib/store';
export const dynamic='force-dynamic';
// Public portfolio content only. No sessions, credentials or draft records.
const headers={'Access-Control-Allow-Origin':'*','Cache-Control':'no-store','X-Content-Type-Options':'nosniff'};
export async function GET(){
 try{
  const data=await content();
  const {name,tagline,biography,email,github,linkedin,instagram,sketchfab,demo}=data.profile;
  return Response.json({projects:data.projects.map(({id,title,description,category,external_url,image_url,sort_order,demo})=>({id,title,description,category,external_url,image_url,sort_order,demo})),profile:{name,tagline,biography,email,github,linkedin,instagram,sketchfab,demo}},{headers});
 }catch{return Response.json({error:'CONTENT_UNAVAILABLE'},{status:503,headers});}
}
