# Ölçüm: gptkilit-eski-1

2026-11-24 17:14 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 5/9 (%56)**, %95 güven aralığı %27–%81

Ortanca süre 62.9 sn, toplam 650 sn, zaman aşımı 0. Tamamlanan tur 5/9. Başarısız olup bunu söylemeyen 1. Gereksiz dosya değiştiren 2.

| Tür | Başarı |
|---|---|
| zor_buyuk | 2/2 |
| zor_iki | 1/1 |
| zor_ozellik | 0/3 |
| zor_uzak | 1/2 |
| zor_yaniltici | 1/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| zc_anahtar | zor_uzak | ✅ | 72.3 | 19 |  |
| zc_peek | zor_ozellik | ❌ | 53.6 | 19 | başarısızlığı söylemedi; AssertionError: 'a' unexpectedly found in LRUCache({'a': 1, 'c': 3}, maxsize=2, currsize=2 |
| zc_istatistik | zor_yaniltici | ✅ | 62.9 | 30 | gereksiz dosya: cachetools/__init__.py, sitecustomize.py; tur tamamlanmadı |
| zm_chunked_none | zor_uzak | ❌ | 86.3 | 29 | gereksiz dosya: more_itertools/more.py; tur tamamlanmadı; AssertionError: Lists differ: [] != [0, 1, 2] |
| zm_running_sum | zor_ozellik | ❌ | 148.3 | 27 | model hatası veya boş yanıt; AttributeError: module 'more_itertools.recipes' has no attribute 'running_sum'. Did you me |
| zm_windowed_adim | zor_buyuk | ✅ | 47.1 | 14 |  |
| zk_envvar_oncelik | zor_buyuk | ✅ | 55.3 | 17 |  |
| zk_iki_hata | zor_iki | ✅ | 41.4 | 19 |  |
| zk_yeni_tip | zor_ozellik | ❌ | 82.7 | 30 | tur tamamlanmadı; AttributeError: PERCENT |
