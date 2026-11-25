# Ölçüm: qwenbaglam-16384-2

2026-11-25 13:13 · model `qwen3.6:35b-a3b` · 1 tekrar · harita 1000

**Başarı: 2/4 (%50)**, %95 güven aralığı %15–%85

Ortanca süre 600 sn, toplam 2115 sn, zaman aşımı 2. Tamamlanan tur 2/4. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 0.

| Tür | Başarı |
|---|---|
| zor_buyuk | 0/1 |
| zor_ozellik | 1/2 |
| zor_yaniltici | 1/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| zc_peek | zor_ozellik | ❌ | 600 |  | zaman aşımı |
| zc_istatistik | zor_yaniltici | ✅ | 531.1 | 20 |  |
| zm_running_sum | zor_ozellik | ✅ | 383.6 | 29 | test değiştirmek istedi |
| zm_windowed_adim | zor_buyuk | ❌ | 600 |  | zaman aşımı |
