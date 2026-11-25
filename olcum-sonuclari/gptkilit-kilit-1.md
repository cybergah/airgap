# Ölçüm: gptkilit-kilit-1

2026-11-24 17:26 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 3/9 (%33)**, %95 güven aralığı %12–%65

Ortanca süre 63.2 sn, toplam 721 sn, zaman aşımı 0. Tamamlanan tur 2/9. Başarısız olup bunu söylemeyen 1. Gereksiz dosya değiştiren 1.

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
| zc_anahtar | zor_uzak | ✅ | 37.0 | 10 |  |
| zc_peek | zor_ozellik | ❌ | 46.2 | 26 | tur tamamlanmadı; AttributeError: 'LRUCache' object has no attribute 'peek' |
| zc_istatistik | zor_yaniltici | ❌ | 61.6 | 30 | tur tamamlanmadı; AssertionError: Tuples differ: (1, 2) != (2, 1) |
| zm_chunked_none | zor_uzak | ❌ | 65.2 | 18 | başarısızlığı söylemedi; gereksiz dosya: more_itertools/more.py; AssertionError: Lists differ: [] != [0, 1, 2] |
| zm_running_sum | zor_ozellik | ❌ | 74.1 | 27 | model hatası veya boş yanıt; ImportError: cannot import name 'running_sum' from 'more_itertools' (/work/more_itertools/ |
| zm_windowed_adim | zor_buyuk | ❌ | 230.6 | 28 | model hatası veya boş yanıt; AssertionError: Lists differ: [(1, 2), (2, 3), (3, 4), (3, 4)] != [(1, 2), (2, 3), (3, 4)] |
| zk_envvar_oncelik | zor_buyuk | ✅ | 83.3 | 28 | tur tamamlanmadı |
| zk_iki_hata | zor_iki | ✅ | 60.1 | 28 | model hatası veya boş yanıt |
| zk_yeni_tip | zor_ozellik | ❌ | 63.2 | 29 | model hatası veya boş yanıt; AttributeError: PERCENT |
