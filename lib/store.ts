import {requireDB} from './db';
import {demoProfile,demoProjects,vrDemoProjects,Profile,Project} from '@/data/content';
import type {RowDataPacket} from 'mysql2';
const state=globalThis as typeof globalThis & {portfolioSchema?:Promise<void>};
async function migrate(){
 const db=requireDB();
 const statements=[
 `CREATE TABLE IF NOT EXISTS projects (id VARCHAR(64) PRIMARY KEY,title VARCHAR(200) NOT NULL,description TEXT NOT NULL,category VARCHAR(32) NOT NULL DEFAULT 'projects',external_url VARCHAR(2048),image_url VARCHAR(2048),published BOOLEAN NOT NULL DEFAULT FALSE,sort_order INT NOT NULL DEFAULT 0,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci`,
 `CREATE TABLE IF NOT EXISTS portfolio_settings (setting_key VARCHAR(64) PRIMARY KEY,setting_value LONGTEXT NOT NULL) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci`,
 `CREATE TABLE IF NOT EXISTS portfolio_admin (id INT PRIMARY KEY,username VARCHAR(100) NOT NULL,password_hash VARCHAR(255) NOT NULL,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)`,
 `CREATE TABLE IF NOT EXISTS portfolio_sessions (token_hash CHAR(64) PRIMARY KEY,expires_at DATETIME NOT NULL,INDEX(expires_at))`,
 `CREATE TABLE IF NOT EXISTS portfolio_attempts (attempt_key VARCHAR(100) PRIMARY KEY,hits INT NOT NULL,expires_at DATETIME NOT NULL)`,
 `CREATE TABLE IF NOT EXISTS portfolio_media (id CHAR(36) PRIMARY KEY,mime VARCHAR(32) NOT NULL,body MEDIUMBLOB NOT NULL,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)`
 ];
 for(const sql of statements)await db.query(sql);
 const [columns]=await db.query<RowDataPacket[]>("SHOW COLUMNS FROM projects LIKE 'is_demo'");if(!columns.length){try{await db.query('ALTER TABLE projects ADD COLUMN is_demo BOOLEAN NOT NULL DEFAULT FALSE');}catch(error){if((error as {code?:string}).code!=='ER_DUP_FIELDNAME')throw error;}}
 // A transaction and durable marker prevent demo records reappearing after deletion.
 const connection=await db.getConnection();
 try{await connection.beginTransaction();await connection.query("INSERT IGNORE INTO portfolio_settings VALUES ('seeded','0')");const [rows]=await connection.query<RowDataPacket[]>("SELECT setting_value FROM portfolio_settings WHERE setting_key='seeded' FOR UPDATE");
 if(rows[0].setting_value==='0'){
 for(const p of demoProjects)await connection.execute('INSERT IGNORE INTO projects (id,title,description,category,external_url,image_url,published,sort_order,is_demo) VALUES (?,?,?,?,?,?,?,?,?)',[p.id,p.title,p.description,p.category,p.external_url,p.image_url,true,p.sort_order??0,true]);
 await connection.execute("INSERT IGNORE INTO portfolio_settings VALUES ('profile',?)",[JSON.stringify(demoProfile)]);await connection.query("UPDATE portfolio_settings SET setting_value='1' WHERE setting_key='seeded'");}
 await connection.query("INSERT IGNORE INTO portfolio_settings VALUES ('vr-gallery-v1','0')");
 const [vrSeed]=await connection.query<RowDataPacket[]>("SELECT setting_value FROM portfolio_settings WHERE setting_key='vr-gallery-v1' FOR UPDATE");
 if(vrSeed[0].setting_value==='0'){
  for(const p of vrDemoProjects)await connection.execute('INSERT IGNORE INTO projects (id,title,description,category,external_url,image_url,published,sort_order,is_demo) VALUES (?,?,?,?,?,?,?,?,?)',[p.id,p.title,p.description,p.category,p.external_url,p.image_url,true,p.sort_order??0,true]);
  await connection.execute("UPDATE projects SET published=0 WHERE id='demo-vr' AND is_demo=1 AND title='Sanal Gerçeklik Deneyimi' AND description LIKE 'Demo proje: Sanal bir ortamı keşfetme%'");
  await connection.query("UPDATE portfolio_settings SET setting_value='1' WHERE setting_key='vr-gallery-v1'");
 }
 await connection.commit();}catch(error){await connection.rollback();throw error;}finally{connection.release();}
}
export function ensureSchema(){return state.portfolioSchema??=migrate().catch(error=>{state.portfolioSchema=undefined;throw error;});}
export async function content(all=false){await ensureSchema();const db=requireDB();const [projects]=await db.query<RowDataPacket[]>(`SELECT id,title,description,category,external_url,image_url,published,sort_order,is_demo FROM projects ${all?'':'WHERE published=1'} ORDER BY category,sort_order,id`);const [settings]=await db.query<RowDataPacket[]>("SELECT setting_value FROM portfolio_settings WHERE setting_key='profile'");return {projects:projects.map(p=>({...p,published:Boolean(p.published),demo:Boolean(p.is_demo)})) as Project[],profile:{...demoProfile,...JSON.parse(settings[0]?.setting_value||'{}')} as Profile};}
