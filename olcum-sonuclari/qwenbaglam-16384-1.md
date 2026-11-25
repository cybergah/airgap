# Ölçüm: qwenbaglam-16384-1

2026-11-25 11:55 · model `qwen3.6:35b-a3b` · 1 tekrar · harita 1000

**Başarı: 1/4 (%25)**, %95 güven aralığı %5–%70

Ortanca süre 356.5 sn, toplam 929 sn, zaman aşımı 0. Tamamlanan tur 1/4. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 0.

| Tür | Başarı |
|---|---|
| zor_buyuk | 0/1 |
| zor_ozellik | 0/2 |
| zor_yaniltici | 1/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| zc_peek | zor_ozellik | ❌ | 416.3 | 35 | model hatası veya boş yanıt; AssertionError: 'a' unexpectedly found in LFUCache({'a': 1, 'c': 3}, maxsize=2, currsize=2 |
| zc_istatistik | zor_yaniltici | ✅ | 57.0 | 12 |  |
| zm_running_sum | zor_ozellik | ❌ | 99.0 | 20 | model hatası veya boş yanıt; FAILED (failures=1) |
| zm_windowed_adim | zor_buyuk | ❌ | 356.5 | 2 | model hatası veya boş yanıt; FAILED (failures=1) |
