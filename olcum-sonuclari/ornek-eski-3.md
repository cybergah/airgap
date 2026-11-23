# Ölçüm: ornek-eski-3

2026-11-23 17:21 · model `qwen3.6:35b-a3b` · 1 tekrar · harita 1000

**Başarı: 5/9 (%56)**, %95 güven aralığı %27–%81

Ortanca süre 188.3 sn, toplam 2360 sn, zaman aşımı 0. Tamamlanan tur 6/9. Başarısız olup bunu söylemeyen 1. Gereksiz dosya değiştiren 0.

| Tür | Başarı |
|---|---|
| zor_buyuk | 1/2 |
| zor_iki | 1/1 |
| zor_ozellik | 1/3 |
| zor_uzak | 2/2 |
| zor_yaniltici | 0/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| zc_anahtar | zor_uzak | ✅ | 84.7 | 19 |  |
| zc_peek | zor_ozellik | ❌ | 448.3 | 32 | tur tamamlanmadı; AttributeError: 'LRUCache' object has no attribute 'peek' |
| zc_istatistik | zor_yaniltici | ❌ | 400.8 | 16 | model hatası veya boş yanıt; AssertionError: Tuples differ: (1, 2) != (2, 1) |
| zm_chunked_none | zor_uzak | ✅ | 125.6 | 19 |  |
| zm_running_sum | zor_ozellik | ❌ | 177.0 | 30 | test değiştirmek istedi; başarısızlığı söylemedi; FAILED (failures=1) |
| zm_windowed_adim | zor_buyuk | ❌ | 545.1 | 6 | model hatası veya boş yanıt; FAILED (failures=1) |
| zk_envvar_oncelik | zor_buyuk | ✅ | 188.3 | 18 |  |
| zk_iki_hata | zor_iki | ✅ | 161.6 | 21 |  |
| zk_yeni_tip | zor_ozellik | ✅ | 228.4 | 26 |  |
