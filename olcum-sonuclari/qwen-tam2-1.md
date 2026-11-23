# Ölçüm: qwen-tam2-1

2026-11-23 05:30 · model `qwen3.6:35b-a3b` · 1 tekrar · harita 1000

**Başarı: 10/11 (%91)**, %95 güven aralığı %62–%98

Ortanca süre 89.5 sn, toplam 1233 sn, zaman aşımı 0. Tamamlanan tur 10/11. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 0.

| Tür | Başarı |
|---|---|
| gercek_hata | 8/8 |
| gercek_ozellik | 2/3 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| ct_lru_okuma | gercek_hata | ✅ | 77.3 | 14 |  |
| ct_ttl_sinir | gercek_hata | ✅ | 79.4 | 14 |  |
| ct_kapasite | gercek_hata | ✅ | 77.2 | 13 |  |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 45.7 | 11 |  |
| mi_maxsplit | gercek_hata | ✅ | 89.5 | 9 |  |
| mi_partition | gercek_hata | ✅ | 69.5 | 9 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 285.1 | 31 | tur tamamlanmadı; TypeError: '<' not supported between instances of 'str' and 'int' |
| ck_aralik | gercek_hata | ✅ | 168.1 | 17 |  |
| ck_secim | gercek_hata | ✅ | 93.5 | 19 |  |
| ck_secenek_sirasi | gercek_hata | ✅ | 113.8 | 20 |  |
| ck_yeni_ozellik | gercek_ozellik | ✅ | 133.7 | 15 |  |
