# Ölçüm: gptkilit-ikisi-2

2026-11-24 18:13 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 3/9 (%33)**, %95 güven aralığı %12–%65

Ortanca süre 47.3 sn, toplam 539 sn, zaman aşımı 0. Tamamlanan tur 6/9. Başarısız olup bunu söylemeyen 2. Gereksiz dosya değiştiren 1.

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
| zc_anahtar | zor_uzak | ✅ | 22.7 | 9 |  |
| zc_peek | zor_ozellik | ❌ | 175.0 | 21 | AssertionError: 'a' unexpectedly found in LRUCache({'a': 1, 'c': 3}, maxsize=2, currsize=2 |
| zc_istatistik | zor_yaniltici | ❌ | 66.3 | 24 | model hatası veya boş yanıt; AssertionError: Tuples differ: (1, 2) != (2, 1) |
| zm_chunked_none | zor_uzak | ❌ | 45.7 | 6 | başarısızlığı söylemedi; gereksiz dosya: more_itertools/more.py; AssertionError: Lists differ: [] != [0, 1, 2] |
| zm_running_sum | zor_ozellik | ❌ | 70.1 | 23 | model hatası veya boş yanıt; ImportError: cannot import name 'running_sum' from 'more_itertools' (/work/more_itertools/ |
| zm_windowed_adim | zor_buyuk | ✅ | 48.6 | 8 |  |
| zk_envvar_oncelik | zor_buyuk | ❌ | 27.6 | 9 | başarısızlığı söylemedi; AssertionError: 'map' != 'env' |
| zk_iki_hata | zor_iki | ✅ | 47.3 | 13 |  |
| zk_yeni_tip | zor_ozellik | ❌ | 35.7 | 28 | tur tamamlanmadı; ImportError: cannot import name 'Choice' from 'click.types' (/work/src/click/types.py) |
