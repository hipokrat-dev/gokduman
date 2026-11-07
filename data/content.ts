export const sections = [
 {id:'projects',name:'Projeler',label:'Dijital çalışmalar',description:'Yazılım ve teknoloji projeleri burada sergilenecek.'},
 {id:'vr',name:'Sanal gerçeklik',label:'Yeni dünyalar',description:'VR deneyimleri ve etkileşimli projeler burada sergilenecek.'},
 {id:'design',name:'3D tasarımlar',label:'Fikirden nesneye',description:'Üç boyutlu modeller ve baskı çalışmaları burada sergilenecek.'},
 {id:'about',name:'Özgeçmiş',label:'Tıp ve teknoloji',description:'Mesleki deneyim, eğitim ve çalışmalar bu alanda yer alacak.'},
 {id:'contact',name:'İletişim',label:'Birlikte üretelim',description:'İletişim ve sosyal profil bağlantıları eklendiğinde burada görünecek.'}
] as const;
export type SectionID = typeof sections[number]['id'];
export interface Project {id:string;title:string;description:string;category:string;external_url:string|null;image_url:string|null}
