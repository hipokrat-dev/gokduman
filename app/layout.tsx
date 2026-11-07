import './globals.css';
import type { Metadata } from 'next';
export const metadata: Metadata = { title: 'Gökduman — Dijital Atölye', description: 'Tıp, teknoloji ve tasarımın buluştuğu interaktif çalışma alanı.' };
export default function Layout({children}:{children:React.ReactNode}) {return <html lang="tr"><body>{children}</body></html>}
