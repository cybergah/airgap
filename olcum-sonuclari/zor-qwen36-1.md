# Ölçüm: zor-qwen36-1

2026-11-23 08:53 · model `qwen3.6:35b-a3b` · 1 tekrar · harita 1000

**Başarı: 4/9 (%44)**, %95 güven aralığı %19–%73

Ortanca süre 304.8 sn, toplam 2265 sn, zaman aşımı 0. Tamamlanan tur 5/9. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 1.

| Tür | Başarı |
|---|---|
| zor_buyuk | 1/2 |
| zor_iki | 1/1 |
| zor_ozellik | 1/3 |
| zor_uzak | 1/2 |
| zor_yaniltici | 0/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| zc_anahtar | zor_uzak | ✅ | 100.1 | 16 |  |
| zc_peek | zor_ozellik | ❌ | 376.2 | 34 | tur tamamlanmadı; AttributeError: 'LRUCache' object has no attribute 'peek' |
| zc_istatistik | zor_yaniltici | ❌ | 313.3 | 12 | model hatası veya boş yanıt; AssertionError: Tuples differ: (1, 2) != (2, 1) |
| zm_chunked_none | zor_uzak | ❌ | 319.8 | 30 | gereksiz dosya: more_itertools/more.py; tur tamamlanmadı; AssertionError: Lists differ: [] != [[1, 2], [3, 4], [5]] |
| zm_running_sum | zor_ozellik | ❌ | 304.8 | 38 | test değiştirmek istedi; FAILED (failures=1) |
| zm_windowed_adim | zor_buyuk | ❌ | 395.0 | 1 | model hatası veya boş yanıt; FAILED (failures=1) |
| zk_envvar_oncelik | zor_buyuk | ✅ | 167.8 | 19 |  |
| zk_iki_hata | zor_iki | ✅ | 92.0 | 18 |  |
| zk_yeni_tip | zor_ozellik | ✅ | 196.4 | 26 |  |
