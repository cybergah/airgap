# Ölçüm: qweniz-2

2026-11-25 11:19 · model `qwen3.6:35b-a3b` · 1 tekrar · harita 1000

**Başarı: 1/4 (%25)**, %95 güven aralığı %5–%70

Ortanca süre 220.7 sn, toplam 969 sn, zaman aşımı 1. Tamamlanan tur 3/4. Başarısız olup bunu söylemeyen 2. Gereksiz dosya değiştiren 0.

| Tür | Başarı |
|---|---|
| zor_buyuk | 0/1 |
| zor_ozellik | 0/2 |
| zor_yaniltici | 1/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| zc_peek | zor_ozellik | ❌ | 37.2 | 4 | başarısızlığı söylemedi; AttributeError: 'LRUCache' object has no attribute 'peek' |
| zc_istatistik | zor_yaniltici | ✅ | 111.0 | 19 |  |
| zm_running_sum | zor_ozellik | ❌ | 220.7 | 31 | başarısızlığı söylemedi; FAILED (failures=1) |
| zm_windowed_adim | zor_buyuk | ❌ | 600 |  | zaman aşımı |
