# MEC Sunucu Güveninin Bulanık Mantıkla Değerlendirilmesi

Bulanık Mantık dersi dönem projesi. Amaç, Ali ve arkadaşlarının MEC sunucu güven modelini yeniden kurmak ve üyelik fonksiyonu seçiminin ölçüm gürültüsü altındaki etkisini incelemek.

## Referans makale

B. Ali, M. A. Gregory, S. Li ve O. A. Dib, “Implementing zero trust security with dual fuzzy methodology for trust-aware authentication and task offloading in Multi-access Edge Computing,” *Computer Networks*, cilt 241, makale 110197, 2024. [DOI](https://doi.org/10.1016/j.comnet.2024.110197)

## Proje kapsamı ve durum

Önerilen minimum kapsam, dört güven girdisinden üç bulanık motorla nihai sunucu güven puanı üretmek. Makaleye özel MRR ve Şekil 7(c) deneyinin uyarlanmış biçiminin kabulü teyit bekliyor. [Makale analizi, 17 kural ve deney taslağı](docs/paper-analysis.md) uygulamanın kapsamını açıklar.

Yönergede Classroom teslimi 27 Ekim 2026, sunum başlangıcı 3 Kasım 2026 olarak belirtiliyor. Güncel teslim takvimi ve varsa ek süre teyit bekliyor.

## Geliştirme ortamı

Python 3.13.1 ile doğrulandı. Harici paket gerekmiyor. PowerShell ile proje klasöründe:

```powershell
python -m venv --without-pip .venv
.\.venv\Scripts\python.exe -c "from src.fuzzy import infer; from src.rules import PAIR_RULES; print(infer(1.0, 0.0, PAIR_RULES, include_medium=False))"
```

Bu örnek tek motorda yüksek–düşük → orta kuralını çalıştırır. Beklenen sonuç yaklaşık 0.5.

## İkinci günün model kararları

Girdiler sonlu ve 0–1 aralığında kabul edilir. İlk iki motorda düşük ve yüksek doğrusal omuz fonksiyonları kullanılır. Üçüncü motorun girdileri ve üç motorun çıktıları düşük/yüksek omuzları ve merkezi 0.5 olan üçgen orta üyeliğini kullanır. Tek motor, Mamdani min–max çıkarımı ve 0–1 aralığında 1001 örnekli ağırlık merkezi hesaplar. Bunlar bu uygulamanın sayısal modelleme seçimleridir. Dilsel kurallar doğrudan makalenin Tablo 4'ünden gelir. İlk iki motor aynı dört kuralı paylaştığı için kodda tek tablo kullanılır.

[Literatür notları](docs/related-work.md) makalenin yöntemini ilgili çalışmalarla karşılaştırır.

## Referans güven modelini çalıştırma

Dört girdiyi DT, RT, IT ve TT sırasıyla ver. Komut iki ara güven puanını ve nihai puanı gösterir.

```powershell
.\.venv\Scripts\python.exe -m src.trust 0.9 0.8 0.7 0.6
```

Elle seçilen örnek girdilerle ilk doğrulama:

| DT, RT, IT, TT | FO1 | FO2 | FO3 |
|---|---:|---:|---:|
| 0, 0, 0, 0 | 0.166333 | 0.166333 | 0.180236 |
| 1, 0, 1, 0 | 0.500000 | 0.500000 | 0.166333 |
| 1, 1, 1, 1 | 0.833667 | 0.833667 | 0.585943 |

İkinci satır Tablo 4'teki orta–orta → düşük kuralını gösterir. Üçüncü satırda ara puanlar üçüncü motorun hem orta hem yüksek üyeliklerini etkinleştirir.

## Şekil 7(c) senaryosunun sentetik uyarlaması

```powershell
.\.venv\Scripts\python.exe -m experiments.baseline.failure_rate
```

Her koşulda üç MEC sunucusu, birer istek gönderen 100 cihaz ve 30 tekrar vardır. Yetkisiz cihaz sayısı 0 ile 100 arasında 20'şer artırılır. İki politika aynı cihaz etiketlerini ve başarısızlık için aynı rastgele çekilişleri kullanır. Güvene dayalı politika her isteği en yüksek FO3 puanlı sunucuya, kontrol politikası istekleri sunuculara sırayla gönderir. Oran, başarısız istek sayısının gönderilen 100 isteğe bölünmesiyle hesaplanır. Varsayılan tohum 42'dir. [Üretilen sonuç tablosu](results/tables/failure-rate.md)

Makalede Şekil 7(c) için önerilen sistemde ortalama %15, SHA-256 tabanlı karşılaştırmada %64 başarısızlık bildirilir. Sentetik deneyde de yetkisiz cihaz sayısı arttıkça başarısızlık oranı artar. Bu eğilim, yetkisiz cihazlara daha yüksek başarısızlık olasılığı atanmasından kaynaklanır. Yüksek güven profiline daha düşük başarısızlık olasılığı atanması da güvene göre seçimi avantajlı kılar. Bu nedenle deney, varsayılan koşullarda aktarım davranışını gösterir. Makaledeki oranları doğrulamak için kimlik doğrulama, SARSA, SHA-256 karşılaştırma kolu ve ağ benzetimi gibi bileşenler gerekir. Deneyde sabit sunucu profilleri ve sınırsız kapasite kullanılır. Uyarlamanın MRR kapsamında kabulü teyit bekliyor.

## Alternatif üyelik fonksiyonları

```powershell
.\.venv\Scripts\python.exe -m src.trust 0.9 0.8 0.7 0.6 --smooth
```

Alternatif sürüm üç motorda da her üyelik derecesi μ için μ²(3 − 2μ) uygular. Dönüşüm 0, 0.5 ve 1 derecelerini sabit tutup ara derecelerde doğrusal eğimleri kübik eğrilere dönüştürür. Kural tabanı, çıkarım ve durulaştırma iki sürümde ortaktır. Özgün katkı deneyinde iki sürüm aynı gürültülü girdilerle karşılaştırılacak.

## Gürültü dayanıklılığı deneyi

Deneyi yeniden çalıştırmak için pip içeren bir ortamda deney bağımlılığını kur.

```powershell
python -m venv .venv-experiments
.\.venv-experiments\Scripts\python.exe -m pip install -r requirements-experiments.txt
.\.venv-experiments\Scripts\python.exe -m experiments.proposed.noise_robustness
```

Sentetik aktarım deneyindeki üç sabit sunucu profili kullanıldı. Her gürültü seviyesinde 200 tekrar yapıldı. Dört girdinin her birine sıfır ortalamalı Gauss gürültüsü eklendi ve sonuçlar [0, 1] aralığına kırpıldı. Tohum 42 ile üretilen aynı standart normal çekilişler iki modelde ve tüm seviyelerde kullanıldı. Her modelin gürültülü FO3 puanları kendi gürültüsüz puanlarına göre değerlendirildi. Eşit puanlarda listedeki ilk sunucu seçildi.

Test edilen pozitif gürültü seviyelerinin tamamında doğrusal modelin ortalama mutlak FO3 sapması daha düşüktü. Örneğin σ = 0,15 seviyesinde ortalama sapma doğrusal modelde 0,038338, kübik modelde 0,047606 oldu. Her modelde gürültüsüz durumda seçilen sunucu, bu seviyede 200 tekrarın birinde değişti (%0,5). Diğer seviyelerde iki modelde de seçim değişmedi. Bu gözlemler üç sabit profile ve kullanılan gürültü düzenine dayanıyor. Özellikle birbirine yakın güven puanlı sunucular için seçim kararlılığı ayrı bir deney gerektirir.

[Sonuç tablosu](results/tables/noise-robustness.csv) · [Karşılaştırma grafiği](results/figures/noise-robustness.png)

## Rapor, sunum ve demo

- [Teknik rapor](report/report.pdf)
- [Sunum](presentation/presentation.pdf)
- [Canlı demo ve savunma akışı](presentation/demo.md)
