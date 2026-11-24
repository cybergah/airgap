# Ölçüm: gptadim-ozet-3

2026-11-24 01:35 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 3/9 (%33)**, %95 güven aralığı %12–%65

Ortanca süre 56.0 sn, toplam 754 sn, zaman aşımı 0. Tamamlanan tur 6/9. Başarısız olup bunu söylemeyen 4. Gereksiz dosya değiştiren 2.

| Tür | Başarı |
|---|---|
| zor_buyuk | 1/2 |
| zor_iki | 0/1 |
| zor_ozellik | 0/3 |
| zor_uzak | 1/2 |
| zor_yaniltici | 1/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| zc_anahtar | zor_uzak | ✅ | 20.2 | 10 |  |
| zc_peek | zor_ozellik | ❌ | 32.6 | 18 | başarısızlığı söylemedi; AttributeError: 'LRUCache' object has no attribute 'peek' |
| zc_istatistik | zor_yaniltici | ✅ | 214.0 | 56 | gereksiz dosya: cachetools/__init__.py, tests/__init__.py; model hatası veya boş yanıt |
| zm_chunked_none | zor_uzak | ❌ | 173.4 | 25 | başarısızlığı söylemedi; gereksiz dosya: more_itertools/more.py; AssertionError: Lists differ: [] != [0, 1, 2] |
| zm_running_sum | zor_ozellik | ❌ | 73.7 | 24 | model hatası veya boş yanıt; ImportError: cannot import name 'running_sum' from 'more_itertools' (/work/more_itertools/ |
| zm_windowed_adim | zor_buyuk | ✅ | 51.0 | 10 |  |
| zk_envvar_oncelik | zor_buyuk | ❌ | 80.0 | 27 | başarısızlığı söylemedi; AssertionError: 'map' != 'env' |
| zk_iki_hata | zor_iki | ❌ | 52.7 | 19 | başarısızlığı söylemedi; AssertionError: False is not true |
| zk_yeni_tip | zor_ozellik | ❌ | 56.0 | 30 | tur tamamlanmadı; AttributeError: PERCENT |
