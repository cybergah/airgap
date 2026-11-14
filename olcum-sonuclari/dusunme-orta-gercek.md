# Ölçüm: dusunme-orta-gercek

2026-11-12 20:39 · model `gpt-oss:20b` · 3 tekrar · harita 1000

**Başarı: 25/33 (%76)**, %95 güven aralığı %59–%87

Ortanca süre 39.6 sn, toplam 1596 sn, zaman aşımı 0. Tamamlanan tur 19/33. Başarısız olup bunu söylemeyen 1. Gereksiz dosya değiştiren 8.

| Tür | Başarı |
|---|---|
| gercek_hata | 20/24 |
| gercek_ozellik | 5/9 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| ct_lru_okuma | gercek_hata | ✅ | 95.3 | 19 | model hatası veya boş yanıt |
| ct_ttl_sinir | gercek_hata | ✅ | 45.0 | 30 | gereksiz dosya: cachetools/__init__.py; adım sınırı |
| ct_kapasite | gercek_hata | ✅ | 36.3 | 14 |  |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 40.8 | 27 | gereksiz dosya: cachetools/__init__.py; adım sınırı |
| mi_maxsplit | gercek_hata | ✅ | 105.6 | 27 | adım sınırı |
| mi_partition | gercek_hata | ✅ | 31.6 | 13 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 43.8 | 26 | gereksiz dosya: more_itertools/recipes.py; adım sınırı; AttributeError: module 'more_itertools.recipes' has no attribute 'every_nth' |
| ck_aralik | gercek_hata | ✅ | 59.0 | 19 |  |
| ck_secim | gercek_hata | ✅ | 36.5 | 17 |  |
| ck_secenek_sirasi | gercek_hata | ❌ | 41.3 | 28 | adım sınırı; AssertionError: '-v, --verbose' not found in 'Usage: k [OPTIONS]\n\nOptions:\n  --verbose, |
| ck_yeni_ozellik | gercek_ozellik | ❌ | 88.6 | 27 | adım sınırı; AttributeError: truncate |
| ct_lru_okuma | gercek_hata | ❌ | 17.0 | 17 | ajan durdurdu: tekrar; AssertionError: 'a' not found in LRUCache({'b': 2, 'c': 3}, maxsize=2, currsize=2) |
| ct_ttl_sinir | gercek_hata | ✅ | 39.1 | 19 |  |
| ct_kapasite | gercek_hata | ✅ | 42.8 | 19 | gereksiz dosya: cachetools/__init__.py |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 35.1 | 15 |  |
| mi_maxsplit | gercek_hata | ✅ | 97.5 | 12 |  |
| mi_partition | gercek_hata | ✅ | 47.9 | 12 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 39.6 | 30 | adım sınırı; ImportError: cannot import name 'every_nth' from 'more_itertools' (/work/more_itertools/__ |
| ck_aralik | gercek_hata | ✅ | 30.0 | 17 |  |
| ck_secim | gercek_hata | ✅ | 44.5 | 26 | adım sınırı |
| ck_secenek_sirasi | gercek_hata | ✅ | 21.4 | 19 |  |
| ck_yeni_ozellik | gercek_ozellik | ✅ | 34.4 | 17 |  |
| ct_lru_okuma | gercek_hata | ✅ | 34.3 | 19 | gereksiz dosya: cachetools/__init__.py, tests/__init__.py |
| ct_ttl_sinir | gercek_hata | ✅ | 26.2 | 18 | gereksiz dosya: cachetools/__init__.py |
| ct_kapasite | gercek_hata | ✅ | 30.0 | 19 | gereksiz dosya: cachetools/__init__.py |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 19.0 | 12 |  |
| mi_maxsplit | gercek_hata | ✅ | 125.2 | 29 | adım sınırı |
| mi_partition | gercek_hata | ✅ | 92.9 | 26 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 22.2 | 30 | adım sınırı; ImportError: cannot import name 'every_nth' from 'more_itertools' (/work/more_itertools/__ |
| ck_aralik | gercek_hata | ❌ | 46.0 | 16 | başarısızlığı söylemedi; FAILED (errors=1) |
| ck_secim | gercek_hata | ✅ | 38.7 | 19 |  |
| ck_secenek_sirasi | gercek_hata | ❌ | 23.8 | 29 | adım sınırı; AssertionError: '-v, --verbose' not found in 'Usage: k [OPTIONS]\n\nOptions:\n  --verbose, |
| ck_yeni_ozellik | gercek_ozellik | ✅ | 64.3 | 30 | gereksiz dosya: src/click/_truncate.py; adım sınırı |
