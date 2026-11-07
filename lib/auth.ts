import {createHash,randomBytes,scryptSync,timingSafeEqual} from 'node:crypto';
import {cookies} from 'next/headers';
import {requireDB} from './db';
import {ensureSchema} from './store';
import type {RowDataPacket} from 'mysql2';
export const cookieName='gokduman_admin';
export function hash(value:string){return createHash('sha256').update(value).digest('hex');}
export function equal(a:string,b:string){const aa=Buffer.from(a);const bb=Buffer.from(b);return aa.length===bb.length&&timingSafeEqual(aa,bb);}
export function passwordHash(password:string){const salt=randomBytes(16).toString('hex');return `${salt}:${scryptSync(password,salt,64).toString('hex')}`;}
export function verifyPassword(password:string,stored:string){const [salt,expected]=stored.split(':');if(!salt||!expected)return false;return equal(scryptSync(password,salt,64).toString('hex'),expected);}
export async function authenticated(){await ensureSchema();const token=(await cookies()).get(cookieName)?.value;if(!token)return false;const [rows]=await requireDB().execute<RowDataPacket[]>('SELECT token_hash FROM portfolio_sessions WHERE token_hash=? AND expires_at>UTC_TIMESTAMP()',[hash(token)]);return rows.length===1;}
export async function session(){const token=randomBytes(32).toString('hex');await requireDB().execute('INSERT INTO portfolio_sessions VALUES (?,DATE_ADD(UTC_TIMESTAMP(),INTERVAL 8 HOUR))',[hash(token)]);await requireDB().query('DELETE FROM portfolio_sessions WHERE expires_at<UTC_TIMESTAMP()');return token;}
export async function rateLimit(key:string,limit=8){const db=requireDB();await db.execute('INSERT INTO portfolio_attempts VALUES (?,1,DATE_ADD(UTC_TIMESTAMP(),INTERVAL 15 MINUTE)) ON DUPLICATE KEY UPDATE hits=IF(expires_at<UTC_TIMESTAMP(),1,hits+1),expires_at=IF(expires_at<UTC_TIMESTAMP(),DATE_ADD(UTC_TIMESTAMP(),INTERVAL 15 MINUTE),expires_at)',[hash(key)]);const [rows]=await db.execute<RowDataPacket[]>('SELECT hits FROM portfolio_attempts WHERE attempt_key=?',[hash(key)]);return rows[0].hits<=limit;}
