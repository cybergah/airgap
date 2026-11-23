# Ölçüm: gptornek-yeni-3

2026-11-23 23:32 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 4/9 (%44)**, %95 güven aralığı %19–%73

Ortanca süre 82.3 sn, toplam 645 sn, zaman aşımı 0. Tamamlanan tur 3/9. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 2.

| Tür | Başarı |
|---|---|
| zor_buyuk | 2/2 |
| zor_iki | 0/1 |
| zor_ozellik | 0/3 |
| zor_uzak | 1/2 |
| zor_yaniltici | 1/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| zc_anahtar | zor_uzak | ✅ | 93.9 | 29 | gereksiz dosya: cachetools/__init__.py; model hatası veya boş yanıt |
| zc_peek | zor_ozellik | ❌ | 82.3 | 28 | tur tamamlanmadı; AttributeError: 'LRUCache' object has no attribute 'peek' |
| zc_istatistik | zor_yaniltici | ✅ | 38.4 | 13 |  |
| zm_chunked_none | zor_uzak | ❌ | 98.9 | 27 | gereksiz dosya: more_itertools/more.py; tur tamamlanmadı; AssertionError: Lists differ: [] != [0, 1, 2] |
| zm_running_sum | zor_ozellik | ❌ | 45.9 | 28 | tur tamamlanmadı; ImportError: cannot import name 'running_sum' from 'more_itertools' (/work/more_itertools/ |
| zm_windowed_adim | zor_buyuk | ✅ | 107.7 | 11 |  |
| zk_envvar_oncelik | zor_buyuk | ✅ | 45.7 | 19 |  |
| zk_iki_hata | zor_iki | ❌ | 43.6 | 27 | model hatası veya boş yanıt; AssertionError: 10 != 9 |
| zk_yeni_tip | zor_ozellik | ❌ | 88.6 | 28 | model hatası veya boş yanıt; AttributeError: PERCENT |
