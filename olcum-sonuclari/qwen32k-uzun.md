# Ölçüm: qwen32k-uzun

2026-11-25 21:56 · model `qwen3.6:35b-a3b` · 3 tekrar · harita 1000

**Başarı: 2/6 (%33)**, %95 güven aralığı %10–%70

Ortanca süre 1200 sn, toplam 6252 sn, zaman aşımı 4. Tamamlanan tur 1/6. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 1.

| Tür | Başarı |
|---|---|
| zor_buyuk | 0/3 |
| zor_ozellik | 2/3 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| zc_peek | zor_ozellik | ❌ | 1200 |  | zaman aşımı |
| zm_windowed_adim | zor_buyuk | ❌ | 1200 |  | zaman aşımı |
| zc_peek | zor_ozellik | ✅ | 429.8 | 39 | model hatası veya boş yanıt |
| zm_windowed_adim | zor_buyuk | ❌ | 1200 |  | zaman aşımı |
| zc_peek | zor_ozellik | ✅ | 1022.2 | 36 | gereksiz dosya: tests/__init__.py |
| zm_windowed_adim | zor_buyuk | ❌ | 1200 |  | zaman aşımı |

## Teşhis: 32K'da zc_peek ve zm_windowed_adim neden kaybediliyor

Koşu: `--baglam 32768 --sure 1200 --sadece zc_peek,zm_windowed_adim --tekrar 3 --iz`. Bu oturumda OneDrive ve Android emülatörü işlemciyi paylaşıyordu; süreler önceki ölçümlerle karşılaştırılmaz, aşağıdaki bulgular kayıtlardaki adımlara dayanır.

Önceki 32K ölçümlerinde (600 sn) bu iki görevdeki kayıpların hepsi zaman aşımıydı; yanlış cevap yoktu. Kazanılan denemeler de 264–557 sn sürmüştü.

**zm_windowed_adim (0/3): yanlış düzeltme kendi yazdığı denemeyle "doğrulanıyor".**
- Model projenin testlerini çalıştırmadı; kısa betiklerle beklenen sonucu kendisi yazdı. Bir denemede kendi çıktısına uysun diye beklentiyi değiştirdi ("`step=3` testi hatalı") ve "Tüm testler geçti" deyip bitirdi.
- Ajanın bitişteki otomatik testi 6 testin bozulduğunu yakaladı (`test_step`, `test_fillvalue_step` ...), ama bu 15–20 dakika sonraydı.
- Üç denemenin üçünde de düşünme 30.000 harf sınırına çarptı (1–2 kez). Sınır ~90 belirteç/sn için hesaplanmış; %40'ı CPU'da çalışan Qwen'de bir çarpma yaklaşık 5 dakika.

**zc_peek (2/3): zamanın yarısı istemi baştan okumak.**
- Başarılı iki denemede istem okuma 210/430 sn, üretim 200/578 sn; 7–8 kez istemin tamamı (20–24 bin belirteç) yeniden okundu.
- Nedeni `gecmisi_sigdir`: geçmiş bağlamın dörtte üçünü geçince yalnız sınırın altına inecek kadar kırpılıyor, birkaç adım sonra yine kırpılıyor; her kırpma Ollama önbelleğini bozuyor.
- Model 6–8 adımını test komutunu bulmaya harcadı (tox, pytest yok, `pip install`, `PYTHONPATH`); bir deneme adım sınırına "NO TESTS RAN" ile geldi.

**Karar (v0.16.0 sırası):** 1) düzenleme sonrası anlık test kontrolü, 2) önbelleği koruyan tek seferlik kırpma, 3) düşünme sınırını model hızına bağlamak. Her biri dönüşümlü ölçülecek.
