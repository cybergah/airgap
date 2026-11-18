# Ölçüm: son-eski-gercek-2

2026-11-14 23:06 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 8/11 (%73)**, %95 güven aralığı %43–%90

Ortanca süre 45.1 sn, toplam 543 sn, zaman aşımı 0. Tamamlanan tur 7/11. Başarısız olup bunu söylemeyen 1. Gereksiz dosya değiştiren 2.

| Tür | Başarı |
|---|---|
| gercek_hata | 7/8 |
| gercek_ozellik | 1/3 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| ct_lru_okuma | gercek_hata | ✅ | 49.3 | 29 | gereksiz dosya: cachetools/__init__.py; adım sınırı |
| ct_ttl_sinir | gercek_hata | ✅ | 20.7 | 17 |  |
| ct_kapasite | gercek_hata | ✅ | 60.0 | 30 | gereksiz dosya: cachetools/__init__.py, tests/__init__.py; adım sınırı |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 21.1 | 9 |  |
| mi_maxsplit | gercek_hata | ❌ | 145.7 | 25 | adım sınırı; AssertionError: Lists differ: ['a', 'cdc', 'a'] != [['a'], ['c', 'd', 'c', 'b', 'a']] |
| mi_partition | gercek_hata | ✅ | 42.3 | 11 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 34.5 | 27 | adım sınırı; ImportError: cannot import name 'every_nth' from 'more_itertools' (/work/more_itertools/__ |
| ck_aralik | gercek_hata | ✅ | 45.1 | 18 |  |
| ck_secim | gercek_hata | ✅ | 28.9 | 29 |  |
| ck_secenek_sirasi | gercek_hata | ✅ | 46.7 | 26 |  |
| ck_yeni_ozellik | gercek_ozellik | ❌ | 48.9 | 15 | başarısızlığı söylemedi; AttributeError: truncate |
