# Ölçüm: guclendirme-sonrasi

2026-11-12 12:42 · model `gpt-oss:20b` · 3 tekrar · harita 1000

**Başarı: 22/33 (%67)**, %95 güven aralığı %50–%80

Ortanca süre 42.7 sn, toplam 1798 sn, zaman aşımı 0. Tamamlanan tur 23/33. Başarısız olup bunu söylemeyen 3. Gereksiz dosya değiştiren 4.

| Tür | Başarı |
|---|---|
| gercek_hata | 17/24 |
| gercek_ozellik | 5/9 |

## Karşılaştırma: guclendirme-oncesi

Önceki: 25/33
Kötüleşen: ck_aralik, ct_ttl_sinir, mi_maxsplit
İyileşen: ck_secenek_sirasi

Güven aralıkları çakışıyorsa fark rastlantı olabilir.

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| ct_lru_okuma | gercek_hata | ✅ | 42.3 | 17 |  |
| ct_ttl_sinir | gercek_hata | ❌ | 32.8 | 28 | adım sınırı; AssertionError: 'a' unexpectedly found in TTLCache({}, maxsize=5, currsize=0) |
| ct_kapasite | gercek_hata | ✅ | 38.7 | 19 |  |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 55.0 | 27 | gereksiz dosya: cachetools/__init__.py, src/__init__.py |
| mi_maxsplit | gercek_hata | ❌ | 151.7 | 27 | adım sınırı; AssertionError: Lists differ: [['a'], ['b', 'c', 'd', 'c', 'b', 'a']] != [['a'], ['c', 'd' |
| mi_partition | gercek_hata | ✅ | 79.6 | 12 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 26.3 | 27 | adım sınırı; ImportError: cannot import name 'every_nth' from 'more_itertools' (/work/more_itertools/__ |
| ck_aralik | gercek_hata | ❌ | 64.2 | 21 | başarısızlığı söylemedi; FAILED (errors=1) |
| ck_secim | gercek_hata | ✅ | 38.3 | 19 |  |
| ck_secenek_sirasi | gercek_hata | ✅ | 43.5 | 19 |  |
| ck_yeni_ozellik | gercek_ozellik | ✅ | 35.8 | 13 |  |
| ct_lru_okuma | gercek_hata | ✅ | 34.8 | 18 | gereksiz dosya: cachetools/__init__.py |
| ct_ttl_sinir | gercek_hata | ✅ | 27.4 | 14 |  |
| ct_kapasite | gercek_hata | ✅ | 43.8 | 18 |  |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 98.6 | 28 | gereksiz dosya: cachetools/__init__.py; adım sınırı |
| mi_maxsplit | gercek_hata | ❌ | 43.2 | 29 | ajan durdurdu: tekrar; FAILED (failures=1) |
| mi_partition | gercek_hata | ✅ | 77.0 | 23 | adım sınırı |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 52.2 | 30 | adım sınırı; AttributeError: module 'more_itertools.more' has no attribute 'every_nth' |
| ck_aralik | gercek_hata | ❌ | 41.2 | 16 | başarısızlığı söylemedi; FAILED (errors=1) |
| ck_secim | gercek_hata | ✅ | 44.7 | 19 |  |
| ck_secenek_sirasi | gercek_hata | ✅ | 24.9 | 19 |  |
| ck_yeni_ozellik | gercek_ozellik | ✅ | 22.2 | 11 |  |
| ct_lru_okuma | gercek_hata | ✅ | 46.5 | 18 | gereksiz dosya: cachetools/__init__.py |
| ct_ttl_sinir | gercek_hata | ✅ | 24.5 | 10 |  |
| ct_kapasite | gercek_hata | ✅ | 34.0 | 19 |  |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 37.8 | 17 |  |
| mi_maxsplit | gercek_hata | ✅ | 144.8 | 17 |  |
| mi_partition | gercek_hata | ✅ | 129.8 | 17 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 52.7 | 29 | adım sınırı; AttributeError: module 'more_itertools.more' has no attribute 'every_nth' |
| ck_aralik | gercek_hata | ❌ | 33.6 | 17 | başarısızlığı söylemedi; FAILED (errors=1) |
| ck_secim | gercek_hata | ✅ | 41.8 | 14 |  |
| ck_secenek_sirasi | gercek_hata | ❌ | 42.7 | 30 | adım sınırı; AssertionError: '-v, --verbose' not found in 'Usage: k [OPTIONS]\n\nOptions:\n  --verbose, |
| ck_yeni_ozellik | gercek_ozellik | ❌ | 91.9 | 26 | adım sınırı; AttributeError: truncate |
