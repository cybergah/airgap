# Ölçüm: adim3-gercek

2026-11-13 06:55 · model `gpt-oss:20b` · 3 tekrar · harita 1000

**Başarı: 23/33 (%70)**, %95 güven aralığı %53–%83

Ortanca süre 37.3 sn, toplam 1559 sn, zaman aşımı 0. Tamamlanan tur 22/33. Başarısız olup bunu söylemeyen 2. Gereksiz dosya değiştiren 4.

| Tür | Başarı |
|---|---|
| gercek_hata | 17/24 |
| gercek_ozellik | 6/9 |

## Karşılaştırma: dusunme-orta-gercek

Önceki: 25/33
Kötüleşen: ck_aralik, ct_kapasite, ct_lru_okuma, ct_ttl_sinir
İyileşen: ck_secenek_sirasi, ck_yeni_ozellik

Güven aralıkları çakışıyorsa fark rastlantı olabilir.

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| ct_lru_okuma | gercek_hata | ❌ | 41.7 | 18 | başarısızlığı söylemedi; gereksiz dosya: cachetools/__init__.py; AssertionError: 'a' not found in LRUCache({'b': 2, 'c': 3}, maxsize=2, currsize=2) |
| ct_ttl_sinir | gercek_hata | ✅ | 44.7 | 23 | model hatası veya boş yanıt |
| ct_kapasite | gercek_hata | ✅ | 27.0 | 14 |  |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 46.6 | 19 |  |
| mi_maxsplit | gercek_hata | ✅ | 113.0 | 26 |  |
| mi_partition | gercek_hata | ✅ | 37.3 | 10 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 43.1 | 28 | adım sınırı; ImportError: cannot import name 'every_nth' from 'more_itertools' (/work/more_itertools/__ |
| ck_aralik | gercek_hata | ❌ | 62.0 | 25 | adım sınırı; FAILED (errors=1) |
| ck_secim | gercek_hata | ✅ | 28.6 | 19 |  |
| ck_secenek_sirasi | gercek_hata | ❌ | 35.5 | 30 | adım sınırı; AssertionError: '-v, --verbose' not found in 'Usage: k [OPTIONS]\n\nOptions:\n  --verbose, |
| ck_yeni_ozellik | gercek_ozellik | ✅ | 48.8 | 16 |  |
| ct_lru_okuma | gercek_hata | ❌ | 37.3 | 30 | adım sınırı; AssertionError: 'a' not found in LRUCache({'b': 2, 'c': 3}, maxsize=2, currsize=2) |
| ct_ttl_sinir | gercek_hata | ❌ | 38.3 | 30 | adım sınırı; AssertionError: 'a' unexpectedly found in TTLCache({}, maxsize=5, currsize=0) |
| ct_kapasite | gercek_hata | ✅ | 35.6 | 19 | gereksiz dosya: sitecustomize.py |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 20.6 | 11 |  |
| mi_maxsplit | gercek_hata | ✅ | 128.0 | 27 | adım sınırı |
| mi_partition | gercek_hata | ✅ | 41.7 | 12 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 25.0 | 30 | adım sınırı; ImportError: cannot import name 'every_nth' from 'more_itertools' (/work/more_itertools/__ |
| ck_aralik | gercek_hata | ❌ | 35.1 | 18 | başarısızlığı söylemedi; FAILED (errors=1) |
| ck_secim | gercek_hata | ✅ | 54.4 | 26 |  |
| ck_secenek_sirasi | gercek_hata | ✅ | 25.9 | 30 | adım sınırı |
| ck_yeni_ozellik | gercek_ozellik | ✅ | 27.7 | 16 |  |
| ct_lru_okuma | gercek_hata | ✅ | 36.2 | 19 | gereksiz dosya: tests/__init__.py |
| ct_ttl_sinir | gercek_hata | ✅ | 24.2 | 14 |  |
| ct_kapasite | gercek_hata | ❌ | 52.4 | 29 | gereksiz dosya: cachetools/__init__.py; adım sınırı; AssertionError: 1 != 2 |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 21.5 | 15 |  |
| mi_maxsplit | gercek_hata | ✅ | 154.6 | 24 |  |
| mi_partition | gercek_hata | ✅ | 114.9 | 11 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 40.3 | 29 | adım sınırı; AttributeError: module 'more_itertools.more' has no attribute 'chunked'. Did you mean: 'ic |
| ck_aralik | gercek_hata | ✅ | 36.0 | 26 |  |
| ck_secim | gercek_hata | ✅ | 24.2 | 16 |  |
| ck_secenek_sirasi | gercek_hata | ✅ | 28.4 | 30 |  |
| ck_yeni_ozellik | gercek_ozellik | ✅ | 28.7 | 16 |  |
