# Ölçüm: zor-gpt-oss-3

2026-11-23 10:16 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 2/9 (%22)**, %95 güven aralığı %6–%55

Ortanca süre 62.5 sn, toplam 702 sn, zaman aşımı 0. Tamamlanan tur 5/9. Başarısız olup bunu söylemeyen 3. Gereksiz dosya değiştiren 1.

| Tür | Başarı |
|---|---|
| zor_buyuk | 0/2 |
| zor_iki | 1/1 |
| zor_ozellik | 0/3 |
| zor_uzak | 1/2 |
| zor_yaniltici | 0/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| zc_anahtar | zor_uzak | ✅ | 60.8 | 18 |  |
| zc_peek | zor_ozellik | ❌ | 62.5 | 21 | başarısızlığı söylemedi; AttributeError: 'LRUCache' object has no attribute 'peek' |
| zc_istatistik | zor_yaniltici | ❌ | 66.2 | 30 | tur tamamlanmadı; AssertionError: Tuples differ: (1, 2) != (2, 1) |
| zm_chunked_none | zor_uzak | ❌ | 59.5 | 17 | başarısızlığı söylemedi; gereksiz dosya: more_itertools/more.py; AssertionError: Lists differ: [] != [0, 1, 2] |
| zm_running_sum | zor_ozellik | ❌ | 77.1 | 28 | tur tamamlanmadı; ImportError: cannot import name 'running_sum' from 'more_itertools' (/work/more_itertools/ |
| zm_windowed_adim | zor_buyuk | ❌ | 178.2 | 28 | tur tamamlanmadı; AssertionError: Lists differ: [(1, 2), (2, 3), (3, 4), (4, None)] != [(1, 2), (2, 3), (3,  |
| zk_envvar_oncelik | zor_buyuk | ❌ | 113.4 | 28 | başarısızlığı söylemedi; AssertionError: 'map' != 'env' |
| zk_iki_hata | zor_iki | ✅ | 42.8 | 16 |  |
| zk_yeni_tip | zor_ozellik | ❌ | 41.9 | 29 | tur tamamlanmadı; AttributeError: PERCENT |
