# Önbelleği koruyan kırpma (tek seferde %60)

2026-11-26 · `qwen3.6:35b-a3b` · bağlam 32K · süre sınırı 1200 sn · 30 adım · anlık kontrol açık · `--sadece zc_peek,zm_windowed_adim`

Kollar aynı oturumda dönüşümlü koştu (`KOD_AJANI_KIRPMA_ORANI=1` eski / `0.6` yeni; 3 tur: eski-yeni, yeni-eski, eski-yeni). OneDrive ve Android emülatörü işlemciyi paylaşıyordu; süreler yalnız bu ölçüm içinde karşılaştırılır.

**Ne değişti:** Eski `gecmisi_sigdir` konuşma sınırı her aştığında yalnızca sınırın altına inecek kadar kırpıyordu. Bu yüzden hemen her adımda geçmişin başı biraz değişiyor, Ollama önbelleği bozuluyor ve model 20-24K token'lık istemi baştan okuyordu (Qwen'de 20-100 sn). Yeni hâli sınır aşılınca konuşmayı bir kerede bütçenin ~%60'ına indiriyor; sonraki adımlarda geçmişin başı aynı kaldığı için önbellek tutuyor. En yeni düşünce silinmiyor. Eski davranış `KOD_AJANI_KIRPMA_ORANI=1` ile seçilebilir.

| | Eski kırpma | Yeni kırpma |
|---|---|---|
| zc_peek başarı | 2/3 | **3/3** |
| zm_windowed_adim başarı | 2/3 | 2/3 |
| **Toplam başarı** | 4/6 | **5/6** |
| Tam okuma (ajanın sayacı) | 27 | **13** |
| Tam okuma (>15K istem, >8 sn) | 24 | **3** |
| İstem okuma toplamı | 616 sn | **260 sn** |
| Üretim toplamı | 732 sn | 792 sn |
| Görev süresi toplamı | 2422 sn | 2371 sn |

Görev bazında:

| | zc_peek eski | zc_peek yeni | windowed eski | windowed yeni |
|---|---|---|---|---|
| Tam okuma (sayaç) | 9 / 13 / 3 | 3 / 5 / 3 | 0 / 0 / 2 | 2 / 0 / 0 |
| İstem okuma (sn) | 194 / 297 / 68 | 67 / 82 / 60 | 10 / 3 / 44 | 34 / 10 / 7 |
| Süre (sn) | 370 / 395 / 182 | 175 / 204 / 152 | 163 / 461 / 851 | 842 / 442 / 556 |

**zc_peek:** Kırpmanın asıl hedefi bu görevdi (istem 23-24K'ya çıkıyor). İstem okuma 559 sn'den 209 sn'ye, ortalama görev süresi 316 sn'den 177 sn'ye indi. Eski kolun kaybı 28 adımda `KeyError` ile bitti; yeni kolda üç deneme de geçti.

**zm_windowed_adim:** İstem genelde bütçe altında kaldığı için kırpma pek devreye girmedi (okuma iki kolda da ~50 sn). İki koldaki birer kayıp da düşünme sınırına art arda 3 kez çarpmaktan geldi (her biri ~30.000 harf, Qwen'de ~5 dk); kırpmayla ilgisi yok. Bu, sıradaki maddenin (düşünme sınırını model hızına bağlama) konusu.

**Örnek küçük:** Başarıdaki fark (5/6 - 4/6) anlamlı değil (Fisher p = 1). Ölçülen kazanç istem okuma süresinde ve tam okuma sayısında; yön her zc_peek turunda aynı.

**Karar:** Yeni kırpma varsayılan (`0.6`).
