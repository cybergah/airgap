# Ölçüm: guclendirme-oncesi

2026-11-12 12:10 · model `gpt-oss:20b` · 3 tekrar · harita 1000

**Başarı: 25/33 (%76)**, %95 güven aralığı %59–%87

Ortanca süre 49.2 sn, toplam 1692 sn, zaman aşımı 0. Tamamlanan tur 23/33. Başarısız olup bunu söylemeyen 2. Gereksiz dosya değiştiren 9.

| Tür | Başarı |
|---|---|
| gercek_hata | 20/24 |
| gercek_ozellik | 5/9 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| ct_lru_okuma | gercek_hata | ✅ | 63.1 | 19 | gereksiz dosya: cachetools/__init__.py |
| ct_ttl_sinir | gercek_hata | ✅ | 54.8 | 24 |  |
| ct_kapasite | gercek_hata | ✅ | 56.6 | 26 | gereksiz dosya: cachetools/__init__.py; adım sınırı |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 42.8 | 19 | gereksiz dosya: cachetools/__init__.py |
| mi_maxsplit | gercek_hata | ❌ | 136.4 | 30 | adım sınırı; AssertionError: Lists differ: [[], ['b']] != [['a'], ['c', 'd', 'c', 'b', 'a']] |
| mi_partition | gercek_hata | ✅ | 26.2 | 8 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 36.8 | 30 | adım sınırı; ImportError: cannot import name 'every_nth' from 'more_itertools' (/work/more_itertools/__ |
| ck_aralik | gercek_hata | ✅ | 38.9 | 19 |  |
| ck_secim | gercek_hata | ✅ | 47.5 | 19 | gereksiz dosya: src/click/__init__.py |
| ck_secenek_sirasi | gercek_hata | ❌ | 40.0 | 20 | başarısızlığı söylemedi; AssertionError: '-v, --verbose' not found in 'Usage: k [OPTIONS]\n\nOptions:\n  --verbose, |
| ck_yeni_ozellik | gercek_ozellik | ✅ | 69.6 | 17 | gereksiz dosya: src/click/_truncate.py |
| ct_lru_okuma | gercek_hata | ✅ | 26.1 | 13 |  |
| ct_ttl_sinir | gercek_hata | ✅ | 61.7 | 18 | gereksiz dosya: tests/__init__.py |
| ct_kapasite | gercek_hata | ✅ | 49.7 | 28 | gereksiz dosya: cachetools/__init__.py; adım sınırı |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 31.1 | 19 |  |
| mi_maxsplit | gercek_hata | ✅ | 49.7 | 8 |  |
| mi_partition | gercek_hata | ✅ | 23.3 | 9 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 72.7 | 26 | adım sınırı; AttributeError: module 'more_itertools.more' has no attribute 'every_nth' |
| ck_aralik | gercek_hata | ✅ | 41.8 | 18 |  |
| ck_secim | gercek_hata | ✅ | 71.9 | 30 | adım sınırı |
| ck_secenek_sirasi | gercek_hata | ✅ | 49.2 | 28 |  |
| ck_yeni_ozellik | gercek_ozellik | ❌ | 70.5 | 29 | adım sınırı; AttributeError: truncate |
| ct_lru_okuma | gercek_hata | ✅ | 59.1 | 18 |  |
| ct_ttl_sinir | gercek_hata | ✅ | 21.4 | 15 |  |
| ct_kapasite | gercek_hata | ✅ | 81.3 | 26 | gereksiz dosya: tests/__init__.py; adım sınırı |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 63.1 | 19 | gereksiz dosya: cachetools/__init__.py, src/__init__.py |
| mi_maxsplit | gercek_hata | ✅ | 72.9 | 11 |  |
| mi_partition | gercek_hata | ✅ | 33.9 | 9 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 31.4 | 28 | adım sınırı; ImportError: cannot import name 'every_nth' from 'more_itertools' (/work/more_itertools/__ |
| ck_aralik | gercek_hata | ❌ | 38.9 | 18 | başarısızlığı söylemedi; FAILED (errors=1) |
| ck_secim | gercek_hata | ✅ | 49.8 | 18 |  |
| ck_secenek_sirasi | gercek_hata | ❌ | 39.7 | 29 | adım sınırı; AssertionError: '-v, --verbose' not found in 'Usage: k [OPTIONS]\n\nOptions:\n  --verbose, |
| ck_yeni_ozellik | gercek_ozellik | ✅ | 40.1 | 14 |  |
