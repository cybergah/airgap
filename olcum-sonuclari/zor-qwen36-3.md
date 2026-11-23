# Ölçüm: zor-qwen36-3

2026-11-23 10:04 · model `qwen3.6:35b-a3b` · 1 tekrar · harita 1000

**Başarı: 7/9 (%78)**, %95 güven aralığı %45–%94

Ortanca süre 160.6 sn, toplam 1295 sn, zaman aşımı 0. Tamamlanan tur 7/9. Başarısız olup bunu söylemeyen 1. Gereksiz dosya değiştiren 1.

| Tür | Başarı |
|---|---|
| zor_buyuk | 2/2 |
| zor_iki | 1/1 |
| zor_ozellik | 2/3 |
| zor_uzak | 1/2 |
| zor_yaniltici | 1/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| zc_anahtar | zor_uzak | ✅ | 67.4 | 10 |  |
| zc_peek | zor_ozellik | ✅ | 198.4 | 30 | model hatası veya boş yanıt |
| zc_istatistik | zor_yaniltici | ✅ | 174.6 | 18 |  |
| zm_chunked_none | zor_uzak | ❌ | 84.8 | 13 | başarısızlığı söylemedi; gereksiz dosya: more_itertools/more.py; AssertionError: Lists differ: [] != [0, 1, 2] |
| zm_running_sum | zor_ozellik | ❌ | 189.4 | 36 | test değiştirmek istedi; tur tamamlanmadı; TypeError: 'int' object is not iterable |
| zm_windowed_adim | zor_buyuk | ✅ | 160.6 | 17 |  |
| zk_envvar_oncelik | zor_buyuk | ✅ | 102.7 | 19 |  |
| zk_iki_hata | zor_iki | ✅ | 73.4 | 12 |  |
| zk_yeni_tip | zor_ozellik | ✅ | 243.7 | 30 |  |
