# Ölçüm: qwensembol-eski-1

2026-11-24 02:33 · model `qwen3.6:35b-a3b` · 1 tekrar · harita 1000

**Başarı: 8/9 (%89)**, %95 güven aralığı %56–%98

Ortanca süre 171.0 sn, toplam 1848 sn, zaman aşımı 0. Tamamlanan tur 6/9. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 0.

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
| zc_anahtar | zor_uzak | ✅ | 114.8 | 17 |  |
| zc_peek | zor_ozellik | ✅ | 296.3 | 37 | tur tamamlanmadı |
| zc_istatistik | zor_yaniltici | ✅ | 172.1 | 24 |  |
| zm_chunked_none | zor_uzak | ✅ | 95.9 | 18 |  |
| zm_running_sum | zor_ozellik | ✅ | 249.7 | 38 | test değiştirmek istedi; tur tamamlanmadı |
| zm_windowed_adim | zor_buyuk | ❌ | 500.7 | 4 | model hatası veya boş yanıt; FAILED (failures=1) |
| zk_envvar_oncelik | zor_buyuk | ✅ | 108.7 | 20 |  |
| zk_iki_hata | zor_iki | ✅ | 138.8 | 21 |  |
| zk_yeni_tip | zor_ozellik | ✅ | 171.0 | 21 |  |
