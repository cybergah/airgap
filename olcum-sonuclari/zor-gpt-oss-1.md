# Ölçüm: zor-gpt-oss-1

2026-11-23 09:04 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 3/9 (%33)**, %95 güven aralığı %12–%65

Ortanca süre 64.6 sn, toplam 667 sn, zaman aşımı 0. Tamamlanan tur 4/9. Başarısız olup bunu söylemeyen 2. Gereksiz dosya değiştiren 2.

| Tür | Başarı |
|---|---|
| zor_buyuk | 1/2 |
| zor_iki | 0/1 |
| zor_ozellik | 1/3 |
| zor_uzak | 1/2 |
| zor_yaniltici | 0/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| zc_anahtar | zor_uzak | ✅ | 41.3 | 13 |  |
| zc_peek | zor_ozellik | ❌ | 64.6 | 29 | model hatası veya boş yanıt; AttributeError: 'LRUCache' object has no attribute 'peek' |
| zc_istatistik | zor_yaniltici | ❌ | 137.7 | 26 | gereksiz dosya: cachetools/__init__.py; model hatası veya boş yanıt; AssertionError: Tuples differ: (1, 2) != (2, 1) |
| zm_chunked_none | zor_uzak | ❌ | 87.2 | 29 | gereksiz dosya: more_itertools/more.py; tur tamamlanmadı; AssertionError: Lists differ: [] != [0, 1, 2] |
| zm_running_sum | zor_ozellik | ❌ | 85.3 | 26 | model hatası veya boş yanıt; ImportError: cannot import name 'running_sum' from 'more_itertools' (/work/more_itertools/ |
| zm_windowed_adim | zor_buyuk | ✅ | 58.9 | 12 |  |
| zk_envvar_oncelik | zor_buyuk | ❌ | 73.7 | 28 | başarısızlığı söylemedi; AssertionError: 'map' != 'env' |
| zk_iki_hata | zor_iki | ❌ | 58.1 | 22 | başarısızlığı söylemedi; AssertionError: 11 != 9 |
| zk_yeni_tip | zor_ozellik | ✅ | 60.6 | 28 | model hatası veya boş yanıt |
