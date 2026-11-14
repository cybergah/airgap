# Ölçüm: iddia

2026-11-12 16:12 · model `gpt-oss:20b` · 3 tekrar · harita 1000

**Başarı: 20/33 (%61)**, %95 güven aralığı %44–%75

Ortanca süre 43.3 sn, toplam 1615 sn, zaman aşımı 0. Tamamlanan tur 22/33. Başarısız olup bunu söylemeyen 4. Gereksiz dosya değiştiren 6.

| Tür | Başarı |
|---|---|
| gercek_hata | 16/24 |
| gercek_ozellik | 4/9 |

## Karşılaştırma: guclendirme-oncesi

Önceki: 25/33
Kötüleşen: ck_aralik, ck_yeni_ozellik, ct_ttl_sinir
İyileşen: yok

Güven aralıkları çakışıyorsa fark rastlantı olabilir.

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| ct_lru_okuma | gercek_hata | ✅ | 32.2 | 19 |  |
| ct_ttl_sinir | gercek_hata | ❌ | 26.0 | 27 | adım sınırı; AssertionError: 'a' unexpectedly found in TTLCache({}, maxsize=5, currsize=0) |
| ct_kapasite | gercek_hata | ✅ | 92.8 | 26 | gereksiz dosya: cachetools/__init__.py; adım sınırı |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 25.0 | 13 |  |
| mi_maxsplit | gercek_hata | ✅ | 109.6 | 25 |  |
| mi_partition | gercek_hata | ✅ | 32.3 | 11 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 45.6 | 28 | adım sınırı; AttributeError: module 'more_itertools.more' has no attribute 'every_nth' |
| ck_aralik | gercek_hata | ❌ | 83.4 | 21 | adım sınırı; FAILED (errors=1) |
| ck_secim | gercek_hata | ✅ | 43.3 | 19 |  |
| ck_secenek_sirasi | gercek_hata | ❌ | 62.2 | 30 | adım sınırı; AssertionError: '-v, --verbose' not found in 'Usage: k [OPTIONS]\n\nOptions:\n  --verbose, |
| ck_yeni_ozellik | gercek_ozellik | ✅ | 48.4 | 17 |  |
| ct_lru_okuma | gercek_hata | ✅ | 71.8 | 28 | gereksiz dosya: cachetools/__init__.py, tests/__init__.py; adım sınırı |
| ct_ttl_sinir | gercek_hata | ✅ | 30.0 | 16 | gereksiz dosya: cachetools/__init__.py |
| ct_kapasite | gercek_hata | ✅ | 25.2 | 9 |  |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 43.6 | 18 | gereksiz dosya: cachetools/__init__.py |
| mi_maxsplit | gercek_hata | ✅ | 41.3 | 9 |  |
| mi_partition | gercek_hata | ✅ | 31.1 | 10 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 40.2 | 30 | adım sınırı; AttributeError: module 'more_itertools.more' has no attribute 'every_nth' |
| ck_aralik | gercek_hata | ❌ | 38.4 | 19 | başarısızlığı söylemedi; FAILED (errors=1) |
| ck_secim | gercek_hata | ✅ | 36.5 | 13 |  |
| ck_secenek_sirasi | gercek_hata | ✅ | 43.7 | 25 |  |
| ck_yeni_ozellik | gercek_ozellik | ❌ | 35.9 | 18 | başarısızlığı söylemedi; AttributeError: truncate |
| ct_lru_okuma | gercek_hata | ✅ | 46.4 | 18 | gereksiz dosya: cachetools/__init__.py |
| ct_ttl_sinir | gercek_hata | ❌ | 44.6 | 30 | adım sınırı; AssertionError: 'a' unexpectedly found in TTLCache({}, maxsize=5, currsize=0) |
| ct_kapasite | gercek_hata | ✅ | 13.9 | 8 |  |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 57.9 | 24 | gereksiz dosya: cachetools/__init__.py |
| mi_maxsplit | gercek_hata | ❌ | 112.7 | 23 | adım sınırı; FAILED (failures=1) |
| mi_partition | gercek_hata | ✅ | 39.3 | 11 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 62.2 | 28 | adım sınırı; ImportError: cannot import name 'Any' from 'collections.abc' (/usr/local/lib/python3.13/_c |
| ck_aralik | gercek_hata | ❌ | 58.3 | 22 | başarısızlığı söylemedi; FAILED (errors=1) |
| ck_secim | gercek_hata | ✅ | 38.0 | 19 |  |
| ck_secenek_sirasi | gercek_hata | ❌ | 24.7 | 29 | adım sınırı; AssertionError: '-v, --verbose' not found in 'Usage: k [OPTIONS]\n\nOptions:\n  --verbose, |
| ck_yeni_ozellik | gercek_ozellik | ❌ | 78.2 | 20 | başarısızlığı söylemedi; AttributeError: truncate |
