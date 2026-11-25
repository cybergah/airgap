# Ölçüm: qwenbaglam-32768-2

2026-11-25 12:37 · model `qwen3.6:35b-a3b` · 1 tekrar · harita 1000

**Başarı: 3/4 (%75)**, %95 güven aralığı %30–%95

Ortanca süre 375.5 sn, toplam 1244 sn, zaman aşımı 1. Tamamlanan tur 1/4. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 1.

| Tür | Başarı |
|---|---|
| zor_buyuk | 0/1 |
| zor_ozellik | 2/2 |
| zor_yaniltici | 1/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| zc_peek | zor_ozellik | ✅ | 375.5 | 36 | model hatası veya boş yanıt |
| zc_istatistik | zor_yaniltici | ✅ | 54.2 | 13 |  |
| zm_running_sum | zor_ozellik | ✅ | 214.2 | 40 | test değiştirmek istedi; gereksiz dosya: README.rst; tur tamamlanmadı |
| zm_windowed_adim | zor_buyuk | ❌ | 600 |  | zaman aşımı |
