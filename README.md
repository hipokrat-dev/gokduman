# Gökduman — Dijital Atölye

Next.js, TypeScript, React Three Fiber, Drei, Three.js, GSAP ve Hostinger MySQL.

## Geliştirme

Node.js 22 veya 24 ile `npm ci`, ardından `npm run dev`.
`npm run build` üretim derlemesini hazırlar; `npm start` sunucuyu başlatır.

## Hostinger

Node.js Web App → GitHub → hipokrat-dev/gokduman → main.
Framework Next.js; build: npm run build; start: npm start.
Hostinger MySQL veritabanında database/schema.sql dosyasını çalıştırın.
.env.example içindeki değişkenleri Hostinger ortam değişkenlerine ekleyin.
Şifreler GitHub'a eklenmez. DB tanımlanmadan uygulama içerik bekleyen portfolyo olarak açılır.

## Durum

İlk etkileşim prototipi: masa, monitör, telefon, VR ve yazıcı hedefleri;
GSAP kamera geçişi, monitörde HTML, mobil paneller, geri dönüş ve sade görünüm.
Gerçek içerikler ve fotogerçekçi Blender GLB varlıkları sonraki aşamada eklenir.

## Yönetim paneli

`/admin` üzerinden proje ekleme/düzenleme, taslağa alma, görsel yükleme, özgeçmiş ve iletişim bağlantıları yönetilir. Demo içerikler ilk bağlantıda bir kez oluşturulur; daha sonra kaydedilen içeriklerin üzerine yazılmaz. Görseller Hostinger MySQL içinde saklanır.

Hostinger ortam değişkenleri: `DB_HOST=127.0.0.1`, `DB_PORT=3306`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `ADMIN_SETUP_TOKEN` (en az 24 karakter). İlk yönetici `/admin` sayfasında bu anahtarla oluşturulur; kullanıcı adı en az 3, şifre en az 12 karakter olmalıdır. İlk hesap sonrası kurulum kilitlenir. Kurulum anahtarı daha sonra ortamdan kaldırılabilir. Şifreler scrypt ile, oturum anahtarları SHA-256 ile özetlenir; oturum 8 saat sürer. Yönetim isteklerinde Origin doğrulaması vardır. Proxy farklı origin bildirirse `APP_URL` değerini sitenin HTTPS adresine ayarlayın.

`/api/health` veritabanı bağlantısı sağlıklıysa HTTP 200, hazır değilse HTTP 503 döndürür. Tablolar uygulama tarafından güvenli, tekrar çalıştırılabilir geçişlerle hazırlanır. Başlangıç için `database/schema.sql` elle çalıştırmak gerekli değildir.

## Sahne varlıkları

Masaüstü ve mobil için ayrı Blender sahneleri `assets/office-reference-*-v2.blend` dosyalarındadır. `scripts/export_web.py` Cycles ışığını dokulara bake eder ve etkileşim gruplarıyla GLB üretir. Tarayıcı Three.js / React Three Fiber ile modelleri gösterir; nesne seçimi kamera yakınlaşmasını başlatır, fare üzerindeyken nesnenin ışığı artar. Menü klavye erişimi, sade görünüm WebGL alternatifi sağlar. Dışa aktarılan GLB dosyaları yaklaşık 9 MB olduğundan ilk açılış bağlantıya bağlıdır.

Kontroller: `npm run build`, `node tests/validation.cjs`.
