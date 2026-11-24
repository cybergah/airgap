# Ölçüm: gptokuma-yeni-1

2026-11-24 05:59 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 3/9 (%33)**, %95 güven aralığı %12–%65

Ortanca süre 70.0 sn, toplam 808 sn, zaman aşımı 0. Tamamlanan tur 2/9. Başarısız olup bunu söylemeyen 1. Gereksiz dosya değiştiren 2.

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
| zc_anahtar | zor_uzak | ✅ | 70.0 | 28 | gereksiz dosya: cachetools/__init__.py; model hatası veya boş yanıt |
| zc_peek | zor_ozellik | ❌ | 88.6 | 28 | tur tamamlanmadı; AssertionError: 'a' unexpectedly found in LRUCache({'a': 1, 'c': 3}, maxsize=2, currsize=2 |
| zc_istatistik | zor_yaniltici | ❌ | 59.1 | 28 | tur tamamlanmadı; AssertionError: Tuples differ: (1, 2) != (2, 1) |
| zm_chunked_none | zor_uzak | ❌ | 76.7 | 19 | başarısızlığı söylemedi; gereksiz dosya: more_itertools/more.py; AssertionError: Lists differ: [] != [0, 1, 2] |
| zm_running_sum | zor_ozellik | ❌ | 118.0 | 29 | model hatası veya boş yanıt; AssertionError: Lists differ: [] != [1, 3, 6, 10] |
| zm_windowed_adim | zor_buyuk | ❌ | 231.6 | 27 | model hatası veya boş yanıt; AssertionError: Lists differ: [(1, 2, 3), (3, None, None)] != [(1, 2, 3)] |
| zk_envvar_oncelik | zor_buyuk | ✅ | 52.7 | 24 | model hatası veya boş yanıt |
| zk_iki_hata | zor_iki | ✅ | 43.1 | 22 |  |
| zk_yeni_tip | zor_ozellik | ❌ | 67.8 | 27 | model hatası veya boş yanıt; AttributeError: PERCENT |
