# Ölçüm: qwensembol-eski-2

2026-11-24 03:41 · model `qwen3.6:35b-a3b` · 1 tekrar · harita 1000

**Başarı: 5/9 (%56)**, %95 güven aralığı %27–%81

Ortanca süre 180.0 sn, toplam 2223 sn, zaman aşımı 1. Tamamlanan tur 5/9. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 0.

| Tür | Başarı |
|---|---|
| zor_buyuk | 1/2 |
| zor_iki | 1/1 |
| zor_ozellik | 1/3 |
| zor_uzak | 2/2 |
| zor_yaniltici | 0/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| zc_anahtar | zor_uzak | ✅ | 61.2 | 17 |  |
| zc_peek | zor_ozellik | ❌ | 511.7 | 48 | model hatası veya boş yanıt; FAILED (failures=1) |
| zc_istatistik | zor_yaniltici | ❌ | 327.7 | 16 | model hatası veya boş yanıt; AssertionError: Tuples differ: (1, 2) != (2, 1) |
| zm_chunked_none | zor_uzak | ✅ | 110.9 | 20 |  |
| zm_running_sum | zor_ozellik | ❌ | 222.0 | 34 | model hatası veya boş yanıt; FAILED (failures=1) |
| zm_windowed_adim | zor_buyuk | ❌ | 600 |  | zaman aşımı |
| zk_envvar_oncelik | zor_buyuk | ✅ | 149.8 | 21 |  |
| zk_iki_hata | zor_iki | ✅ | 59.8 | 14 |  |
| zk_yeni_tip | zor_ozellik | ✅ | 180.0 | 23 |  |
