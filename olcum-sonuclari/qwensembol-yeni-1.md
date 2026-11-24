# Ölçüm: qwensembol-yeni-1

2026-11-24 03:03 · model `qwen3.6:35b-a3b` · 1 tekrar · harita 1000

**Başarı: 6/9 (%67)**, %95 güven aralığı %35–%88

Ortanca süre 110.8 sn, toplam 1805 sn, zaman aşımı 0. Tamamlanan tur 6/9. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 0.

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
| zc_anahtar | zor_uzak | ✅ | 97.1 | 18 |  |
| zc_peek | zor_ozellik | ❌ | 402.8 | 72 | model hatası veya boş yanıt; AttributeError: 'LRUCache' object has no attribute 'peek' |
| zc_istatistik | zor_yaniltici | ✅ | 72.6 | 17 |  |
| zm_chunked_none | zor_uzak | ✅ | 86.2 | 18 |  |
| zm_running_sum | zor_ozellik | ❌ | 157.7 | 29 | model hatası veya boş yanıt; NameError: name 'collections' is not defined. Did you forget to import 'collections'? |
| zm_windowed_adim | zor_buyuk | ❌ | 552.8 | 6 | model hatası veya boş yanıt; FAILED (failures=1) |
| zk_envvar_oncelik | zor_buyuk | ✅ | 98.7 | 20 |  |
| zk_iki_hata | zor_iki | ✅ | 110.8 | 17 |  |
| zk_yeni_tip | zor_ozellik | ✅ | 226.5 | 29 |  |
