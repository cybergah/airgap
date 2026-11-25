# Ölçüm: qwen32k-3

2026-11-25 17:09 · model `qwen3.6:35b-a3b` · 1 tekrar · harita 1000

**Başarı: 7/9 (%78)**, %95 güven aralığı %45–%94

Ortanca süre 399.5 sn, toplam 3884 sn, zaman aşımı 2. Tamamlanan tur 7/9. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 0.

| Tür | Başarı |
|---|---|
| zor_buyuk | 1/2 |
| zor_iki | 1/1 |
| zor_ozellik | 2/3 |
| zor_uzak | 2/2 |
| zor_yaniltici | 1/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| zc_anahtar | zor_uzak | ✅ | 261.2 | 20 |  |
| zc_peek | zor_ozellik | ❌ | 600 |  | zaman aşımı |
| zc_istatistik | zor_yaniltici | ✅ | 537.7 | 28 |  |
| zm_chunked_none | zor_uzak | ✅ | 287.3 | 21 |  |
| zm_running_sum | zor_ozellik | ✅ | 399.5 | 33 | test değiştirmek istedi |
| zm_windowed_adim | zor_buyuk | ❌ | 600 |  | zaman aşımı |
| zk_envvar_oncelik | zor_buyuk | ✅ | 306.2 | 20 |  |
| zk_iki_hata | zor_iki | ✅ | 374.6 | 25 |  |
| zk_yeni_tip | zor_ozellik | ✅ | 517.1 | 22 |  |
