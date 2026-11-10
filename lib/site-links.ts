// Empty for the Hostinger application; configured in the Pages delivery package.
export const backendOrigin=(process.env.NEXT_PUBLIC_BACKEND_ORIGIN||'').replace(/\/$/,'');
export const adminUrl=`${backendOrigin}/admin`;
