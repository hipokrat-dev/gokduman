import {NextRequest,NextResponse} from 'next/server';
import {randomUUID} from 'node:crypto';
import {cookies} from 'next/headers';
import {requireDB} from '@/lib/db';
import {content,ensureSchema} from '@/lib/store';
import {authenticated,cookieName,equal,hash,passwordHash,rateLimit,session,verifyPassword} from '@/lib/auth';
import {profile,project} from '@/lib/validation';
import type {RowDataPacket} from 'mysql2';
export const runtime='nodejs';
export const dynamic='force-dynamic';
const response=(body:unknown,status=200)=>NextResponse.json(body,{status,headers:{'Cache-Control':'no-store'}});
export async function GET(_req:NextRequest,ctx:{params:Promise<{action:string}>}){try{await ensureSchema();const {action}=await ctx.params;if(action==='status'){const [rows]=await requireDB().query<RowDataPacket[]>('SELECT id FROM portfolio_admin LIMIT 1');return response({configured:rows.length>0,authenticated:await authenticated(),setupAvailable:(process.env.ADMIN_SETUP_TOKEN?.length||0)>=24});}if(!await authenticated())return response({error:'Oturum açmanız gerekiyor.'},401);if(action==='content')return response(await content(true));return response({error:'Bulunamadı.'},404);}catch{return response({error:'Veritabanı bağlantısı hazır değil. Hostinger ortam ayarlarını kontrol edin.'},503);}}
export async function POST(req:NextRequest,ctx:{params:Promise<{action:string}>}){
 const expected=process.env.APP_URL||req.nextUrl.origin;if(req.headers.get('origin')!==expected)return response({error:'İstek kaynağı geçersiz.'},403);
 try{await ensureSchema();const db=requireDB();const {action}=await ctx.params;
 if(action==='upload'){
  if(!await authenticated())return response({error:'Oturum açmanız gerekiyor.'},401);
  if(Number(req.headers.get('content-length')||0)>5_500_000)return response({error:'En fazla 5 MB yükleyebilirsiniz.'},413);
  const form=await req.formData();const file=form.get('file');if(!(file instanceof File)||file.size>5_000_000)return response({error:'Geçerli bir görsel seçin (en fazla 5 MB).'},400);
  const sharp=(await import('sharp')).default;const image=sharp(Buffer.from(await file.arrayBuffer()),{limitInputPixels:25_000_000});const metadata=await image.metadata();if(!['jpeg','png','webp'].includes(metadata.format||''))return response({error:'JPEG, PNG veya WebP yükleyin.'},400);
  const body=await image.resize(1600,1600,{fit:'inside',withoutEnlargement:true}).webp({quality:85}).toBuffer();const id=randomUUID();await db.execute('INSERT INTO portfolio_media (id,mime,body) VALUES (?,?,?)',[id,'image/webp',body]);return response({url:`/api/media/${id}`});
 }
 if(Number(req.headers.get('content-length')||0)>100000)return response({error:'İstek çok büyük.'},413);
 const body=await req.json();
 if(action==='setup'||action==='login'){
  if(!await rateLimit(`${action}:${req.headers.get('x-forwarded-for')?.split(',')[0]||'unknown'}`)||!await rateLimit(`${action}:global`,80))return response({error:'Çok fazla deneme. 15 dakika sonra tekrar deneyin.'},429);
  const username=String(body.username||'').trim().toLowerCase();const password=String(body.password||'');if(!/^[a-z0-9._@-]{3,100}$/.test(username)||password.length<12||password.length>200)return response({error:'Kullanıcı adı en az 3, şifre en az 12 karakter olmalı.'},400);
  if(action==='setup'){
   const secret=process.env.ADMIN_SETUP_TOKEN;if(!secret||secret.length<24||!equal(hash(String(body.token||'')),hash(secret)))return response({error:'Kurulum anahtarı geçersiz.'},403);
   const [existing]=await db.query<RowDataPacket[]>('SELECT id FROM portfolio_admin LIMIT 1');if(existing.length)return response({error:'Yönetici hesabı zaten oluşturulmuş.'},409);
   await db.execute('INSERT INTO portfolio_admin (id,username,password_hash) VALUES (1,?,?)',[username,passwordHash(password)]);
  }else{const [rows]=await db.execute<RowDataPacket[]>('SELECT password_hash FROM portfolio_admin WHERE username=?',[username]);if(!rows.length||!verifyPassword(password,rows[0].password_hash))return response({error:'Kullanıcı adı veya şifre yanlış.'},401);}
  const result=response({ok:true});result.cookies.set(cookieName,await session(),{httpOnly:true,secure:process.env.NODE_ENV==='production',sameSite:'strict',maxAge:8*60*60,path:'/'});return result;
 }
 if(!await authenticated())return response({error:'Oturumunuz sona erdi. Tekrar giriş yapın.'},401);
 if(action==='logout'){const token=(await cookies()).get(cookieName)?.value;if(token)await db.execute('DELETE FROM portfolio_sessions WHERE token_hash=?',[hash(token)]);const result=response({ok:true});result.cookies.delete(cookieName);return result;}
 if(action==='project'){const p=project(body);if(!p.id)p.id=randomUUID();if(!/^[a-zA-Z0-9_-]{1,64}$/.test(p.id))return response({error:'Proje kimliği geçersiz.'},400);await db.execute('INSERT INTO projects (id,title,description,category,external_url,image_url,published,sort_order,is_demo) VALUES (?,?,?,?,?,?,?,?,?) ON DUPLICATE KEY UPDATE title=VALUES(title),description=VALUES(description),category=VALUES(category),external_url=VALUES(external_url),image_url=VALUES(image_url),published=VALUES(published),sort_order=VALUES(sort_order),is_demo=VALUES(is_demo)',[p.id,p.title,p.description,p.category,p.external_url,p.image_url,p.published??false,p.sort_order??0,p.demo??false]);return response({ok:true,id:p.id});}
 if(action==='archive'){await db.execute('UPDATE projects SET published=0 WHERE id=?',[String(body.id)]);return response({ok:true});}
 if(action==='profile'){const p=profile(body);await db.execute("INSERT INTO portfolio_settings VALUES ('profile',?) ON DUPLICATE KEY UPDATE setting_value=VALUES(setting_value)",[JSON.stringify(p)]);return response({ok:true});}
 return response({error:'Bulunamadı.'},404);
 }catch(error){if(error instanceof Error&&['Alan uzunluğu geçersiz.','Proje başlığı gerekli.','Kategori geçersiz.','Sıra değeri geçersiz.','E-posta geçersiz.','Geçerli bir https bağlantısı girin.'].includes(error.message))return response({error:error.message},400);console.error('Admin request failed.');return response({error:'İşlem tamamlanamadı. Bağlantıyı ve alanları kontrol edin.'},500);}
}
