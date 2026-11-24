# Ölçüm: gptadim-a30-1

2026-11-23 23:45 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 4/9 (%44)**, %95 güven aralığı %19–%73

Ortanca süre 65.9 sn, toplam 668 sn, zaman aşımı 0. Tamamlanan tur 4/9. Başarısız olup bunu söylemeyen 1. Gereksiz dosya değiştiren 2.

| Tür | Başarı |
|---|---|
| zor_buyuk | 2/2 |
| zor_iki | 1/1 |
| zor_ozellik | 0/3 |
| zor_uzak | 1/2 |
| zor_yaniltici | 0/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| zc_anahtar | zor_uzak | ✅ | 26.9 | 13 |  |
| zc_peek | zor_ozellik | ❌ | 103.0 | 27 | tur tamamlanmadı; AttributeError: 'LRUCache' object has no attribute 'peek' |
| zc_istatistik | zor_yaniltici | ❌ | 65.9 | 30 | gereksiz dosya: cachetools/__init__.py; tur tamamlanmadı; AssertionError: Tuples differ: (1, 2) != (2, 1) |
| zm_chunked_none | zor_uzak | ❌ | 142.2 | 15 | başarısızlığı söylemedi; gereksiz dosya: more_itertools/more.py; AssertionError: Lists differ: [] != [0, 1, 2] |
| zm_running_sum | zor_ozellik | ❌ | 63.4 | 29 | model hatası veya boş yanıt; AttributeError: module 'more_itertools.recipes' has no attribute 'running_mean'. Did you m |
| zm_windowed_adim | zor_buyuk | ✅ | 116.7 | 27 | model hatası veya boş yanıt |
| zk_envvar_oncelik | zor_buyuk | ✅ | 41.2 | 19 |  |
| zk_iki_hata | zor_iki | ✅ | 31.5 | 17 |  |
| zk_yeni_tip | zor_ozellik | ❌ | 77.7 | 28 | model hatası veya boş yanıt; AttributeError: PERCENT |
