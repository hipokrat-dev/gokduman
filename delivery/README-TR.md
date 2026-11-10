# Dr. Murat Gökduman — GitHub Pages teslim paketi

## Bu paketin kapsamı
Bu klasör, `https://drmuratgokduman.github.io/` için hazırlanmış ön yüz kaynak kodudur.
Masaüstü/mobil 3D oda, mouse kamera hareketi, cihaz ekranları ve VR galeri korunur.
İçerikler mevcut Hostinger sunucusundan alınır. MySQL ve yönetim paneli Hostinger'da kalır.
Bu sürüm tamamen bağımsız bir backend teslimi değildir; Hostinger hizmetinin açık kalması gerekir.

## Yayına alma (bir kez)
1. `drmuratgokduman` hesabına giriş yapın ve **drmuratgokduman.github.io** adlı repo oluşturun. Ücretsiz GitHub Pages için public repo kullanın.
2. Bu klasörün **içindeki dosyaları** reponun köküne, `main` dalına yükleyin. Üst klasörü ayrıca yüklemeyin. `package.json`, `app`, `public` ve `.github/workflows/pages.yml` doğrudan kökte olmalı.
3. Gizli `.github` klasörünü atlamayın. macOS Finder'da Command+Shift+. ile gizli dosyalar görünür. Git veya GitHub Desktop ile yükleme önerilir. ZIP dosyasının kendisini repoya yüklemek siteyi kurmaz.
4. Repo → **Settings → Pages → Build and deployment → Source: GitHub Actions** seçin.
5. **Actions → Publish portfolio to GitHub Pages → Run workflow → main** ile yayını başlatın. Sonraki `main` gönderimleri otomatik yayınlanır.
6. İş akışı başarılı olduğunda `https://drmuratgokduman.github.io/` adresini açın.

Repo adı veya kullanıcı adı farklıysa bu paket kök adres için yeniden yapılandırılmalıdır; `/repo-adi/` alt yolu için hazırlanmadı.

## İçerik değiştirme
- Ana sayfada sol üst raftaki beyaz kitaba tıklayın. Kitap parlamaz.
- Yönetim paneli: https://dimgrey-mule-297927.hostingersite.com/admin
- Yetkili yönetici hesabıyla başlık, açıklama, yayın durumu, sıralama, görseller ve profil bilgilerini düzenleyin.
- Değişikliği kaydedip GitHub sitesini yenileyin. Yeni bir GitHub yayını gerekmez.
- Yönetici giriş bilgileri bu pakette bulunmaz; site sahibiyle ayrı ve güvenli biçimde paylaşılmalıdır.
- Yönetici ekranına geçerken adresin Hostinger olması beklenir. Giriş oturumu GitHub'a taşınmaz.

## Teknik yapı
- Next.js statik dışa aktarım: `npm run build` → `out/`.
- Three.js / React Three Fiber / Drei; GLB modeller ve dokular pakettedir.
- GitHub Actions: Node.js 22, `npm ci`, derleme, Pages artifact, deployment.
- Genel API: `https://dimgrey-mule-297927.hostingersite.com/api/public/content`.
- API yalnızca yayınlanmış projeleri ve herkese açık profil alanlarını verir. Taslaklar, şifreler ve oturumlar verilmez.
- Kullanıcının yüklediği görseller Hostinger `/api/media/...` adresinden; paketle gelen görseller ve modeller GitHub Pages'ten yüklenir.
- Veri alınamazsa açık hata mesajı ve tekrar deneme düğmesi gösterilir; gerçek içerik yerine sessizce demo gösterilmez.

## Yerel çalıştırma
Node.js 22 kurulu bilgisayarda:

```sh
npm ci
npm run dev
```

Statik çıktıyı üretmek için:

```sh
npm run build
python3 -m http.server 8080 --directory out
```

Tarayıcıda `http://localhost:8080` açın. Statik çıktı için `next start` kullanmayın.

## Backend adresi ileride değişirse
`next.config.ts` içindeki varsayılan `NEXT_PUBLIC_BACKEND_ORIGIN` adresini değiştirip tekrar yayınlayın veya derleme ortamında bu genel değişkeni tanımlayın. Yeni sunucunun `/api/public/content`, `/api/media/...`, `/admin` yollarını desteklemesi gerekir.

`NEXT_PUBLIC_` ile başlayan değerler tarayıcıya açıktır. Veritabanı şifresi, yönetici şifresi veya ADMIN_SETUP_TOKEN eklemeyin. Bu pakete `.env`, Hostinger yedeği veya veritabanı dökümü koymayın.

## Teslim sonrası kontrol
- Ana sayfa ve iki ayrı masaüstü/mobil oda yükleniyor.
- Mouse hafif kamera hareketi oluşturuyor; dokunmatik cihazda otomatik hareket yok.
- Monitör, telefon, VR gözlüğü, yazıcı ve özgeçmiş açılıyor.
- Beyaz kitap Hostinger yönetim panelini açıyor.
- Üç VR demo başlığı: İlk Yardım, AED Eğitimi, İş Güvenliği.
- Panelde içerik değiştirince GitHub sayfası yenilendiğinde değişiklik geliyor.

## Sorun giderme
- **404:** Repo adı, hesap adı, `main`, Pages kaynağı ve başarılı Actions çalışmasını kontrol edin.
- **Actions dosyası yok:** `.github/workflows/pages.yml` repoya yüklenmemiştir.
- **İçerik yüklenemiyor:** Hostinger API ve veritabanının çalıştığını kontrol edin; Secrets eklemek çözüm değildir.
- **Görsel/model 404:** `public` klasörünü ve kök alan adı kullanımını kontrol edin.

GitHub Pages kurulum belgesi: https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages
