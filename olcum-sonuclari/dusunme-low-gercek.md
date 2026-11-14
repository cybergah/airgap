# Ölçüm: dusunme-low-gercek

2026-11-12 21:09 · model `gpt-oss:20b` · 3 tekrar · harita 1000

**Başarı: 21/33 (%64)**, %95 güven aralığı %47–%78

Ortanca süre 17.5 sn, toplam 695 sn, zaman aşımı 0. Tamamlanan tur 32/33. Başarısız olup bunu söylemeyen 8. Gereksiz dosya değiştiren 4.

| Tür | Başarı |
|---|---|
| gercek_hata | 16/24 |
| gercek_ozellik | 5/9 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| ct_lru_okuma | gercek_hata | ❌ | 27.1 | 14 | başarısızlığı söylemedi; ModuleNotFoundError: No module named 'cachetools._cache' |
| ct_ttl_sinir | gercek_hata | ✅ | 17.5 | 16 |  |
| ct_kapasite | gercek_hata | ✅ | 11.2 | 10 |  |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 12.9 | 10 |  |
| mi_maxsplit | gercek_hata | ✅ | 25.7 | 7 |  |
| mi_partition | gercek_hata | ✅ | 22.7 | 12 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 19.3 | 9 | ImportError: cannot import name 'every_nth' from 'more_itertools' (/work/more_itertools/__ |
| ck_aralik | gercek_hata | ✅ | 9.5 | 8 |  |
| ck_secim | gercek_hata | ✅ | 10.0 | 11 |  |
| ck_secenek_sirasi | gercek_hata | ❌ | 30.1 | 19 | başarısızlığı söylemedi; gereksiz dosya: src/click/core.py; AssertionError: '-v, --verbose' not found in 'Usage: k [OPTIONS]\n\nOptions:\n  --verbose, |
| ck_yeni_ozellik | gercek_ozellik | ❌ | 31.1 | 12 | başarısızlığı söylemedi; TypeError: 'module' object is not callable |
| ct_lru_okuma | gercek_hata | ❌ | 12.4 | 11 | başarısızlığı söylemedi; AttributeError: 'LRUCache' object has no attribute '_Cache__touch'. Did you mean: '_LRUCac |
| ct_ttl_sinir | gercek_hata | ✅ | 8.6 | 7 |  |
| ct_kapasite | gercek_hata | ✅ | 14.5 | 9 |  |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 13.3 | 7 |  |
| mi_maxsplit | gercek_hata | ❌ | 71.9 | 23 | başarısızlığı söylemedi; gereksiz dosya: more_itertools/__init__.py; ImportError: cannot import name 'distinct_permutations' from 'more_itertools.more' (/work/ |
| mi_partition | gercek_hata | ✅ | 23.1 | 14 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 29.8 | 19 | başarısızlığı söylemedi; gereksiz dosya: more_itertools/recipes.py; ImportError: cannot import name 'every_nth' from 'more_itertools' (/work/more_itertools/__ |
| ck_aralik | gercek_hata | ✅ | 13.1 | 9 |  |
| ck_secim | gercek_hata | ✅ | 10.4 | 11 |  |
| ck_secenek_sirasi | gercek_hata | ❌ | 15.9 | 14 | başarısızlığı söylemedi; gereksiz dosya: src/click/core.py; AttributeError: 'Option' object has no attribute 'param_decls'. Did you mean: '_parse_decl |
| ck_yeni_ozellik | gercek_ozellik | ✅ | 31.4 | 10 |  |
| ct_lru_okuma | gercek_hata | ❌ | 10.5 | 5 | AssertionError: 'a' not found in LRUCache({'b': 2, 'c': 3}, maxsize=2, currsize=2) |
| ct_ttl_sinir | gercek_hata | ✅ | 8.6 | 8 |  |
| ct_kapasite | gercek_hata | ✅ | 24.4 | 19 |  |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 11.1 | 5 |  |
| mi_maxsplit | gercek_hata | ✅ | 47.4 | 19 |  |
| mi_partition | gercek_hata | ✅ | 25.7 | 13 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 34.5 | 26 | adım sınırı; AttributeError: module 'more_itertools.more' has no attribute 'every_nth' |
| ck_aralik | gercek_hata | ❌ | 19.4 | 5 | başarısızlığı söylemedi; FAILED (errors=1) |
| ck_secim | gercek_hata | ✅ | 8.1 | 9 |  |
| ck_secenek_sirasi | gercek_hata | ❌ | 14.3 | 12 | AssertionError: '-v, --verbose' not found in 'Usage: k [OPTIONS]\n\nOptions:\n  --verbose, |
| ck_yeni_ozellik | gercek_ozellik | ✅ | 29.6 | 12 |  |
