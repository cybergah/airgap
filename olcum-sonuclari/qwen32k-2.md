# Ölçüm: qwen32k-2

2026-11-25 16:04 · model `qwen3.6:35b-a3b` · 1 tekrar · harita 1000

**Başarı: 7/9 (%78)**, %95 güven aralığı %45–%94

Ortanca süre 298.6 sn, toplam 3162 sn, zaman aşımı 2. Tamamlanan tur 7/9. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 1.

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
| zc_anahtar | zor_uzak | ✅ | 151.1 | 16 |  |
| zc_peek | zor_ozellik | ❌ | 600 |  | zaman aşımı |
| zc_istatistik | zor_yaniltici | ✅ | 226.7 | 18 |  |
| zm_chunked_none | zor_uzak | ✅ | 301.1 | 24 |  |
| zm_running_sum | zor_ozellik | ✅ | 462.9 | 30 | gereksiz dosya: README.rst |
| zm_windowed_adim | zor_buyuk | ❌ | 600 |  | zaman aşımı |
| zk_envvar_oncelik | zor_buyuk | ✅ | 298.6 | 20 |  |
| zk_iki_hata | zor_iki | ✅ | 229.8 | 21 |  |
| zk_yeni_tip | zor_ozellik | ✅ | 292.0 | 31 |  |
