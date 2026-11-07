import {NextResponse} from 'next/server';
import {ensureSchema} from '@/lib/store';
import {requireDB} from '@/lib/db';
export const dynamic='force-dynamic';
export async function GET(){try{await ensureSchema();await requireDB().query('SELECT 1');return NextResponse.json({status:'ok',database:'connected'},{headers:{'Cache-Control':'no-store'}});}catch{return NextResponse.json({status:'degraded',database:'unavailable'},{status:503,headers:{'Cache-Control':'no-store'}});}}
