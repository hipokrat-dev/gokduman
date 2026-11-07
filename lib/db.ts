import mysql, {Pool} from 'mysql2/promise';
const state=globalThis as typeof globalThis & {portfolioPool?:Pool};
export function getDB(){
 if(!process.env.DB_NAME||!process.env.DB_USER||!process.env.DB_PASSWORD)return null;
 return state.portfolioPool??=mysql.createPool({host:process.env.DB_HOST||'127.0.0.1',port:Number(process.env.DB_PORT||3306),user:process.env.DB_USER,password:process.env.DB_PASSWORD,database:process.env.DB_NAME,connectionLimit:4,waitForConnections:true,queueLimit:20,connectTimeout:5000,charset:'utf8mb4'});
}
export function requireDB(){const db=getDB();if(!db)throw new Error('DATABASE_UNAVAILABLE');return db;}
