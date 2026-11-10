import type {NextConfig} from 'next';
const config:NextConfig={output:'export',trailingSlash:true,images:{unoptimized:true},poweredByHeader:false,env:{NEXT_PUBLIC_BACKEND_ORIGIN:process.env.NEXT_PUBLIC_BACKEND_ORIGIN||'https://dimgrey-mule-297927.hostingersite.com'}};
export default config;
