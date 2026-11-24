# Ölçüm: gptokuma-eski-1

2026-11-24 05:45 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 4/9 (%44)**, %95 güven aralığı %19–%73

Ortanca süre 52.4 sn, toplam 506 sn, zaman aşımı 0. Tamamlanan tur 4/9. Başarısız olup bunu söylemeyen 1. Gereksiz dosya değiştiren 2.

| Tür | Başarı |
|---|---|
| zor_buyuk | 2/2 |
| zor_iki | 0/1 |
| zor_ozellik | 1/3 |
| zor_uzak | 1/2 |
| zor_yaniltici | 0/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| zc_anahtar | zor_uzak | ✅ | 62.2 | 24 | gereksiz dosya: cachetools/__init__.py, tests/__init__.py; model hatası veya boş yanıt |
| zc_peek | zor_ozellik | ❌ | 64.2 | 28 | tur tamamlanmadı; AttributeError: 'LRUCache' object has no attribute 'peek' |
| zc_istatistik | zor_yaniltici | ❌ | 52.2 | 29 | tur tamamlanmadı; AssertionError: Tuples differ: (1, 2) != (2, 1) |
| zm_chunked_none | zor_uzak | ❌ | 86.8 | 26 | gereksiz dosya: more_itertools/more.py; model hatası veya boş yanıt; AssertionError: Lists differ: [] != [0, 1, 2] |
| zm_running_sum | zor_ozellik | ❌ | 40.5 | 30 | tur tamamlanmadı; ImportError: cannot import name 'running_sum' from 'more_itertools' (/work/more_itertools/ |
| zm_windowed_adim | zor_buyuk | ✅ | 52.4 | 12 |  |
| zk_envvar_oncelik | zor_buyuk | ✅ | 50.4 | 19 |  |
| zk_iki_hata | zor_iki | ❌ | 56.6 | 19 | başarısızlığı söylemedi; AssertionError: 11 != 9 |
| zk_yeni_tip | zor_ozellik | ✅ | 40.3 | 19 |  |
