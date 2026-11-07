import mysql, { Pool } from 'mysql2/promise';
const globalDB = globalThis as typeof globalThis & { pool?: Pool };
export function getDB() {
 if (!process.env.DB_NAME || !process.env.DB_USER || !process.env.DB_PASSWORD) return null;
 return globalDB.pool ??= mysql.createPool({ host: process.env.DB_HOST || '127.0.0.1', port:Number(process.env.DB_PORT || 3306), user:process.env.DB_USER, password:process.env.DB_PASSWORD, database:process.env.DB_NAME, connectionLimit:5, waitForConnections:true });
}
