# Ölçüm: gptkilit-eski-2

2026-11-24 17:50 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 4/9 (%44)**, %95 güven aralığı %19–%73

Ortanca süre 62.1 sn, toplam 586 sn, zaman aşımı 0. Tamamlanan tur 4/9. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 0.

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
| zc_anahtar | zor_uzak | ✅ | 51.3 | 19 |  |
| zc_peek | zor_ozellik | ❌ | 60.7 | 29 | tur tamamlanmadı; AttributeError: 'LRUCache' object has no attribute 'peek' |
| zc_istatistik | zor_yaniltici | ❌ | 68.6 | 29 | tur tamamlanmadı; AssertionError: Tuples differ: (1, 2) != (2, 1) |
| zm_chunked_none | zor_uzak | ❌ | 59.7 | 27 | model hatası veya boş yanıt; AssertionError: Lists differ: [] != [[1, 2, 3]] |
| zm_running_sum | zor_ozellik | ❌ | 83.1 | 27 | model hatası veya boş yanıt; ImportError: cannot import name 'running_sum' from 'more_itertools' (/work/more_itertools/ |
| zm_windowed_adim | zor_buyuk | ✅ | 94.7 | 8 |  |
| zk_envvar_oncelik | zor_buyuk | ✅ | 62.1 | 19 |  |
| zk_iki_hata | zor_iki | ✅ | 42.5 | 21 |  |
| zk_yeni_tip | zor_ozellik | ❌ | 62.8 | 30 | tur tamamlanmadı; AttributeError: PERCENT |
