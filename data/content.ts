export const sections = [
 {id:'projects',name:'Projeler',label:'Dijital çalışmalar'},
 {id:'vr',name:'Sanal gerçeklik',label:'Yeni dünyalar'},
 {id:'design',name:'3D tasarımlar',label:'Fikirden nesneye'},
 {id:'about',name:'Özgeçmiş',label:'Tıp ve teknoloji'},
 {id:'contact',name:'İletişim',label:'Birlikte üretelim'}
] as const;
export type SectionID = typeof sections[number]['id'];
export interface Project {id:string;title:string;description:string;category:string;external_url:string|null;image_url:string|null;published?:boolean;sort_order?:number;demo?:boolean}
export interface Profile {name:string;tagline:string;biography:string;email:string;github:string;linkedin:string;instagram:string;sketchfab:string;demo:boolean}
export const demoProfile:Profile={name:'Dr. Murat Gökduman',tagline:'Tıp · Teknoloji · Tasarım',biography:'Bu bir demo özgeçmiş metnidir. Eğitim, mesleki deneyim, araştırmalar ve ilgi alanları yönetim panelinden düzenlenebilir. Buradaki açıklamalar gerçek mesleki geçmişi temsil etmez.',email:'',github:'',linkedin:'',instagram:'',sketchfab:'',demo:true};
export const demoProjects:Project[]=[
 {id:'demo-digital-office',title:'Dijital Atölye',category:'projects',description:'Demo proje: Tıp, teknoloji ve tasarım çalışmalarını bir araya getiren etkileşimli bir çalışma odası. Proje başlığını, açıklamasını, görsellerini ve bağlantısını yönetim panelinden değiştirebilirsiniz.',image_url:'/previews/desktop.png',external_url:null,published:true,sort_order:0,demo:true},
 {id:'demo-learning',title:'Etkileşimli Öğrenme',category:'projects',description:'Demo proje: Görsel anlatım ve etkileşimli içeriklerle hazırlanabilecek bir eğitim uygulaması örneği. Bu kayıt örnek içeriktir; gerçek bir ürün veya klinik çalışma iddiası taşımaz.',image_url:'/previews/mobile.png',external_url:null,published:true,sort_order:1,demo:true},
 {id:'demo-vr',title:'Sanal Gerçeklik Deneyimi',category:'vr',description:'Demo proje: Sanal bir ortamı keşfetme ve nesnelerle etkileşim kurma fikrini gösteren örnek portfolyo kaydı. Kendi VR çalışmanızın görselini, açıklamasını ve bağlantısını ekleyebilirsiniz.',image_url:'/previews/desktop.png',external_url:null,published:true,sort_order:0,demo:true},
 {id:'demo-print',title:'Masaüstü 3D Çalışması',category:'design',description:'Demo proje: Tasarımdan modele, modelden baskıya uzanan üretim sürecini anlatmak için hazırlanmış örnek kayıt. Kendi tasarımlarınızı bu bölümden paylaşabilirsiniz.',image_url:'/previews/desktop.png',external_url:null,published:true,sort_order:0,demo:true}
];
