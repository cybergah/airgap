# Ölçüm: ornek-yeni-3

2026-11-23 18:01 · model `qwen3.6:35b-a3b` · 1 tekrar · harita 1000

**Başarı: 6/9 (%67)**, %95 güven aralığı %35–%88

Ortanca süre 209.8 sn, toplam 2358 sn, zaman aşımı 1. Tamamlanan tur 7/9. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 0.

| Tür | Başarı |
|---|---|
| zor_buyuk | 1/2 |
| zor_iki | 1/1 |
| zor_ozellik | 1/3 |
| zor_uzak | 2/2 |
| zor_yaniltici | 1/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| zc_anahtar | zor_uzak | ✅ | 71.7 | 12 |  |
| zc_peek | zor_ozellik | ❌ | 458.3 | 49 | model hatası veya boş yanıt; AttributeError: 'LRUCache' object has no attribute '_LRUCache__links'. Did you mean: '_LRU |
| zc_istatistik | zor_yaniltici | ✅ | 174.1 | 19 |  |
| zm_chunked_none | zor_uzak | ✅ | 215.6 | 21 |  |
| zm_running_sum | zor_ozellik | ✅ | 340.5 | 35 | test değiştirmek istedi |
| zm_windowed_adim | zor_buyuk | ❌ | 600 |  | zaman aşımı |
| zk_envvar_oncelik | zor_buyuk | ✅ | 209.8 | 21 |  |
| zk_iki_hata | zor_iki | ✅ | 139.8 | 18 |  |
| zk_yeni_tip | zor_ozellik | ❌ | 148.3 | 23 | AttributeError: PERCENT |
