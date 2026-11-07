import {NextResponse} from 'next/server';
import {requireDB} from '@/lib/db';
import {ensureSchema} from '@/lib/store';
import type {RowDataPacket} from 'mysql2';
export async function GET(_req:Request,{params}:{params:Promise<{id:string}>}){const {id}=await params;if(!/^[a-f0-9-]{36}$/.test(id))return new NextResponse(null,{status:404});try{await ensureSchema();const [rows]=await requireDB().execute<RowDataPacket[]>('SELECT mime,body FROM portfolio_media WHERE id=?',[id]);if(!rows[0])return new NextResponse(null,{status:404});return new NextResponse(new Uint8Array(rows[0].body),{headers:{'Content-Type':rows[0].mime,'Cache-Control':'public,max-age=31536000,immutable','X-Content-Type-Options':'nosniff'}});}catch{return new NextResponse(null,{status:503});}}
