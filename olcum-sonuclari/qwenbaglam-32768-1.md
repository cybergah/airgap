# Ölçüm: qwenbaglam-32768-1

2026-11-25 12:16 · model `qwen3.6:35b-a3b` · 1 tekrar · harita 1000

**Başarı: 4/4 (%100)**, %95 güven aralığı %51–%100

Ortanca süre 308.9 sn, toplam 1281 sn, zaman aşımı 0. Tamamlanan tur 2/4. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 1.

| Tür | Başarı |
|---|---|
| zor_buyuk | 1/1 |
| zor_ozellik | 2/2 |
| zor_yaniltici | 1/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| zc_peek | zor_ozellik | ✅ | 308.9 | 31 |  |
| zc_istatistik | zor_yaniltici | ✅ | 221.8 | 30 | tur tamamlanmadı |
| zm_running_sum | zor_ozellik | ✅ | 192.6 | 39 | test değiştirmek istedi; gereksiz dosya: README.rst |
| zm_windowed_adim | zor_buyuk | ✅ | 557.4 | 7 | model hatası veya boş yanıt |
