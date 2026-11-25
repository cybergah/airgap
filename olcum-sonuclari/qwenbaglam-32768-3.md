# Ölçüm: qwenbaglam-32768-3

2026-11-25 14:08 · model `qwen3.6:35b-a3b` · 1 tekrar · harita 1000

**Başarı: 4/4 (%100)**, %95 güven aralığı %51–%100

Ortanca süre 390.3 sn, toplam 1229 sn, zaman aşımı 0. Tamamlanan tur 3/4. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 1.

| Tür | Başarı |
|---|---|
| zor_buyuk | 1/1 |
| zor_ozellik | 2/2 |
| zor_yaniltici | 1/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| zc_peek | zor_ozellik | ✅ | 264.4 | 28 |  |
| zc_istatistik | zor_yaniltici | ✅ | 114.5 | 19 |  |
| zm_running_sum | zor_ozellik | ✅ | 390.3 | 28 | test değiştirmek istedi; gereksiz dosya: README.rst; model hatası veya boş yanıt |
| zm_windowed_adim | zor_buyuk | ✅ | 459.9 | 13 |  |
