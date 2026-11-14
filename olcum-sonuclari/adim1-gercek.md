# Ölçüm: adim1-gercek

2026-11-12 22:58 · model `gpt-oss:20b` · 3 tekrar · harita 1000

**Başarı: 21/33 (%64)**, %95 güven aralığı %47–%78

Ortanca süre 40.3 sn, toplam 1572 sn, zaman aşımı 0. Tamamlanan tur 22/33. Başarısız olup bunu söylemeyen 2. Gereksiz dosya değiştiren 5.

| Tür | Başarı |
|---|---|
| gercek_hata | 16/24 |
| gercek_ozellik | 5/9 |

## Karşılaştırma: dusunme-orta-gercek

Önceki: 25/33
Kötüleşen: ck_aralik, ck_secenek_sirasi, ct_ttl_sinir
İyileşen: yok

Güven aralıkları çakışıyorsa fark rastlantı olabilir.

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| ct_lru_okuma | gercek_hata | ✅ | 42.2 | 19 | gereksiz dosya: cachetools/__init__.py |
| ct_ttl_sinir | gercek_hata | ✅ | 40.3 | 24 |  |
| ct_kapasite | gercek_hata | ✅ | 22.4 | 14 |  |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 36.2 | 19 |  |
| mi_maxsplit | gercek_hata | ✅ | 125.5 | 20 |  |
| mi_partition | gercek_hata | ✅ | 37.1 | 8 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 32.8 | 30 | adım sınırı; ImportError: cannot import name 'every_nth' from 'more_itertools' (/work/more_itertools/__ |
| ck_aralik | gercek_hata | ❌ | 42.2 | 16 | başarısızlığı söylemedi; FAILED (errors=1) |
| ck_secim | gercek_hata | ✅ | 36.8 | 13 |  |
| ck_secenek_sirasi | gercek_hata | ❌ | 46.9 | 27 | adım sınırı; AssertionError: '-v, --verbose' not found in 'Usage: k [OPTIONS]\n\nOptions:\n  --verbose, |
| ck_yeni_ozellik | gercek_ozellik | ✅ | 30.1 | 15 |  |
| ct_lru_okuma | gercek_hata | ✅ | 36.6 | 19 |  |
| ct_ttl_sinir | gercek_hata | ❌ | 37.6 | 28 | adım sınırı; AssertionError: 'a' unexpectedly found in TTLCache({}, maxsize=5, currsize=0) |
| ct_kapasite | gercek_hata | ✅ | 45.8 | 18 | gereksiz dosya: cachetools/__init__.py |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 47.5 | 19 | gereksiz dosya: cachetools/__init__.py |
| mi_maxsplit | gercek_hata | ✅ | 33.3 | 8 |  |
| mi_partition | gercek_hata | ✅ | 23.1 | 7 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 43.6 | 30 | adım sınırı; ImportError: cannot import name 'every_nth' from 'more_itertools' (/work/more_itertools/__ |
| ck_aralik | gercek_hata | ❌ | 46.7 | 19 | başarısızlığı söylemedi; FAILED (errors=1) |
| ck_secim | gercek_hata | ✅ | 37.2 | 19 |  |
| ck_secenek_sirasi | gercek_hata | ❌ | 36.7 | 27 | adım sınırı; AssertionError: '-v, --verbose' not found in 'Usage: k [OPTIONS]\n\nOptions:\n  --verbose, |
| ck_yeni_ozellik | gercek_ozellik | ✅ | 50.7 | 13 |  |
| ct_lru_okuma | gercek_hata | ❌ | 30.6 | 29 | adım sınırı; AssertionError: 'a' not found in LRUCache({'b': 2, 'c': 3}, maxsize=2, currsize=2) |
| ct_ttl_sinir | gercek_hata | ✅ | 23.0 | 13 |  |
| ct_kapasite | gercek_hata | ✅ | 196.2 | 30 | gereksiz dosya: cachetools/__init__.py, sitecustomize.py, tmp_test.py; adım sınırı |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 53.7 | 24 |  |
| mi_maxsplit | gercek_hata | ✅ | 62.4 | 16 |  |
| mi_partition | gercek_hata | ✅ | 48.0 | 8 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 45.8 | 29 | gereksiz dosya: more_itertools/recipes.py; adım sınırı; AttributeError: module 'more_itertools.recipes' has no attribute 'every_nth' |
| ck_aralik | gercek_hata | ❌ | 20.5 | 7 | ajan durdurdu: tekrar; FAILED (errors=1) |
| ck_secim | gercek_hata | ✅ | 33.4 | 12 |  |
| ck_secenek_sirasi | gercek_hata | ❌ | 57.5 | 30 | adım sınırı; AssertionError: '-v, --verbose' not found in 'Usage: k [OPTIONS]\n\nOptions:\n  --verbose, |
| ck_yeni_ozellik | gercek_ozellik | ❌ | 69.8 | 25 | adım sınırı; AttributeError: truncate |
