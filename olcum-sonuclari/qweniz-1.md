# Ölçüm: qweniz-1

2026-11-25 11:03 · model `qwen3.6:35b-a3b` · 1 tekrar · harita 1000

**Başarı: 1/4 (%25)**, %95 güven aralığı %5–%70

Ortanca süre 165.4 sn, toplam 750 sn, zaman aşımı 0. Tamamlanan tur 2/4. Başarısız olup bunu söylemeyen 1. Gereksiz dosya değiştiren 0.

| Tür | Başarı |
|---|---|
| zor_buyuk | 1/1 |
| zor_ozellik | 0/2 |
| zor_yaniltici | 0/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| zc_peek | zor_ozellik | ❌ | 160.1 | 5 | başarısızlığı söylemedi; AttributeError: 'LRUCache' object has no attribute 'peek' |
| zc_istatistik | zor_yaniltici | ❌ | 331.6 | 13 | model hatası veya boş yanıt; AssertionError: Tuples differ: (1, 2) != (2, 1) |
| zm_running_sum | zor_ozellik | ❌ | 92.9 | 22 | model hatası veya boş yanıt; FAILED (failures=1) |
| zm_windowed_adim | zor_buyuk | ✅ | 165.4 | 13 |  |
