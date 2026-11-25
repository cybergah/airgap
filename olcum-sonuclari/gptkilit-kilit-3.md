# Ölçüm: gptkilit-kilit-3

2026-11-24 18:38 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 4/9 (%44)**, %95 güven aralığı %19–%73

Ortanca süre 75.8 sn, toplam 708 sn, zaman aşımı 0. Tamamlanan tur 1/9. Başarısız olup bunu söylemeyen 1. Gereksiz dosya değiştiren 1.

| Tür | Başarı |
|---|---|
| zor_buyuk | 0/2 |
| zor_iki | 1/1 |
| zor_ozellik | 1/3 |
| zor_uzak | 2/2 |
| zor_yaniltici | 0/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| zc_anahtar | zor_uzak | ✅ | 87.6 | 29 | gereksiz dosya: cachetools/__init__.py, cachetools/func.py, cachetools/keys.; model hatası veya boş yanıt |
| zc_peek | zor_ozellik | ✅ | 75.8 | 30 | tur tamamlanmadı |
| zc_istatistik | zor_yaniltici | ❌ | 69.1 | 30 | tur tamamlanmadı; AssertionError: Tuples differ: (1, 2) != (2, 1) |
| zm_chunked_none | zor_uzak | ✅ | 64.0 | 28 | model hatası veya boş yanıt |
| zm_running_sum | zor_ozellik | ❌ | 84.2 | 27 | model hatası veya boş yanıt; ImportError: cannot import name 'running_sum' from 'more_itertools' (/work/more_itertools/ |
| zm_windowed_adim | zor_buyuk | ❌ | 148.7 | 28 | model hatası veya boş yanıt; AssertionError: Lists differ: [(0, 1, 2), (2, 3, 4)] != [(0, 1, 2), (2, 3, 4), (4, 5, None |
| zk_envvar_oncelik | zor_buyuk | ❌ | 59.9 | 21 | başarısızlığı söylemedi; AssertionError: 'map' != 'env' |
| zk_iki_hata | zor_iki | ✅ | 85.3 | 30 | tur tamamlanmadı |
| zk_yeni_tip | zor_ozellik | ❌ | 33.5 | 29 | tur tamamlanmadı; AttributeError: PERCENT |
