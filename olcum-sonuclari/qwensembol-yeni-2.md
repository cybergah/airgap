# Ölçüm: qwensembol-yeni-2

2026-11-24 04:18 · model `qwen3.6:35b-a3b` · 1 tekrar · harita 1000

**Başarı: 6/9 (%67)**, %95 güven aralığı %35–%88

Ortanca süre 192.3 sn, toplam 2198 sn, zaman aşımı 0. Tamamlanan tur 6/9. Başarısız olup bunu söylemeyen 1. Gereksiz dosya değiştiren 1.

| Tür | Başarı |
|---|---|
| zor_buyuk | 1/2 |
| zor_iki | 1/1 |
| zor_ozellik | 2/3 |
| zor_uzak | 2/2 |
| zor_yaniltici | 0/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| zc_anahtar | zor_uzak | ✅ | 59.8 | 14 |  |
| zc_peek | zor_ozellik | ✅ | 489.6 | 41 | tur tamamlanmadı |
| zc_istatistik | zor_yaniltici | ❌ | 435.6 | 18 | model hatası veya boş yanıt; AssertionError: Tuples differ: (1, 2) != (2, 1) |
| zm_chunked_none | zor_uzak | ✅ | 132.0 | 24 |  |
| zm_running_sum | zor_ozellik | ❌ | 243.8 | 36 | test değiştirmek istedi; başarısızlığı söylemedi; gereksiz dosya: README.rst; TypeError: 'int' object is not iterable |
| zm_windowed_adim | zor_buyuk | ❌ | 432.4 | 4 | model hatası veya boş yanıt; FAILED (failures=1) |
| zk_envvar_oncelik | zor_buyuk | ✅ | 80.7 | 14 |  |
| zk_iki_hata | zor_iki | ✅ | 131.4 | 21 |  |
| zk_yeni_tip | zor_ozellik | ✅ | 192.3 | 25 |  |
