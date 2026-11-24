# Ölçüm: qwensembol-eski-3

2026-11-24 04:56 · model `qwen3.6:35b-a3b` · 1 tekrar · harita 1000

**Başarı: 5/9 (%56)**, %95 güven aralığı %27–%81

Ortanca süre 212.6 sn, toplam 2258 sn, zaman aşımı 1. Tamamlanan tur 5/9. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 0.

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
| zc_anahtar | zor_uzak | ✅ | 74.1 | 20 |  |
| zc_peek | zor_ozellik | ❌ | 315.3 | 43 | tur tamamlanmadı; AssertionError: 'a' unexpectedly found in LRUCache({'a': 1, 'c': 3}, maxsize=2, currsize=2 |
| zc_istatistik | zor_yaniltici | ❌ | 600 |  | zaman aşımı |
| zm_chunked_none | zor_uzak | ✅ | 102.0 | 21 |  |
| zm_running_sum | zor_ozellik | ❌ | 212.6 | 34 | test değiştirmek istedi; model hatası veya boş yanıt; AssertionError: Lists differ: [] != [1, 3, 6, 10] |
| zm_windowed_adim | zor_buyuk | ❌ | 532.8 | 12 | model hatası veya boş yanıt; AssertionError: Lists differ: [(1, 2), (2, 3), (3, 4), (4, None)] != [(1, 2), (2, 3), (3,  |
| zk_envvar_oncelik | zor_buyuk | ✅ | 109.5 | 19 |  |
| zk_iki_hata | zor_iki | ✅ | 95.6 | 20 |  |
| zk_yeni_tip | zor_ozellik | ✅ | 216.5 | 30 |  |
