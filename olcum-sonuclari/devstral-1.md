# Ölçüm: devstral-1

2026-11-23 21:14 · model `devstral-small-2:24b` · 1 tekrar · harita 1000

**Başarı: 3/9 (%33)**, %95 güven aralığı %12–%65

Ortanca süre 418.0 sn, toplam 3707 sn, zaman aşımı 3. Tamamlanan tur 1/9. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 0.

| Tür | Başarı |
|---|---|
| zor_buyuk | 0/2 |
| zor_iki | 0/1 |
| zor_ozellik | 1/3 |
| zor_uzak | 2/2 |
| zor_yaniltici | 0/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| zc_anahtar | zor_uzak | ✅ | 217.1 | 19 | test değiştirmek istedi; model hatası veya boş yanıt |
| zc_peek | zor_ozellik | ❌ | 377.8 | 23 | model hatası veya boş yanıt; AssertionError: 'a' unexpectedly found in LRUCache({'a': 1, 'c': 3}, maxsize=2, currsize=2 |
| zc_istatistik | zor_yaniltici | ❌ | 600 |  | zaman aşımı |
| zm_chunked_none | zor_uzak | ✅ | 299.5 | 26 |  |
| zm_running_sum | zor_ozellik | ❌ | 550.1 | 28 | test değiştirmek istedi; tur tamamlanmadı; FAILED (failures=1) |
| zm_windowed_adim | zor_buyuk | ❌ | 600 |  | zaman aşımı |
| zk_envvar_oncelik | zor_buyuk | ❌ | 44.2 | 9 | tur tamamlanmadı; AssertionError: 'map' != 'env' |
| zk_iki_hata | zor_iki | ❌ | 600 |  | zaman aşımı |
| zk_yeni_tip | zor_ozellik | ✅ | 418.0 | 30 | test değiştirmek istedi; tur tamamlanmadı |
