import Office from '@/components/Office';
import {getDB} from '@/lib/db';
import {Project} from '@/data/content';
import type {RowDataPacket} from 'mysql2';
export const dynamic = 'force-dynamic';
export default async function Page(){
 let projects:Project[]=[]; const db=getDB();
 if(db){try{const [rows]=await db.query<RowDataPacket[]>('SELECT id,title,description,category,external_url,image_url FROM projects WHERE published=1 ORDER BY sort_order,id');projects=rows as Project[]}catch{console.error('Portfolio content could not be loaded from MySQL.')}}
 return <Office projects={projects}/>;
}
