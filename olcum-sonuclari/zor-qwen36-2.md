# Ölçüm: zor-qwen36-2

2026-11-23 09:31 · model `qwen3.6:35b-a3b` · 1 tekrar · harita 1000

**Başarı: 7/9 (%78)**, %95 güven aralığı %45–%94

Ortanca süre 182.5 sn, toplam 1572 sn, zaman aşımı 0. Tamamlanan tur 7/9. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 1.

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
| zc_anahtar | zor_uzak | ✅ | 87.6 | 14 |  |
| zc_peek | zor_ozellik | ❌ | 225.2 | 31 | tur tamamlanmadı; AttributeError: 'LRUCache' object has no attribute 'peek' |
| zc_istatistik | zor_yaniltici | ✅ | 182.5 | 13 |  |
| zm_chunked_none | zor_uzak | ❌ | 205.9 | 30 | gereksiz dosya: more_itertools/more.py; tur tamamlanmadı; AssertionError: Lists differ: [] != [[1, 2], [3, 4], [5]] |
| zm_running_sum | zor_ozellik | ✅ | 242.1 | 34 | test değiştirmek istedi |
| zm_windowed_adim | zor_buyuk | ✅ | 89.7 | 10 |  |
| zk_envvar_oncelik | zor_buyuk | ✅ | 225.4 | 25 |  |
| zk_iki_hata | zor_iki | ✅ | 161.5 | 28 |  |
| zk_yeni_tip | zor_ozellik | ✅ | 151.9 | 24 |  |
