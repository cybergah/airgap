# Ölçüm: gptadim-a30-3

2026-11-24 01:08 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 2/9 (%22)**, %95 güven aralığı %6–%55

Ortanca süre 54.6 sn, toplam 537 sn, zaman aşımı 0. Tamamlanan tur 5/9. Başarısız olup bunu söylemeyen 2. Gereksiz dosya değiştiren 1.

| Tür | Başarı |
|---|---|
| zor_buyuk | 1/2 |
| zor_iki | 0/1 |
| zor_ozellik | 0/3 |
| zor_uzak | 1/2 |
| zor_yaniltici | 0/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| zc_anahtar | zor_uzak | ✅ | 35.3 | 13 |  |
| zc_peek | zor_ozellik | ❌ | 64.7 | 28 | tur tamamlanmadı; AttributeError: 'LRUCache' object has no attribute 'peek' |
| zc_istatistik | zor_yaniltici | ❌ | 54.6 | 29 | tur tamamlanmadı; AssertionError: Tuples differ: (1, 2) != (2, 1) |
| zm_chunked_none | zor_uzak | ❌ | 47.3 | 18 | başarısızlığı söylemedi; gereksiz dosya: more_itertools/more.py; AssertionError: Lists differ: [] != [0, 1, 2] |
| zm_running_sum | zor_ozellik | ❌ | 98.9 | 27 | model hatası veya boş yanıt; AttributeError: module 'more_itertools.recipes' has no attribute 'running_min'. Did you me |
| zm_windowed_adim | zor_buyuk | ✅ | 39.6 | 8 |  |
| zk_envvar_oncelik | zor_buyuk | ❌ | 64.6 | 30 | AssertionError: 'map' != 'env' |
| zk_iki_hata | zor_iki | ❌ | 38.6 | 19 | başarısızlığı söylemedi; AssertionError: -1 != 1 |
| zk_yeni_tip | zor_ozellik | ❌ | 93.1 | 26 | model hatası veya boş yanıt; AttributeError: PERCENT |
