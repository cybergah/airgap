# Ölçüm: gptokuma-yeni-3

2026-11-24 06:39 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 3/9 (%33)**, %95 güven aralığı %12–%65

Ortanca süre 52.8 sn, toplam 555 sn, zaman aşımı 0. Tamamlanan tur 3/9. Başarısız olup bunu söylemeyen 1. Gereksiz dosya değiştiren 1.

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
| zc_anahtar | zor_uzak | ✅ | 19.7 | 10 |  |
| zc_peek | zor_ozellik | ❌ | 52.8 | 27 | model hatası veya boş yanıt; AttributeError: 'LRUCache' object has no attribute 'peek' |
| zc_istatistik | zor_yaniltici | ❌ | 49.5 | 30 | tur tamamlanmadı; AssertionError: Tuples differ: (1, 2) != (2, 1) |
| zm_chunked_none | zor_uzak | ❌ | 66.0 | 19 | başarısızlığı söylemedi; gereksiz dosya: more_itertools/more.py; AssertionError: Lists differ: [] != [0, 1, 2] |
| zm_running_sum | zor_ozellik | ❌ | 33.6 | 30 | tur tamamlanmadı; ImportError: cannot import name 'running_sum' from 'more_itertools' (/work/more_itertools/ |
| zm_windowed_adim | zor_buyuk | ❌ | 176.5 | 27 | model hatası veya boş yanıt; FAILED (failures=1) |
| zk_envvar_oncelik | zor_buyuk | ✅ | 52.8 | 19 |  |
| zk_iki_hata | zor_iki | ✅ | 67.4 | 29 | tur tamamlanmadı |
| zk_yeni_tip | zor_ozellik | ❌ | 36.6 | 28 | tur tamamlanmadı; AttributeError: PERCENT |
