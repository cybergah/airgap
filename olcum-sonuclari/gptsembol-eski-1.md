# Ölçüm: gptsembol-eski-1

2026-11-24 01:52 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 5/9 (%56)**, %95 güven aralığı %27–%81

Ortanca süre 50.5 sn, toplam 525 sn, zaman aşımı 0. Tamamlanan tur 5/9. Başarısız olup bunu söylemeyen 1. Gereksiz dosya değiştiren 2.

| Tür | Başarı |
|---|---|
| zor_buyuk | 2/2 |
| zor_iki | 1/1 |
| zor_ozellik | 0/3 |
| zor_uzak | 1/2 |
| zor_yaniltici | 1/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| zc_anahtar | zor_uzak | ✅ | 30.9 | 11 |  |
| zc_peek | zor_ozellik | ❌ | 58.3 | 29 | tur tamamlanmadı; AttributeError: 'LRUCache' object has no attribute 'peek' |
| zc_istatistik | zor_yaniltici | ✅ | 83.6 | 27 | gereksiz dosya: cachetools/__init__.py, tests/__init__.py; tur tamamlanmadı |
| zm_chunked_none | zor_uzak | ❌ | 73.8 | 18 | başarısızlığı söylemedi; gereksiz dosya: more_itertools/more.py; AssertionError: Lists differ: [] != [0, 1, 2] |
| zm_running_sum | zor_ozellik | ❌ | 50.2 | 29 | model hatası veya boş yanıt; AttributeError: module 'more_itertools.recipes' has no attribute 'running_sum'. Did you me |
| zm_windowed_adim | zor_buyuk | ✅ | 80.4 | 13 |  |
| zk_envvar_oncelik | zor_buyuk | ✅ | 48.1 | 19 |  |
| zk_iki_hata | zor_iki | ✅ | 50.5 | 23 |  |
| zk_yeni_tip | zor_ozellik | ❌ | 49.0 | 30 | tur tamamlanmadı; AttributeError: PERCENT |
