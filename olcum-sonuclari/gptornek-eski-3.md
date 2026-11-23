# Ölçüm: gptornek-eski-3

2026-11-23 23:21 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 4/9 (%44)**, %95 güven aralığı %19–%73

Ortanca süre 68.5 sn, toplam 606 sn, zaman aşımı 0. Tamamlanan tur 3/9. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 1.

| Tür | Başarı |
|---|---|
| zor_buyuk | 1/2 |
| zor_iki | 1/1 |
| zor_ozellik | 0/3 |
| zor_uzak | 1/2 |
| zor_yaniltici | 1/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| zc_anahtar | zor_uzak | ✅ | 17.4 | 11 |  |
| zc_peek | zor_ozellik | ❌ | 80.0 | 29 | tur tamamlanmadı; AttributeError: 'LRUCache' object has no attribute 'peek' |
| zc_istatistik | zor_yaniltici | ✅ | 49.2 | 29 | tur tamamlanmadı |
| zm_chunked_none | zor_uzak | ❌ | 68.5 | 29 | gereksiz dosya: more_itertools/more.py; tur tamamlanmadı; AssertionError: Lists differ: [] != [0, 1, 2] |
| zm_running_sum | zor_ozellik | ❌ | 83.5 | 26 | model hatası veya boş yanıt; AttributeError: module 'more_itertools.recipes' has no attribute 'running_sum'. Did you me |
| zm_windowed_adim | zor_buyuk | ❌ | 142.2 | 28 | model hatası veya boş yanıt; FAILED (failures=1) |
| zk_envvar_oncelik | zor_buyuk | ✅ | 55.0 | 19 |  |
| zk_iki_hata | zor_iki | ✅ | 34.4 | 15 |  |
| zk_yeni_tip | zor_ozellik | ❌ | 76.0 | 25 | model hatası veya boş yanıt; AttributeError: PERCENT |
