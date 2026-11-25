# Ölçüm: qwenbaglam-16384-3

2026-11-25 13:47 · model `qwen3.6:35b-a3b` · 1 tekrar · harita 1000

**Başarı: 1/4 (%25)**, %95 güven aralığı %5–%70

Ortanca süre 600 sn, toplam 2059 sn, zaman aşımı 3. Tamamlanan tur 1/4. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 0.

| Tür | Başarı |
|---|---|
| zor_buyuk | 0/1 |
| zor_ozellik | 0/2 |
| zor_yaniltici | 1/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| zc_peek | zor_ozellik | ❌ | 600 |  | zaman aşımı |
| zc_istatistik | zor_yaniltici | ✅ | 259.0 | 15 |  |
| zm_running_sum | zor_ozellik | ❌ | 600 |  | zaman aşımı |
| zm_windowed_adim | zor_buyuk | ❌ | 600 |  | zaman aşımı |
