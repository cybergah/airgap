# Ölçüm: gptokuma-eski-2

2026-11-24 06:09 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 4/9 (%44)**, %95 güven aralığı %19–%73

Ortanca süre 66.6 sn, toplam 593 sn, zaman aşımı 0. Tamamlanan tur 6/9. Başarısız olup bunu söylemeyen 2. Gereksiz dosya değiştiren 1.

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
| zc_anahtar | zor_uzak | ✅ | 36.9 | 11 |  |
| zc_peek | zor_ozellik | ❌ | 86.7 | 27 | model hatası veya boş yanıt; AssertionError: 'a' unexpectedly found in LRUCache({'a': 1, 'c': 3}, maxsize=2, currsize=2 |
| zc_istatistik | zor_yaniltici | ❌ | 53.0 | 29 | tur tamamlanmadı; AssertionError: Tuples differ: (1, 2) != (2, 1) |
| zm_chunked_none | zor_uzak | ❌ | 90.3 | 23 | başarısızlığı söylemedi; gereksiz dosya: more_itertools/more.py; AssertionError: Lists differ: [] != [0, 1, 2] |
| zm_running_sum | zor_ozellik | ❌ | 66.6 | 17 | başarısızlığı söylemedi; ImportError: cannot import name 'running_sum' from 'more_itertools' (/work/more_itertools/ |
| zm_windowed_adim | zor_buyuk | ✅ | 51.2 | 10 |  |
| zk_envvar_oncelik | zor_buyuk | ✅ | 52.0 | 18 |  |
| zk_iki_hata | zor_iki | ✅ | 88.4 | 30 |  |
| zk_yeni_tip | zor_ozellik | ❌ | 68.3 | 28 | model hatası veya boş yanıt; AttributeError: PERCENT |
