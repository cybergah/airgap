# Ölçüm: son-yeni-gercek-2

2026-11-14 23:21 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 8/11 (%73)**, %95 güven aralığı %43–%90

Ortanca süre 41.1 sn, toplam 624 sn, zaman aşımı 0. Tamamlanan tur 6/11. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 2.

| Tür | Başarı |
|---|---|
| gercek_hata | 7/8 |
| gercek_ozellik | 1/3 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| ct_lru_okuma | gercek_hata | ❌ | 203.7 | 27 | gereksiz dosya: cachetools/__init__.py; adım sınırı; AttributeError: 'LRUCache' object has no attribute '_LRUCache__data'. Did you mean: '_Cach |
| ct_ttl_sinir | gercek_hata | ✅ | 15.6 | 9 |  |
| ct_kapasite | gercek_hata | ✅ | 32.7 | 18 | gereksiz dosya: cachetools/__init__.py, cachetools/cached.py, cachetools/cac |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 50.8 | 28 | adım sınırı |
| mi_maxsplit | gercek_hata | ✅ | 57.1 | 14 |  |
| mi_partition | gercek_hata | ✅ | 41.1 | 13 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 33.0 | 30 | adım sınırı; ImportError: cannot import name 'every_nth' from 'more_itertools' (/work/more_itertools/__ |
| ck_aralik | gercek_hata | ✅ | 67.4 | 26 | adım sınırı |
| ck_secim | gercek_hata | ✅ | 39.5 | 16 |  |
| ck_secenek_sirasi | gercek_hata | ✅ | 51.8 | 28 |  |
| ck_yeni_ozellik | gercek_ozellik | ❌ | 30.8 | 9 | model hatası veya boş yanıt; ImportError: cannot import name 'truncate' from 'click.utils' (/work/src/click/utils.py) |
