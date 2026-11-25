# Ölçüm: gptkilit-kilit-2

2026-11-24 18:03 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 4/9 (%44)**, %95 güven aralığı %19–%73

Ortanca süre 61.2 sn, toplam 781 sn, zaman aşımı 0. Tamamlanan tur 4/9. Başarısız olup bunu söylemeyen 1. Gereksiz dosya değiştiren 2.

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
| zc_anahtar | zor_uzak | ✅ | 48.2 | 11 |  |
| zc_peek | zor_ozellik | ❌ | 55.8 | 29 | tur tamamlanmadı; AttributeError: 'LRUCache' object has no attribute 'peek' |
| zc_istatistik | zor_yaniltici | ❌ | 65.0 | 29 | gereksiz dosya: cachetools/__init__.py; model hatası veya boş yanıt; AssertionError: Tuples differ: (1, 2) != (2, 1) |
| zm_chunked_none | zor_uzak | ❌ | 122.8 | 24 | başarısızlığı söylemedi; gereksiz dosya: more_itertools/more.py; AssertionError: Lists differ: [] != [0, 1, 2] |
| zm_running_sum | zor_ozellik | ❌ | 61.2 | 30 | tur tamamlanmadı; FAILED (failures=1) |
| zm_windowed_adim | zor_buyuk | ✅ | 255.1 | 22 | model hatası veya boş yanıt |
| zk_envvar_oncelik | zor_buyuk | ✅ | 44.1 | 19 |  |
| zk_iki_hata | zor_iki | ✅ | 41.3 | 21 |  |
| zk_yeni_tip | zor_ozellik | ❌ | 87.8 | 28 | model hatası veya boş yanıt; AttributeError: PERCENT |
