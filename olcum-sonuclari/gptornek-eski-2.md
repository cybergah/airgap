# Ölçüm: gptornek-eski-2

2026-11-23 22:55 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 3/9 (%33)**, %95 güven aralığı %12–%65

Ortanca süre 62.4 sn, toplam 655 sn, zaman aşımı 0. Tamamlanan tur 3/9. Başarısız olup bunu söylemeyen 2. Gereksiz dosya değiştiren 3.

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
| zc_anahtar | zor_uzak | ✅ | 28.4 | 10 |  |
| zc_peek | zor_ozellik | ❌ | 62.4 | 28 | model hatası veya boş yanıt; AssertionError: 'a' unexpectedly found in LRUCache({'a': 1, 'c': 3}, maxsize=2, currsize=2 |
| zc_istatistik | zor_yaniltici | ✅ | 65.2 | 27 | gereksiz dosya: cachetools/__init__.py, tests/__init__.py; tur tamamlanmadı |
| zm_chunked_none | zor_uzak | ❌ | 142.4 | 30 | gereksiz dosya: more_itertools/more.py; tur tamamlanmadı; AssertionError: Lists differ: [] != [0, 1, 2] |
| zm_running_sum | zor_ozellik | ❌ | 60.6 | 30 | tur tamamlanmadı; AttributeError: module 'more_itertools.recipes' has no attribute 'running_sum'. Did you me |
| zm_windowed_adim | zor_buyuk | ❌ | 129.4 | 20 | başarısızlığı söylemedi; FAILED (failures=1) |
| zk_envvar_oncelik | zor_buyuk | ✅ | 70.5 | 27 | gereksiz dosya: docs/__pycache__/conf.cpython-313.pyc, examples/aliases/__py; model hatası veya boş yanıt |
| zk_iki_hata | zor_iki | ❌ | 44.5 | 19 | başarısızlığı söylemedi; AssertionError: False is not true |
| zk_yeni_tip | zor_ozellik | ❌ | 51.5 | 29 | tur tamamlanmadı; AttributeError: PERCENT |
