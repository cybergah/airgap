# Ölçüm: qweniz-3

2026-11-25 11:32 · model `qwen3.6:35b-a3b` · 1 tekrar · harita 1000

**Başarı: 2/4 (%50)**, %95 güven aralığı %15–%85

Ortanca süre 233.3 sn, toplam 773 sn, zaman aşımı 0. Tamamlanan tur 2/4. Başarısız olup bunu söylemeyen 1. Gereksiz dosya değiştiren 1.

| Tür | Başarı |
|---|---|
| zor_buyuk | 0/1 |
| zor_ozellik | 1/2 |
| zor_yaniltici | 1/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| zc_peek | zor_ozellik | ❌ | 112.6 | 18 | başarısızlığı söylemedi; AttributeError: 'LRUCache' object has no attribute 'peek' |
| zc_istatistik | zor_yaniltici | ✅ | 164.2 | 18 |  |
| zm_running_sum | zor_ozellik | ✅ | 233.3 | 32 | test değiştirmek istedi; gereksiz dosya: README.rst; model hatası veya boş yanıt |
| zm_windowed_adim | zor_buyuk | ❌ | 262.6 | 16 | model hatası veya boş yanıt; AssertionError: Lists differ: [(1, 2, 3), (3, None, None)] != [(1, 2, 3)] |
