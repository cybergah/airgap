# Ölçüm: qwensembol-yeni-3

2026-11-24 05:19 · model `qwen3.6:35b-a3b` · 1 tekrar · harita 1000

**Başarı: 7/9 (%78)**, %95 güven aralığı %45–%94

Ortanca süre 122.7 sn, toplam 1364 sn, zaman aşımı 0. Tamamlanan tur 7/9. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 1.

| Tür | Başarı |
|---|---|
| zor_buyuk | 2/2 |
| zor_iki | 1/1 |
| zor_ozellik | 1/3 |
| zor_uzak | 2/2 |
| zor_yaniltici | 1/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| zc_anahtar | zor_uzak | ✅ | 56.2 | 13 |  |
| zc_peek | zor_ozellik | ❌ | 298.9 | 30 | tur tamamlanmadı; FAILED (failures=1) |
| zc_istatistik | zor_yaniltici | ✅ | 108.3 | 15 |  |
| zm_chunked_none | zor_uzak | ✅ | 122.7 | 18 |  |
| zm_running_sum | zor_ozellik | ❌ | 240.3 | 42 | test değiştirmek istedi; gereksiz dosya: README.rst; model hatası veya boş yanıt; TypeError: 'int' object is not iterable |
| zm_windowed_adim | zor_buyuk | ✅ | 112.1 | 12 |  |
| zk_envvar_oncelik | zor_buyuk | ✅ | 121.5 | 19 |  |
| zk_iki_hata | zor_iki | ✅ | 127.8 | 16 |  |
| zk_yeni_tip | zor_ozellik | ✅ | 175.7 | 24 |  |
