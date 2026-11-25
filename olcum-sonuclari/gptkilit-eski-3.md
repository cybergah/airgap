# Ölçüm: gptkilit-eski-3

2026-11-24 18:26 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 4/9 (%44)**, %95 güven aralığı %19–%73

Ortanca süre 66.0 sn, toplam 768 sn, zaman aşımı 0. Tamamlanan tur 4/9. Başarısız olup bunu söylemeyen 1. Gereksiz dosya değiştiren 1.

| Tür | Başarı |
|---|---|
| zor_buyuk | 1/2 |
| zor_iki | 1/1 |
| zor_ozellik | 0/3 |
| zor_uzak | 1/2 |
| zor_yaniltici | 1/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| zc_anahtar | zor_uzak | ✅ | 26.2 | 15 |  |
| zc_peek | zor_ozellik | ❌ | 101.5 | 29 | tur tamamlanmadı; AssertionError: 'a' unexpectedly found in LRUCache({'a': 1, 'c': 3}, maxsize=2, currsize=2 |
| zc_istatistik | zor_yaniltici | ✅ | 54.4 | 27 |  |
| zm_chunked_none | zor_uzak | ❌ | 94.9 | 19 | başarısızlığı söylemedi; gereksiz dosya: more_itertools/more.py; AssertionError: Lists differ: [] != [0, 1, 2] |
| zm_running_sum | zor_ozellik | ❌ | 61.2 | 30 | tur tamamlanmadı; ImportError: cannot import name 'running_sum' from 'more_itertools' (/work/more_itertools/ |
| zm_windowed_adim | zor_buyuk | ❌ | 217.1 | 29 | model hatası veya boş yanıt; AssertionError: Lists differ: [(0, 1, 2), (2, 3, 4)] != [(0, 1, 2), (2, 3, 4), (4, 5, None |
| zk_envvar_oncelik | zor_buyuk | ✅ | 66.0 | 27 | tur tamamlanmadı |
| zk_iki_hata | zor_iki | ✅ | 50.4 | 23 |  |
| zk_yeni_tip | zor_ozellik | ❌ | 96.1 | 28 | model hatası veya boş yanıt; AttributeError: PERCENT |
