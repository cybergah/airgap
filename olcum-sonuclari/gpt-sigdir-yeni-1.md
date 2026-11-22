# Ölçüm: gpt-sigdir-yeni-1

2026-11-22 21:23 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 7/11 (%64)**, %95 güven aralığı %35–%85

Ortanca süre 72.8 sn, toplam 919 sn, zaman aşımı 0. Tamamlanan tur 6/11. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 1.

| Tür | Başarı |
|---|---|
| gercek_hata | 6/8 |
| gercek_ozellik | 1/3 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| ct_lru_okuma | gercek_hata | ✅ | 100.9 | 28 | tur tamamlanmadı |
| ct_ttl_sinir | gercek_hata | ✅ | 28.6 | 16 |  |
| ct_kapasite | gercek_hata | ❌ | 92.7 | 30 | gereksiz dosya: cachetools/__init__.py, sitecustomize.py; tur tamamlanmadı; AssertionError: 1 != 2 |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 54.1 | 18 |  |
| mi_maxsplit | gercek_hata | ✅ | 72.8 | 14 |  |
| mi_partition | gercek_hata | ✅ | 46.2 | 5 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 157.7 | 28 | model hatası veya boş yanıt; AttributeError: module 'more_itertools.more' has no attribute 'every_nth' |
| ck_aralik | gercek_hata | ❌ | 108.1 | 29 | tur tamamlanmadı; FAILED (errors=1) |
| ck_secim | gercek_hata | ✅ | 41.2 | 16 |  |
| ck_secenek_sirasi | gercek_hata | ✅ | 53.3 | 28 |  |
| ck_yeni_ozellik | gercek_ozellik | ❌ | 163.7 | 21 | model hatası veya boş yanıt; AttributeError: truncate |
