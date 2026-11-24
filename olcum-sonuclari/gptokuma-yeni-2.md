# Ölçüm: gptokuma-yeni-2

2026-11-24 06:19 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 4/9 (%44)**, %95 güven aralığı %19–%73

Ortanca süre 65.7 sn, toplam 583 sn, zaman aşımı 0. Tamamlanan tur 4/9. Başarısız olup bunu söylemeyen 1. Gereksiz dosya değiştiren 1.

| Tür | Başarı |
|---|---|
| zor_buyuk | 1/2 |
| zor_iki | 1/1 |
| zor_ozellik | 0/3 |
| zor_uzak | 2/2 |
| zor_yaniltici | 0/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| zc_anahtar | zor_uzak | ✅ | 104.4 | 29 | gereksiz dosya: cachetools/__init__.py, tests/__init__.py; tur tamamlanmadı |
| zc_peek | zor_ozellik | ❌ | 69.2 | 26 | model hatası veya boş yanıt; AttributeError: 'LRUCache' object has no attribute 'peek' |
| zc_istatistik | zor_yaniltici | ❌ | 66.9 | 30 | tur tamamlanmadı; AssertionError: Tuples differ: (1, 2) != (2, 1) |
| zm_chunked_none | zor_uzak | ✅ | 89.1 | 19 |  |
| zm_running_sum | zor_ozellik | ❌ | 65.7 | 30 | tur tamamlanmadı; FAILED (failures=1) |
| zm_windowed_adim | zor_buyuk | ✅ | 45.5 | 11 |  |
| zk_envvar_oncelik | zor_buyuk | ❌ | 50.1 | 22 | test değiştirmek istedi; başarısızlığı söylemedi; AssertionError: 'map' != 'env' |
| zk_iki_hata | zor_iki | ✅ | 36.5 | 19 |  |
| zk_yeni_tip | zor_ozellik | ❌ | 55.3 | 28 | model hatası veya boş yanıt; AttributeError: PERCENT |
