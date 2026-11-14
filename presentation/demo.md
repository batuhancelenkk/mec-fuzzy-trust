# Canlı demo ve savunma

## Sunum akışı

| Slaytlar | Süre | Konu |
|---|---:|---|
| 1–3 | 4 dk | MEC problemi, güven ihtiyacı ve ilgili çalışmalar |
| 4–5 | 4 dk | Üç motor, Tablo 4, üyelik ve durulaştırma |
| 6–7 | 4 dk | Sentetik aktarım ve gürültü deneyinin düzeni |
| 8–9 | 4 dk | Ölçülen sonuçlar ve sınırlılıklar |
| 10–11 | 1 dk | Demo senaryosu ve kaynaklar |

Sunumdan sonraki yaklaşık 5 dakikada canlı çalıştırma ve soru-cevap yap.

## Demo komutları

Proje kökünden PowerShell ile çalıştır.

```powershell
python -m src.trust 0.9 0.8 0.7 0.6
python -m src.trust 0.9 0.8 0.7 0.6 --smooth
python -m src.trust 1 0 1 0
```

| Örnek | FO1 | FO2 | FO3 |
|---|---:|---:|---:|
| Doğrusal | 0,668052 | 0,559938 | 0,415912 |
| Kübik | 0,751271 | 0,593313 | 0,502083 |
| İki ara puan orta | 0,500000 | 0,500000 | 0,166333 |

Üçüncü örnekte her iki giriş çifti de yüksek ve düşükten oluşur. Bu yüzden ilk iki motor orta puan verir. Üçüncü motorda orta–orta → düşük kuralı çalışır. Düşük çıktı kümesinin ağırlık merkezi 0,166333’tür.

## Savunma soruları

- **Neden FO3 puanları farklı?** Kübik dönüşüm kısmi üyelikleri değiştirir. Bunun sonucunda kuralların etkinlik düzeyleri ve çıktı eğrisinin ağırlık merkezi değişir.
- **Kübik model daha iyi mi?** Deneyde doğrusal modelin puan sapması daha düşüktü. Seçim değişim oranı ölçülen tüm seviyelerde eşitti. Bulgular üç sabit sunucu profiline dayanıyor.
- **Şekil 7(c) ile doğrudan kıyas yapılabilir mi?** Orijinal ağ deneyi kimlik doğrulama ve SARSA içerir. Uyarlama, sabit sunucu profilleri ve atanmış başarısızlık olasılıklarıyla deneyin eğilimini inceler. Bu nedenle sayısal farkın yorumu koşullarla sınırlı.
