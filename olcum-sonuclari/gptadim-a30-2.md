# Ölçüm: gptadim-a30-2

2026-11-24 00:31 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 5/9 (%56)**, %95 güven aralığı %27–%81

Ortanca süre 52.3 sn, toplam 480 sn, zaman aşımı 0. Tamamlanan tur 4/9. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 0.

| Tür | Başarı |
|---|---|
| zor_buyuk | 2/2 |
| zor_iki | 1/1 |
| zor_ozellik | 0/3 |
| zor_uzak | 2/2 |
| zor_yaniltici | 0/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| zc_anahtar | zor_uzak | ✅ | 19.3 | 9 |  |
| zc_peek | zor_ozellik | ❌ | 73.3 | 29 | model hatası veya boş yanıt; AssertionError: 'a' unexpectedly found in LRUCache({'a': 1, 'c': 3}, maxsize=2, currsize=2 |
| zc_istatistik | zor_yaniltici | ❌ | 54.6 | 29 | tur tamamlanmadı; AssertionError: Tuples differ: (1, 2) != (2, 1) |
| zm_chunked_none | zor_uzak | ✅ | 61.0 | 30 | tur tamamlanmadı |
| zm_running_sum | zor_ozellik | ❌ | 52.3 | 30 | tur tamamlanmadı; FAILED (failures=1) |
| zm_windowed_adim | zor_buyuk | ✅ | 52.1 | 12 |  |
| zk_envvar_oncelik | zor_buyuk | ✅ | 47.7 | 18 |  |
| zk_iki_hata | zor_iki | ✅ | 40.8 | 19 |  |
| zk_yeni_tip | zor_ozellik | ❌ | 79.2 | 28 | model hatası veya boş yanıt; AttributeError: PERCENT |
