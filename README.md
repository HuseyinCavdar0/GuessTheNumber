# GuessTheNumber_NetworkProgramming

Ağ Tabanlı Çok Oyunculu Sayı Tahmin Oyunu

Bilgisayar Ağ Programlama dersi kapsamında geliştirilmiş, gerçek zamanlı (real-time) ve çok oyunculu (multiplayer) bir sayı tahmin oyunudur. Python, WebSocket ve Flask teknolojileri kullanılarak geliştirilmiştir.

Proje Hakkında
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Oyunun temel amacı, sunucu tarafından rastgele üretilen 4 basamaklı ve rakamları birbirinden farklı gizli sayıyı, sistemin verdiği ipuçlarını (+/-) kullanarak en az denemede bulmaktır.
Oyun, asenkron yapısı sayesinde birden fazla oyuncunun aynı anda bağlanmasına, yarışmasına ve anlık olarak birbirlerinin skorlarını görmesine olanak tanır.

Özellikler
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Çok Oyunculu Altyapı: WebSocket ile düşük gecikmeli, gerçek zamanlı iletişim.
Canlı Skor Tablosu: Anlık oyuncu puanları ve tüm zamanların en iyileri.
Kalıcı Veri: Sunucu kapansa bile skorlar leaderboard.json dosyasında saklanır.
Dinamik Puanlama: Doğru tahmin, yanlış yer ve süreye göre değişen puanlama algoritması.

Çift Arayüz Desteği: Modern Web Arayüzü (Flask + HTML/JS).
Terminal İstemcisi (CLI).
Admin Modu: Sunucu bilgisayarından bağlanıldığında skor tablosunu sıfırlama yetkisi.

Kullanılan Teknolojiler
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Dil: Python 3 
Backend & Ağ: asyncio, websockets 
Web Sunucusu: Flask 
Frontend: HTML5, CSS3, JavaScript 
Veri Formatı: JSON 

Nasıl Oynanır?
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Giriş: Adınızı girin ve "Gir" butonuna basın.
Tahmin: 4 basamaklı, rakamları birbirinden farklı bir sayı girin (Örn: 1234).
İpuçları:
+ (Plus): Rakam doğru ve yeri de doğru.
- (Minus): Rakam gizli sayıda var ama yeri yanlış.

Örnek: Gizli sayı 4271, Tahmin 1234 -> Sonuç: +1, -2.

Kazanma: 20 hak bitmeden sayıyı doğru tahmin eden oyuncu turu kazanır ve ekstra puan alır.

Dosya Yapısı
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
server.py: WebSocket sunucusu ve oyuncu yönetimi.
game_logic.py: Oyun kuralları ve matematiksel hesaplamalar.
app.py: Web arayüzünü sunan Flask uygulaması.
client.py: Alternatif terminal tabanlı istemci.
templates/index.html: Oyunun arayüz tasarımı.
static/app.js: İstemci tarafı mantığı ve WebSocket bağlantısı.
