# Ölçüm: gptiz-1

2026-11-24 05:32 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 5/9 (%56)**, %95 güven aralığı %27–%81

Ortanca süre 65.8 sn, toplam 568 sn, zaman aşımı 0. Tamamlanan tur 5/9. Başarısız olup bunu söylemeyen 1. Gereksiz dosya değiştiren 1.

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
| zc_anahtar | zor_uzak | ✅ | 66.4 | 14 |  |
| zc_peek | zor_ozellik | ❌ | 72.7 | 28 | tur tamamlanmadı; AttributeError: 'LRUCache' object has no attribute 'peek' |
| zc_istatistik | zor_yaniltici | ✅ | 59.9 | 30 | tur tamamlanmadı |
| zm_chunked_none | zor_uzak | ❌ | 87.1 | 17 | başarısızlığı söylemedi; gereksiz dosya: more_itertools/more.py; AssertionError: Lists differ: [] != [0, 1, 2] |
| zm_running_sum | zor_ozellik | ❌ | 84.7 | 30 | tur tamamlanmadı; AssertionError: Lists differ: [] != [1, 3, 6, 10] |
| zm_windowed_adim | zor_buyuk | ✅ | 65.8 | 11 |  |
| zk_envvar_oncelik | zor_buyuk | ✅ | 43.1 | 18 |  |
| zk_iki_hata | zor_iki | ✅ | 35.4 | 19 |  |
| zk_yeni_tip | zor_ozellik | ❌ | 53.1 | 27 | model hatası veya boş yanıt; AttributeError: PERCENT |
