# Ölçüm: son-yeni-gercek-1

2026-11-14 22:53 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 10/11 (%91)**, %95 güven aralığı %62–%98

Ortanca süre 42.7 sn, toplam 569 sn, zaman aşımı 0. Tamamlanan tur 7/11. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 1.

| Tür | Başarı |
|---|---|
| gercek_hata | 7/8 |
| gercek_ozellik | 3/3 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| ct_lru_okuma | gercek_hata | ✅ | 72.2 | 30 | adım sınırı |
| ct_ttl_sinir | gercek_hata | ✅ | 19.6 | 14 |  |
| ct_kapasite | gercek_hata | ✅ | 69.2 | 28 | gereksiz dosya: cachetools/__init__.py; adım sınırı |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 34.4 | 18 |  |
| mi_maxsplit | gercek_hata | ❌ | 65.2 | 20 | adım sınırı; UnboundLocalError: cannot access local variable 'split_limit_reached' where it is not asso |
| mi_partition | gercek_hata | ✅ | 35.2 | 13 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ✅ | 75.6 | 28 | adım sınırı |
| ck_aralik | gercek_hata | ✅ | 42.7 | 19 |  |
| ck_secim | gercek_hata | ✅ | 35.8 | 14 |  |
| ck_secenek_sirasi | gercek_hata | ✅ | 37.7 | 19 |  |
| ck_yeni_ozellik | gercek_ozellik | ✅ | 81.0 | 21 |  |
