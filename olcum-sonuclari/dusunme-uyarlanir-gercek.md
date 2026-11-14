# Ölçüm: dusunme-uyarlanir-gercek

2026-11-12 22:11 · model `gpt-oss:20b` · 3 tekrar · harita 1000

**Başarı: 24/33 (%73)**, %95 güven aralığı %56–%85

Ortanca süre 29.5 sn, toplam 1348 sn, zaman aşımı 0. Tamamlanan tur 24/33. Başarısız olup bunu söylemeyen 3. Gereksiz dosya değiştiren 8.

| Tür | Başarı |
|---|---|
| gercek_hata | 19/24 |
| gercek_ozellik | 5/9 |

## Karşılaştırma: dusunme-orta-gercek

Önceki: 25/33
Kötüleşen: ck_secim, ct_ttl_sinir
İyileşen: ck_aralik

Güven aralıkları çakışıyorsa fark rastlantı olabilir.

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| ct_lru_okuma | gercek_hata | ✅ | 37.4 | 19 |  |
| ct_ttl_sinir | gercek_hata | ✅ | 27.7 | 15 | gereksiz dosya: cachetools/__init__.py |
| ct_kapasite | gercek_hata | ✅ | 58.4 | 26 | gereksiz dosya: cachetools.py, cachetools/__init__.py, cachetools/func.py, c |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 13.5 | 6 |  |
| mi_maxsplit | gercek_hata | ✅ | 108.3 | 8 |  |
| mi_partition | gercek_hata | ✅ | 72.2 | 27 | gereksiz dosya: more_itertools/more.py; adım sınırı |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 22.7 | 26 | adım sınırı; AttributeError: module 'more_itertools.more' has no attribute 'every_nth' |
| ck_aralik | gercek_hata | ✅ | 43.8 | 14 |  |
| ck_secim | gercek_hata | ❌ | 59.6 | 28 | FAILED (errors=1) |
| ck_secenek_sirasi | gercek_hata | ❌ | 24.2 | 29 | adım sınırı; AssertionError: '-v, --verbose' not found in 'Usage: k [OPTIONS]\n\nOptions:\n  --verbose, |
| ck_yeni_ozellik | gercek_ozellik | ✅ | 107.2 | 18 |  |
| ct_lru_okuma | gercek_hata | ✅ | 62.8 | 26 | gereksiz dosya: cachetools/__init__.py; adım sınırı |
| ct_ttl_sinir | gercek_hata | ❌ | 23.1 | 14 | başarısızlığı söylemedi; AssertionError: 'a' unexpectedly found in TTLCache({}, maxsize=5, currsize=0) |
| ct_kapasite | gercek_hata | ✅ | 23.9 | 16 |  |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 17.0 | 11 |  |
| mi_maxsplit | gercek_hata | ✅ | 18.7 | 5 |  |
| mi_partition | gercek_hata | ✅ | 16.8 | 7 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 41.6 | 27 | gereksiz dosya: more_itertools/recipes.py; adım sınırı; AttributeError: module 'more_itertools.recipes' has no attribute 'nth_combination'. Did yo |
| ck_aralik | gercek_hata | ✅ | 12.7 | 9 |  |
| ck_secim | gercek_hata | ✅ | 29.5 | 15 |  |
| ck_secenek_sirasi | gercek_hata | ✅ | 33.6 | 22 |  |
| ck_yeni_ozellik | gercek_ozellik | ✅ | 35.1 | 13 | gereksiz dosya: src/click/_truncate.py |
| ct_lru_okuma | gercek_hata | ❌ | 26.2 | 16 | başarısızlığı söylemedi; gereksiz dosya: cachetools/__init__.py; KeyError: 'a' |
| ct_ttl_sinir | gercek_hata | ✅ | 43.5 | 30 | gereksiz dosya: cachetools/__init__.py, tests/__init__.py; adım sınırı |
| ct_kapasite | gercek_hata | ✅ | 36.6 | 11 |  |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 19.5 | 8 |  |
| mi_maxsplit | gercek_hata | ✅ | 131.1 | 23 |  |
| mi_partition | gercek_hata | ✅ | 27.4 | 10 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 75.8 | 26 | adım sınırı; AttributeError: module 'more_itertools.more' has no attribute 'every_nth' |
| ck_aralik | gercek_hata | ✅ | 20.7 | 10 | ajan durdurdu: tekrar |
| ck_secim | gercek_hata | ✅ | 28.5 | 11 |  |
| ck_secenek_sirasi | gercek_hata | ❌ | 34.0 | 30 | adım sınırı; AssertionError: '-v, --verbose' not found in 'Usage: k [OPTIONS]\n\nOptions:\n  --verbose, |
| ck_yeni_ozellik | gercek_ozellik | ❌ | 14.7 | 11 | başarısızlığı söylemedi; AttributeError: truncate |
