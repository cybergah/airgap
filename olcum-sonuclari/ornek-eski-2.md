# Ölçüm: ornek-eski-2

2026-11-23 16:11 · model `qwen3.6:35b-a3b` · 1 tekrar · harita 1000

**Başarı: 8/9 (%89)**, %95 güven aralığı %56–%98

Ortanca süre 242.4 sn, toplam 2345 sn, zaman aşımı 0. Tamamlanan tur 7/9. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 1.

| Tür | Başarı |
|---|---|
| zor_buyuk | 1/2 |
| zor_iki | 1/1 |
| zor_ozellik | 3/3 |
| zor_uzak | 2/2 |
| zor_yaniltici | 1/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| zc_anahtar | zor_uzak | ✅ | 84.3 | 18 |  |
| zc_peek | zor_ozellik | ✅ | 309.8 | 28 |  |
| zc_istatistik | zor_yaniltici | ✅ | 595.3 | 27 |  |
| zm_chunked_none | zor_uzak | ✅ | 171.1 | 24 |  |
| zm_running_sum | zor_ozellik | ✅ | 314.6 | 39 | test değiştirmek istedi; gereksiz dosya: README.rst; tur tamamlanmadı |
| zm_windowed_adim | zor_buyuk | ❌ | 358.4 | 1 | model hatası veya boş yanıt; FAILED (failures=1) |
| zk_envvar_oncelik | zor_buyuk | ✅ | 242.4 | 21 |  |
| zk_iki_hata | zor_iki | ✅ | 117.9 | 22 |  |
| zk_yeni_tip | zor_ozellik | ✅ | 150.9 | 22 |  |
