# Düzenleme sonrası anlık test kontrolü

2026-11-25/26 · `qwen3.6:35b-a3b` · bağlam 32K · süre sınırı 1200 sn · 30 adım · `--sadece zc_peek,zm_windowed_adim`

Kollar aynı oturumda dönüşümlü koştu (`KOD_AJANI_ANLIK=0` / `1`, 3 tur: kapalı-açık, açık-kapalı, kapalı-açık). OneDrive ve Android emülatörü işlemciyi paylaşıyordu; süreler yalnız bu ölçüm içinde karşılaştırılır.

**Ne yapıyor:** Model bir `.py` dosyasını düzenleyince, turun başında bulunan ve 60 sn içinde biten test komutu sessizce yeniden çalışır. Önceden geçip şimdi bozulan testler düzenleme sonucuna kısa bir `[Note]` olarak eklenir (sert hata değil; çok dosyalı değişikliğin ortasında beklenebileceği söylenir). Bir koşu 60 sn'yi aşarsa o tur kapanır.

| Görev | Kapalı | Açık |
|---|---|---|
| zm_windowed_adim | 0/3 | **2/3** |
| zc_peek | 3/3 | 1/3 |
| Toplam | 3/6 | 3/6 |

Aynı oturumdaki önceki ölçümle (`qwen32k-uzun`, kontrol yoktu) kapalı kol `zm_windowed_adim` 0/6, `zc_peek` 5/6 olur. Örnek küçük; hiçbir fark anlamlı değil (2/3 - 0/6: Fisher p = 0,08).

**zm_windowed_adim:** Açık kolda model ilk düzenlemeden hemen sonra "önceden geçen 2-8 test şimdi bozuk" notunu gördü ve projenin testlerine göre düzeltti. Kapalı kolda yine kendi yazdığı denemeyle "geçti" deyip bitirdi; bitişteki otomatik test hatayı geç yakaladı. Düşünme sınırına çarpma: kapalı 5, açık 1. Bir test koşusu ~10 sn; 70 sn süren bir koşuda kontrol kendini kapattı.

**zc_peek:** Açık koldaki iki kayıpta model ilk düzenlemeden önce 20-28 adım okuma yaptı ve 30 adım bitti. Not yalnız ilk düzenlemeden sonra eklendiği için bu okumayı etkileyemez (o ana kadar istem iki kolda aynı). Notların hepsi "bozulan yok" idi (0,8 sn). Bu görevde zaman yine istemi baştan okumaya gidiyor (205-521 sn); sıradaki iş bunu hedefliyor.

**Karar:** Anlık kontrol varsayılan açık. Bozulan testleri sayan kod unittest özet satırını ("FAILED (failures=6, skipped=5)") test adı sanıyordu; düzeltildi.
