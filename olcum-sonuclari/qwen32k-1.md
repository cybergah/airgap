# Ölçüm: qwen32k-1

2026-11-25 15:10 · model `qwen3.6:35b-a3b` · 1 tekrar · harita 1000

**Başarı: 8/9 (%89)**, %95 güven aralığı %56–%98

Ortanca süre 315.3 sn, toplam 3168 sn, zaman aşımı 0. Tamamlanan tur 8/9. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 1.

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
| zc_anahtar | zor_uzak | ✅ | 92.0 | 13 |  |
| zc_peek | zor_ozellik | ✅ | 474.9 | 31 |  |
| zc_istatistik | zor_yaniltici | ✅ | 262.5 | 19 |  |
| zm_chunked_none | zor_uzak | ✅ | 272.5 | 20 |  |
| zm_running_sum | zor_ozellik | ❌ | 406.3 | 38 | test değiştirmek istedi; gereksiz dosya: README.rst; tur tamamlanmadı; TypeError: 'int' object is not iterable |
| zm_windowed_adim | zor_buyuk | ✅ | 542.1 | 12 |  |
| zk_envvar_oncelik | zor_buyuk | ✅ | 315.3 | 20 |  |
| zk_iki_hata | zor_iki | ✅ | 258.3 | 21 |  |
| zk_yeni_tip | zor_ozellik | ✅ | 543.9 | 30 |  |
