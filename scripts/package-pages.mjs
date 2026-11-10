import {mkdir,copyFile,cp,writeFile,readFile} from 'node:fs/promises';
import {resolve,join} from 'node:path';
const root=resolve(import.meta.dirname,'..');
const dest=resolve(process.argv[2]||join(root,'../deliveries/drmuratgokduman.github.io'));
await mkdir(dest,{recursive:true});
for(const dir of ['components','data','public'])await cp(join(root,dir),join(dest,dir),{recursive:true});
// An explicit allowlist keeps server code, credentials, Git history and private files out.
for(const dir of ['app','lib'])await mkdir(join(dest,dir),{recursive:true});
for(const f of ['app/layout.tsx','app/globals.css','lib/site-links.ts','tsconfig.json','package.json','package-lock.json'])await copyFile(join(root,f),join(dest,f));
await cp(join(root,'delivery/templates'),dest,{recursive:true});
const ts=JSON.parse(await readFile(join(dest,'tsconfig.json'),'utf8'));ts.exclude=['node_modules'];await writeFile(join(dest,'tsconfig.json'),JSON.stringify(ts,null,2)+'\n');
await writeFile(join(dest,'.gitignore'),'node_modules/\n.next/\nout/\n.env*\n!.env.example\n*.tsbuildinfo\n.DS_Store\n');
await writeFile(join(dest,'.env.example'),'# Public API address, not a secret. Never add database credentials here.\nNEXT_PUBLIC_BACKEND_ORIGIN=https://dimgrey-mule-297927.hostingersite.com\n');
await writeFile(join(dest,'public/.nojekyll'),'');
await copyFile(join(root,'delivery/README-TR.md'),join(dest,'README.md'));
console.log(dest);
