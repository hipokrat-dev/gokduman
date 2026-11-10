const assert=require('node:assert/strict');
const ts=require('typescript');
const fs=require('node:fs');
const vm=require('node:vm');
let fail=false;
const source=ts.transpileModule(fs.readFileSync('app/api/public/content/route.ts','utf8'),{compilerOptions:{module:ts.ModuleKind.CommonJS,target:ts.ScriptTarget.ES2020}}).outputText;
const context={exports:{},Response,require:(id)=>{assert.equal(id,'@/lib/store');return {content:async (...args)=>{assert.equal(args.length,0);if(fail)throw new Error('PRIVATE_DATABASE_DETAILS');return {projects:[{id:'published',title:'Public',category:'vr',description:'Demo',image_url:'/api/media/example',private_field:'DO_NOT_EXPOSE'}],profile:{name:'Public name',email:'public@example.com',password_hash:'DO_NOT_EXPOSE'}}}}}};
vm.runInNewContext(source,context);
(async()=>{
 const response=await context.exports.GET();assert.equal(response.status,200);assert.equal(response.headers.get('Access-Control-Allow-Origin'),'*');assert.equal(response.headers.get('Access-Control-Allow-Credentials'),null);
 const data=await response.json();assert.equal(data.projects[0].title,'Public');assert.equal(data.profile.name,'Public name');assert.ok(!JSON.stringify(data).includes('DO_NOT_EXPOSE'));
 fail=true;const unavailable=await context.exports.GET();assert.equal(unavailable.status,503);assert.deepEqual(await unavailable.json(),{error:'CONTENT_UNAVAILABLE'});console.log('Public content: CORS, public field allowlist and sanitized failure passed');
})().catch(e=>{console.error(e);process.exitCode=1});
