# Ölçüm: model-gpt-oss-3

2026-11-22 15:51 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 10/11 (%91)**, %95 güven aralığı %62–%98

Ortanca süre 39.4 sn, toplam 600 sn, zaman aşımı 0. Tamamlanan tur 9/11. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 1.

| Tür | Başarı |
|---|---|
| gercek_hata | 8/8 |
| gercek_ozellik | 2/3 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| ct_lru_okuma | gercek_hata | ✅ | 92.8 | 29 | gereksiz dosya: cachetools/__init__.py, tests/__init__.py; tur tamamlanmadı |
| ct_ttl_sinir | gercek_hata | ✅ | 22.7 | 13 |  |
| ct_kapasite | gercek_hata | ✅ | 36.2 | 13 |  |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 36.6 | 19 |  |
| mi_maxsplit | gercek_hata | ✅ | 39.4 | 9 |  |
| mi_partition | gercek_hata | ✅ | 33.0 | 7 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 76.1 | 29 | tur tamamlanmadı; ImportError: cannot import name 'every_nth' from 'more_itertools' (/work/more_itertools/__ |
| ck_aralik | gercek_hata | ✅ | 43.2 | 17 |  |
| ck_secim | gercek_hata | ✅ | 39.4 | 19 |  |
| ck_secenek_sirasi | gercek_hata | ✅ | 49.9 | 18 | test değiştirmek istedi |
| ck_yeni_ozellik | gercek_ozellik | ✅ | 130.5 | 26 |  |
