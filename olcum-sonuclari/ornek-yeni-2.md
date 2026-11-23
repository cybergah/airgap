# Ölçüm: ornek-yeni-2

2026-11-23 16:41 · model `qwen3.6:35b-a3b` · 1 tekrar · harita 1000

**Başarı: 8/9 (%89)**, %95 güven aralığı %56–%98

Ortanca süre 169.6 sn, toplam 1790 sn, zaman aşımı 0. Tamamlanan tur 8/9. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 0.

| Tür | Başarı |
|---|---|
| zor_buyuk | 2/2 |
| zor_iki | 1/1 |
| zor_ozellik | 2/3 |
| zor_uzak | 2/2 |
| zor_yaniltici | 1/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| zc_anahtar | zor_uzak | ✅ | 62.1 | 14 |  |
| zc_peek | zor_ozellik | ❌ | 415.6 | 40 | tur tamamlanmadı; NameError: name '_LFUCache__marker' is not defined. Did you mean: '_LFUCache__touch'? |
| zc_istatistik | zor_yaniltici | ✅ | 176.9 | 17 |  |
| zm_chunked_none | zor_uzak | ✅ | 159.4 | 20 |  |
| zm_running_sum | zor_ozellik | ✅ | 169.6 | 30 |  |
| zm_windowed_adim | zor_buyuk | ✅ | 99.0 | 12 |  |
| zk_envvar_oncelik | zor_buyuk | ✅ | 367.5 | 15 |  |
| zk_iki_hata | zor_iki | ✅ | 128.5 | 25 |  |
| zk_yeni_tip | zor_ozellik | ✅ | 211.6 | 31 |  |
