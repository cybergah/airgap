# Ölçüm: zor-gpt-oss-2

2026-11-23 09:42 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 4/9 (%44)**, %95 güven aralığı %19–%73

Ortanca süre 63.1 sn, toplam 622 sn, zaman aşımı 0. Tamamlanan tur 5/9. Başarısız olup bunu söylemeyen 1. Gereksiz dosya değiştiren 2.

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
| zc_anahtar | zor_uzak | ✅ | 35.6 | 10 |  |
| zc_peek | zor_ozellik | ❌ | 62.2 | 26 | tur tamamlanmadı; AttributeError: 'LRUCache' object has no attribute 'peek' |
| zc_istatistik | zor_yaniltici | ❌ | 126.8 | 30 | gereksiz dosya: cachetools/__init__.py, tests/__init__.py; tur tamamlanmadı; AssertionError: Tuples differ: (1, 2) != (2, 1) |
| zm_chunked_none | zor_uzak | ❌ | 64.0 | 18 | başarısızlığı söylemedi; gereksiz dosya: more_itertools/more.py; AssertionError: Lists differ: [] != [0, 1, 2] |
| zm_running_sum | zor_ozellik | ❌ | 97.7 | 24 | model hatası veya boş yanıt; ImportError: cannot import name 'running_sum' from 'more_itertools' (/work/more_itertools/ |
| zm_windowed_adim | zor_buyuk | ✅ | 63.1 | 12 |  |
| zk_envvar_oncelik | zor_buyuk | ✅ | 51.2 | 17 | test değiştirmek istedi |
| zk_iki_hata | zor_iki | ✅ | 41.5 | 19 |  |
| zk_yeni_tip | zor_ozellik | ❌ | 80.0 | 24 | model hatası veya boş yanıt; AttributeError: PERCENT |
