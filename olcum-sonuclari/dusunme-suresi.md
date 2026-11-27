# Süreli düşünme sınırı (120 sn) ve devam notu

2026-11-26 · `qwen3.6:35b-a3b` · bağlam 32K · süre sınırı 1200 sn · 30 adım · anlık kontrol açık · kırpma 0.6 · `--sadece zc_peek,zm_windowed_adim`

Kollar aynı oturumda dönüşümlü koştu (`KOD_AJANI_DUSUNME_SN=0` eski: 30.000 harf + eski not / `120` yeni: 120 sn + devam notu; 3 tur: eski-yeni, yeni-eski, eski-yeni).

| | Eski (harf) | Yeni (120 sn) |
|---|---|---|
| zc_peek başarı | 3/3 | 2/3 |
| zm_windowed_adim başarı | 3/3 | 2/3 |
| **Toplam** | **6/6** | 4/6 |
| Sınıra takılma (windowed) | 2 / 3 / 3 | 2 / 0 / 3 |
| Kesilen düşüncenin süresi | 111-189 sn | 120 sn |
| Kesintiden sonraki adımın düşüncesi | 20-25 bin harf | 0-9 bin harf |
| windowed süreleri | 584 / 962 / 1018 sn | 457 / 82 / 953 sn |
| zc_peek süreleri | 318 / 194 / 138 sn | 292 / 181 / 227 sn |

**Varsayım düzeltmesi:** 30.000 harfin Qwen'de ~5 dk sürdüğünü sanıyordum; ölçülen 111-189 sn. Yeni sınır eskisinden yalnız ~%20-35 kısa, yani iki kol beklenenden çok daha yakın.

**Devam notu işe yarıyor:** Eski notla kesintiden sonraki adım yine 20-25 bin harf düşündü (aynı döngü). Yeni notla sonraki adım 0-9 bin harf düşünüp araç çağırdı.

**Kayıplar:**
- `zc_peek` yeni-3: düşünme sınırına hiç takılmadı; 30 adım bitti, sonuç `KeyError: 'x'` (önceki ölçümde eski kolda da görülen hata). Sınırla ilgisi yok.
- `zm_windowed_adim` yeni-3: üçüncü kesintide tur durdu, düzeltme yarımdı.

**Asıl bulgu:** Tur "art arda 3 kez" değil, turdaki **toplam** 3 kesintide duruyor (sayaç başarılı cevaptan sonra sıfırlanmıyor). Eski kolun windowed 2 ve 3. koşuları da bu kuralla durdu; düzeltme o ana kadar bitmiş olduğu için geçti. eski-3'te üçüncü kesinti 19. adımda, ilerleyen bir turu kesti.

**Sonuç:** Temiz değil. Başarıdaki fark anlamlı değil (6/6 - 4/6: Fisher p = 0,45), ama yeni kol daha iyi de değil. Önce sayaç düzeltilip yeniden ölçüldü.

## İkinci ölçüm: sayaç düzeltildi, iki kolda da yeni not

Sayaç artık başarılı bir cevapta sıfırlanıyor; tur yalnız **art arda** 3 kesintide duruyor. Devam notu iki kolda da aynı, tek fark sınırın türü. Aynı ayarlar, 3 tur dönüşümlü.

| | Eski (harf) | Yeni (120 sn) |
|---|---|---|
| zc_peek başarı | 2/3 | 2/3 |
| zm_windowed_adim başarı | 1/3 | 2/3 |
| **Toplam** | 3/6 | 4/6 |
| Kesilen düşüncenin süresi | 118-189 sn | 120 sn |

- **zc_peek:** İki koldaki kayıpta da model düşünme sınırına hiç takılmadı (30 adım bitti, sonuç yanlış). Sınırla ilgisi yok.
- **zm_windowed_adim:** İki koldaki birer kayıp ilk adımda art arda 3 kesintiyle geldi; model ilk adımı geçemedi (kısa düşünme ile yeniden denemeler de kesildi). Eski koldaki ikinci kayıpta tur 4. kesintiden sonra art arda 3 kesintiyle durdu.
- **Sayaç düzeltmesi işe yaradı:** yeni-1'de 3 kesinti aralıklıydı; eski kural turu 3. kesintide durdururdu, bu sefer tur sürdü ve görev geçti. eski-3'te de tur eski kuralın duracağı yerden ileri gitti.

**İki ölçüm birlikte:** harf 9/12, 120 sn 8/12. 120 sn belirgin kazanç sağlamadı.

**Karar:** Süreli sınır kaldırıldı. Yeni devam notu da v0.15 ile dönüşümlü tam set ölçümünde kazanç göstermediği için geri alındı (24/27 - 27/27, `v016-karsilastirma.md`); eski not geçerli. Kalan tek değişiklik sayaç düzeltmesi: gerçek bir kod hatasıydı, birim testiyle korunuyor.
