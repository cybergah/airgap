# Ölçüm: gercek-bitirme

2026-11-09 17:10 · model `gpt-oss:20b` · 3 tekrar · harita 1000

**Başarı: 24/33 (%73)**, %95 güven aralığı %56–%85

Ortanca süre 38.8 sn, toplam 1509 sn, zaman aşımı 0. Tamamlanan tur 25/33. Başarısız olup bunu söylemeyen 1. Gereksiz dosya değiştiren 3.

| Tür | Başarı |
|---|---|
| gercek_hata | 20/24 |
| gercek_ozellik | 4/9 |

## Karşılaştırma: gercek-taban

Önceki: 15/22
Kötüleşen: ck_yeni_ozellik
İyileşen: ck_aralik, ck_secenek_sirasi, ct_kapasite

Güven aralıkları çakışıyorsa fark rastlantı olabilir.

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| ct_lru_okuma | gercek_hata | ✅ | 38.8 | 15 |  |
| ct_ttl_sinir | gercek_hata | ✅ | 20.6 | 16 |  |
| ct_kapasite | gercek_hata | ✅ | 61.6 | 21 | gereksiz dosya: cachetools/__init__.py |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 25.9 | 13 |  |
| mi_maxsplit | gercek_hata | ✅ | 239.6 | 26 |  |
| mi_partition | gercek_hata | ✅ | 47.7 | 12 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 58.3 | 28 | gereksiz dosya: more_itertools/__init__.py, more_itertools/every_nth.py; adım sınırı; FAILED (failures=1) |
| ck_aralik | gercek_hata | ❌ | 71.9 | 27 | FAILED (errors=1) |
| ck_secim | gercek_hata | ✅ | 18.5 | 14 |  |
| ck_secenek_sirasi | gercek_hata | ❌ | 42.7 | 30 | adım sınırı; AssertionError: '-v, --verbose' not found in 'Usage: k [OPTIONS]\n\nOptions:\n  --verbose, |
| ck_yeni_ozellik | gercek_ozellik | ❌ | 58.7 | 28 | adım sınırı; AttributeError: truncate |
| ct_lru_okuma | gercek_hata | ✅ | 30.6 | 16 |  |
| ct_ttl_sinir | gercek_hata | ✅ | 45.3 | 19 |  |
| ct_kapasite | gercek_hata | ❌ | 18.9 | 10 | başarısızlığı söylemedi; AssertionError: 1 != 2 |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 26.6 | 11 |  |
| mi_maxsplit | gercek_hata | ✅ | 79.9 | 12 |  |
| mi_partition | gercek_hata | ✅ | 40.6 | 15 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 49.4 | 28 | adım sınırı; AttributeError: module 'more_itertools.more' has no attribute 'every_nth' |
| ck_aralik | gercek_hata | ✅ | 22.2 | 11 |  |
| ck_secim | gercek_hata | ✅ | 34.5 | 18 |  |
| ck_secenek_sirasi | gercek_hata | ✅ | 41.1 | 19 |  |
| ck_yeni_ozellik | gercek_ozellik | ❌ | 6.5 | 2 | ajan durdurdu: tekrar; AttributeError: truncate |
| ct_lru_okuma | gercek_hata | ✅ | 27.7 | 19 |  |
| ct_ttl_sinir | gercek_hata | ✅ | 14.6 | 11 |  |
| ct_kapasite | gercek_hata | ✅ | 33.2 | 14 |  |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 48.1 | 19 |  |
| mi_maxsplit | gercek_hata | ✅ | 82.6 | 14 |  |
| mi_partition | gercek_hata | ✅ | 28.0 | 9 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 37.8 | 30 | adım sınırı; FAILED (failures=1) |
| ck_aralik | gercek_hata | ✅ | 36.1 | 13 | model hatası veya boş yanıt |
| ck_secim | gercek_hata | ✅ | 24.2 | 19 |  |
| ck_secenek_sirasi | gercek_hata | ❌ | 46.8 | 29 | adım sınırı; AssertionError: '-v, --verbose' not found in 'Usage: k [OPTIONS]\n\nOptions:\n  --verbose, |
| ck_yeni_ozellik | gercek_ozellik | ✅ | 50.0 | 19 | gereksiz dosya: src/click/truncate.py |
