# Ölçüm: gptsembol-yeni-1

2026-11-24 02:01 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 3/9 (%33)**, %95 güven aralığı %12–%65

Ortanca süre 62.4 sn, toplam 498 sn, zaman aşımı 0. Tamamlanan tur 4/9. Başarısız olup bunu söylemeyen 1. Gereksiz dosya değiştiren 2.

| Tür | Başarı |
|---|---|
| zor_buyuk | 1/2 |
| zor_iki | 1/1 |
| zor_ozellik | 0/3 |
| zor_uzak | 1/2 |
| zor_yaniltici | 0/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| zc_anahtar | zor_uzak | ✅ | 29.1 | 10 |  |
| zc_peek | zor_ozellik | ❌ | 68.4 | 29 | tur tamamlanmadı; AttributeError: 'LRUCache' object has no attribute 'peek' |
| zc_istatistik | zor_yaniltici | ❌ | 57.3 | 28 | gereksiz dosya: sitecustomize.py; tur tamamlanmadı; AssertionError: Tuples differ: (1, 2) != (2, 1) |
| zm_chunked_none | zor_uzak | ❌ | 62.4 | 19 | başarısızlığı söylemedi; gereksiz dosya: more_itertools/more.py; AssertionError: Lists differ: [] != [0, 1, 2] |
| zm_running_sum | zor_ozellik | ❌ | 97.4 | 26 | model hatası veya boş yanıt; AttributeError: module 'more_itertools.recipes' has no attribute 'running_sum'. Did you me |
| zm_windowed_adim | zor_buyuk | ✅ | 42.5 | 9 |  |
| zk_envvar_oncelik | zor_buyuk | ❌ | 10.8 | 7 | model hatası veya boş yanıt; AssertionError: 'map' != 'env' |
| zk_iki_hata | zor_iki | ✅ | 66.2 | 22 |  |
| zk_yeni_tip | zor_ozellik | ❌ | 64.1 | 29 | model hatası veya boş yanıt; AttributeError: PERCENT |
