# Ölçüm: gptadim-a60-2

2026-11-24 00:45 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 5/9 (%56)**, %95 güven aralığı %27–%81

Ortanca süre 74.3 sn, toplam 799 sn, zaman aşımı 0. Tamamlanan tur 6/9. Başarısız olup bunu söylemeyen 1. Gereksiz dosya değiştiren 1.

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
| zc_anahtar | zor_uzak | ✅ | 22.9 | 11 |  |
| zc_peek | zor_ozellik | ❌ | 119.2 | 58 | tur tamamlanmadı; AttributeError: 'LRUCache' object has no attribute 'peek' |
| zc_istatistik | zor_yaniltici | ✅ | 87.6 | 55 |  |
| zm_chunked_none | zor_uzak | ❌ | 68.0 | 23 | başarısızlığı söylemedi; gereksiz dosya: more_itertools/more.py; AssertionError: Lists differ: [] != [0, 1, 2] |
| zm_running_sum | zor_ozellik | ❌ | 149.9 | 39 | model hatası veya boş yanıt; AttributeError: module 'more_itertools.recipes' has no attribute 'running_sum'. Did you me |
| zm_windowed_adim | zor_buyuk | ✅ | 55.5 | 13 |  |
| zk_envvar_oncelik | zor_buyuk | ✅ | 40.0 | 15 |  |
| zk_iki_hata | zor_iki | ✅ | 182.0 | 34 |  |
| zk_yeni_tip | zor_ozellik | ❌ | 74.3 | 27 | model hatası veya boş yanıt; AttributeError: PERCENT |
