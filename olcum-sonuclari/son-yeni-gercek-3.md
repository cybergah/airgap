# Ölçüm: son-yeni-gercek-3

2026-11-14 23:44 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 10/11 (%91)**, %95 güven aralığı %62–%98

Ortanca süre 45.9 sn, toplam 513 sn, zaman aşımı 0. Tamamlanan tur 8/11. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 2.

| Tür | Başarı |
|---|---|
| gercek_hata | 8/8 |
| gercek_ozellik | 2/3 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| ct_lru_okuma | gercek_hata | ✅ | 31.4 | 19 |  |
| ct_ttl_sinir | gercek_hata | ✅ | 53.5 | 29 | gereksiz dosya: cachetools/__init__.py; adım sınırı |
| ct_kapasite | gercek_hata | ✅ | 22.9 | 16 |  |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 23.7 | 16 |  |
| mi_maxsplit | gercek_hata | ✅ | 49.0 | 10 |  |
| mi_partition | gercek_hata | ✅ | 31.5 | 11 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 45.9 | 30 | adım sınırı; ImportError: cannot import name 'every_nth' from 'more_itertools' (/work/more_itertools/__ |
| ck_aralik | gercek_hata | ✅ | 94.5 | 22 | adım sınırı |
| ck_secim | gercek_hata | ✅ | 57.1 | 22 |  |
| ck_secenek_sirasi | gercek_hata | ✅ | 40.1 | 19 |  |
| ck_yeni_ozellik | gercek_ozellik | ✅ | 63.2 | 21 | gereksiz dosya: src/click/__pycache__/__init__.cpython-313.pyc |
