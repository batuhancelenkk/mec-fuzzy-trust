# MEC Sunucu Güveninin Bulanık Mantıkla Değerlendirilmesi

Bulanık Mantık dersi dönem projesi. Amaç, Ali ve arkadaşlarının MEC sunucu güven modelini yeniden kurmak ve üyelik fonksiyonu seçiminin ölçüm gürültüsü altındaki etkisini incelemek.

## Referans makale

B. Ali, M. A. Gregory, S. Li ve O. A. Dib, “Implementing zero trust security with dual fuzzy methodology for trust-aware authentication and task offloading in Multi-access Edge Computing,” *Computer Networks*, cilt 241, makale 110197, 2024. [DOI](https://doi.org/10.1016/j.comnet.2024.110197)

## Proje kapsamı ve durum

Önerilen minimum kapsam, dört güven girdisinden üç bulanık motorla nihai sunucu güven puanı üretmek. Makaleye özel MRR ve Şekil 7(c) deneyinin uyarlanmış biçiminin kabulü teyit bekliyor. İlk günün çıktısı [makale analizi, 17 kural ve deney taslağı](docs/paper-analysis.md). Python uygulaması ve çalıştırma komutları sonraki aşamada eklenecek.

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
