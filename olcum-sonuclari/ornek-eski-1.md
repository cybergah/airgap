# Ölçüm: ornek-eski-1

2026-11-23 14:55 · model `qwen3.6:35b-a3b` · 1 tekrar · harita 1000

**Başarı: 7/9 (%78)**, %95 güven aralığı %45–%94

Ortanca süre 195.1 sn, toplam 2059 sn, zaman aşımı 0. Tamamlanan tur 5/9. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 1.

| Tür | Başarı |
|---|---|
| zor_buyuk | 1/2 |
| zor_iki | 1/1 |
| zor_ozellik | 3/3 |
| zor_uzak | 2/2 |
| zor_yaniltici | 0/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| zc_anahtar | zor_uzak | ✅ | 123.6 | 19 |  |
| zc_peek | zor_ozellik | ✅ | 330.2 | 32 | tur tamamlanmadı |
| zc_istatistik | zor_yaniltici | ❌ | 389.4 | 11 | model hatası veya boş yanıt; AssertionError: Tuples differ: (1, 2) != (2, 1) |
| zm_chunked_none | zor_uzak | ✅ | 132.1 | 22 |  |
| zm_running_sum | zor_ozellik | ✅ | 239.6 | 34 | test değiştirmek istedi; gereksiz dosya: README.rst; model hatası veya boş yanıt |
| zm_windowed_adim | zor_buyuk | ❌ | 342.3 | 13 | model hatası veya boş yanıt; FAILED (failures=1) |
| zk_envvar_oncelik | zor_buyuk | ✅ | 165.8 | 19 |  |
| zk_iki_hata | zor_iki | ✅ | 195.1 | 23 |  |
| zk_yeni_tip | zor_ozellik | ✅ | 141.0 | 21 |  |
