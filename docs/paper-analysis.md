# Referans makale analizi

## Problem, yöntem ve kapsam

Multi-access Edge Computing (MEC), kullanıcı cihazlarının görevlerini ağın kenarındaki sunuculara aktararak gecikmeyi azaltmayı amaçlar. Ancak cihazın kimliği doğrulansa bile görevi alacak sunucu veya iletişim yolu güvenilmez olabilir. Makale, Zero Trust Orchestrator (ZTO) üzerinden cihaz doğrulamasını, bulanık sunucu güven değerlendirmesini ve güvene duyarlı görev aktarımını bir araya getirir. Kimlik, biyometri ve fiziksel klonlanamaz işlev (PUF) cihaz doğrulamasına; QUARK ve blockchain güven kayıtlarına; SARSA ise görev aktarımı kararına hizmet eder.

Önerilen MRR, Bölüm 3.2'deki bulanık güven hesaplayıcısıdır. Şekil 6'daki iki paralel motor ve bunları birleştiren üçüncü motor yeniden kurulacaktır. Kimlik doğrulama, blockchain ve SARSA, bulanık alt sistem kapsamına dahil edilmemiştir. Deney için gerekli benzetim bileşenleri hocanın belirlediği MRR'ye göre kesinleştirilecektir.

## Girdiler ve çıktılar

| Simge | Anlamı |
|---|---|
| DT | Sunucunun geçmiş görev yürütme başarısına ve performansına dayanan doğrudan güven |
| RT | Komşu güvenilir sunuculardan gelen tavsiye güveni |
| IT | Kullanıcı cihazlarının sunucuya verdiği dolaylı güven |
| TT | İletim yolundaki başarılı ve röleli aktarımlarla ilişkili iletim güveni |
| FO1 | DT ve RT birleşimi |
| FO2 | IT ve TT birleşimi |
| FO3 | FO1 ve FO2 ile hesaplanan nihai sunucu güven puanı |

## Tablo 4'teki 17 kural

L düşük, M orta, H yüksek. Birinci ve ikinci motorun girdileri L/H, çıktıları L/M/H.

| Motor 1 DT | RT | FO1 | Motor 2 IT | TT | FO2 |
|---|---|---|---|---|---|
| H | H | H | H | H | H |
| H | L | M | H | L | M |
| L | H | M | L | H | M |
| L | L | L | L | L | L |

| Motor 3 FO1 | FO2 | FO3 |
|---|---|---|
| H | H | H |
| H | M | H |
| H | L | M |
| M | H | H |
| M | M | L |
| M | L | L |
| L | H | M |
| L | M | L |
| L | L | L |

Orta–orta → düşük, makalenin kuralıdır. Uygulamada önce her kuralın tek başına etkin olduğu girdiler, ardından birden fazla kuralın etkin olduğu ara değerler ve sınırlar kontrol edilecek.

## Kaynak bilgisi ve uygulama kararları

Makale, IT için kullanıcı güvenlerinin toplamını (Denklem 7), TT için röle ve başarılı iletim sayılarının toplamını (Denklem 8) verir. Bu toplamlar doğrudan 0–1 aralığında olmak zorunda değildir. İlk uygulamanın arayüzü dört normalleştirilmiş güven skoru alacak. Ham sayaçlardan skor üretilecekse normalleştirme yöntemi ayrıca tanımlanacak.

Şekil 6 ve Tablo 4 mimari ve kural kaynağıdır. Sayısal üyelik parametreleri, çıkarım operatörleri ve durulaştırma ayrıntıları uygulamadan önce kaynakta kontrol edilecek. Kaynaktan çıkarılamayan ayrıntılar için Mamdani min–max çıkarımı ve ağırlık merkezi durulaştırması aday kararlardır. Seçilen sayısal parametreler ve gerekçeleri uygulamayla birlikte kaydedilecek.

## Referans deney adayı

Bölüm 4, OMNeT++, Veins ve SUMO tabanlı MEC benzetimini anlatır. Tablo 6'da 100 kullanıcı cihazı, 3 MEC sunucusu, 2 eNodeB, 1 ZTO ve 15 dakikalık benzetim yer alır. Makalenin veri erişimi beyanı, verinin talep üzerine sunulacağını belirtir.

Şekil 7(c) ve Bölüm 4.3.2, yetkisiz cihaz sayısı arttıkça görev başarısızlık oranını karşılaştırır. Denklem 11'de oran, sunucudaki başarısız görev sayısının toplam alınan görev sayısına bölünmesidir. Pay ve paydaya hangi isteklerin girdiği deneyde açıkça kaydedilecek. Yazarlar ortalama %15 (önerilen sistem) ve %64 (SHA-256 tabanlı karşılaştırma) bildirir. Bu değerler kimlik doğrulama, güven ve aktarım bileşenlerini birlikte kullanan referans düzenekten gelir.

MRR izin verirse deney, 3 sunucu ve değişen yetkisiz cihaz sayısıyla sentetik olarak uyarlanacak. İstek akışı, kabul politikası, kapasite ve başarısızlık ölçütü deneyden önce belirlenecek. Yetkisiz cihaz etkisini modellemek için kimlik doğrulama basitleştirilirse bu karar açıkça kaydedilecek. Aynı koşullarda güven puanını kullanan ve kullanmayan iki aktarım politikası karşılaştırılabilir. Bu kontrol kolu SHA-256 sisteminin yeniden uygulaması değildir. Referansla sonuç karşılaştırması koşul farklarını ve eğilimleri içerecek. Uyarlamanın yeniden gerçekleştirme şartını karşılayıp karşılamadığı MRR ile teyit edilecek.

## Özgün katkı deneyi

Hipotez: Üyelik fonksiyonu ailesini değiştirmek, ölçüm gürültüsü altında sunucu sıralamasının kararlılığını etkiler. Kural tabanı, çıkarım, durulaştırma, giriş senaryoları ve rastgele tohumlar iki sürümde ortak tutulacak. Girdi aralığı dışına taşan gürültülü değerler aynı yöntemle sınırlandırılacak. Gürültüsüz koşula göre mutlak FO3 sapması ve en yüksek puanlı sunucunun değişme oranı raporlanacak. Eşit puanlarda ortak ve deterministik bir seçim kuralı kullanılacak. Sonuçlar puan kararlılığı ve sıralama davranışı açısından yorumlanacak.

## Sınırlılıklar

Sentetik skorlar, gerçek ağ ölçümlerini temsil etme iddiası taşımaz. Alt sistem deneyiyle uçtan uca kimlik doğrulama güvenliği, gecikme veya enerji kazanımı çıkarılamaz. Yazarlar ölçeklenebilirliği gelecekteki çalışmaya bırakır. Bu belgede belirtilen deneyler plan aşamasındadır.
