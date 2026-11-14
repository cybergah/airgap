# Ölçüm: guclendirme-b

2026-11-12 13:29 · model `gpt-oss:20b` · 3 tekrar · harita 1000

**Başarı: 24/33 (%73)**, %95 güven aralığı %56–%85

Ortanca süre 39.4 sn, toplam 1472 sn, zaman aşımı 0. Tamamlanan tur 24/33. Başarısız olup bunu söylemeyen 1. Gereksiz dosya değiştiren 4.

| Tür | Başarı |
|---|---|
| gercek_hata | 20/24 |
| gercek_ozellik | 4/9 |

## Karşılaştırma: guclendirme-oncesi

Önceki: 25/33
Kötüleşen: ct_ttl_sinir, ct_yeni_ozellik, mi_partition
İyileşen: ck_secenek_sirasi, mi_maxsplit

Güven aralıkları çakışıyorsa fark rastlantı olabilir.

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| ct_lru_okuma | gercek_hata | ✅ | 27.5 | 17 | gereksiz dosya: cachetools/__init__.py |
| ct_ttl_sinir | gercek_hata | ✅ | 49.2 | 19 | gereksiz dosya: cachetools/__init__.py |
| ct_kapasite | gercek_hata | ✅ | 40.7 | 18 | gereksiz dosya: cachetools.py, cachetools/__init__.py, tests/__init__.py |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 44.8 | 19 |  |
| mi_maxsplit | gercek_hata | ✅ | 159.0 | 29 | adım sınırı |
| mi_partition | gercek_hata | ✅ | 42.4 | 13 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 66.7 | 30 | adım sınırı; ImportError: cannot import name 'every_nth' from 'more_itertools' (/work/more_itertools/__ |
| ck_aralik | gercek_hata | ❌ | 25.5 | 8 | ajan durdurdu: tekrar; FAILED (errors=1) |
| ck_secim | gercek_hata | ✅ | 36.1 | 16 |  |
| ck_secenek_sirasi | gercek_hata | ✅ | 45.0 | 22 |  |
| ck_yeni_ozellik | gercek_ozellik | ✅ | 53.1 | 15 | gereksiz dosya: src/click/_truncate.py |
| ct_lru_okuma | gercek_hata | ✅ | 24.2 | 10 |  |
| ct_ttl_sinir | gercek_hata | ❌ | 36.1 | 30 | adım sınırı; AssertionError: 'a' unexpectedly found in TTLCache({}, maxsize=5, currsize=0) |
| ct_kapasite | gercek_hata | ✅ | 43.0 | 19 |  |
| ct_yeni_ozellik | gercek_ozellik | ❌ | 29.2 | 19 | başarısızlığı söylemedi; TypeError: unsupported operand type(s) for /: 'NoneType' and 'int' |
| mi_maxsplit | gercek_hata | ✅ | 95.1 | 10 |  |
| mi_partition | gercek_hata | ✅ | 39.1 | 12 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 31.8 | 27 | adım sınırı; ImportError: cannot import name 'every_nth' from 'more_itertools' (/work/more_itertools/__ |
| ck_aralik | gercek_hata | ✅ | 39.4 | 18 |  |
| ck_secim | gercek_hata | ✅ | 38.2 | 14 |  |
| ck_secenek_sirasi | gercek_hata | ✅ | 23.2 | 17 |  |
| ck_yeni_ozellik | gercek_ozellik | ✅ | 49.8 | 14 |  |
| ct_lru_okuma | gercek_hata | ✅ | 28.9 | 19 |  |
| ct_ttl_sinir | gercek_hata | ❌ | 25.7 | 20 | ajan durdurdu: tekrar; AssertionError: 'a' unexpectedly found in TTLCache({}, maxsize=5, currsize=0) |
| ct_kapasite | gercek_hata | ✅ | 50.5 | 18 |  |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 41.0 | 19 |  |
| mi_maxsplit | gercek_hata | ✅ | 110.6 | 11 |  |
| mi_partition | gercek_hata | ❌ | 23.4 | 13 | model hatası veya boş yanıt; AssertionError: Tuples differ: ([1, 'x'], [0, '']) != ([0, ''], [1, 'x']) |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 29.6 | 29 | adım sınırı; ImportError: cannot import name 'every_nth' from 'more_itertools' (/work/more_itertools/__ |
| ck_aralik | gercek_hata | ✅ | 56.6 | 18 |  |
| ck_secim | gercek_hata | ✅ | 40.2 | 13 |  |
| ck_secenek_sirasi | gercek_hata | ✅ | 20.9 | 14 |  |
| ck_yeni_ozellik | gercek_ozellik | ❌ | 5.8 | 2 | ajan durdurdu: tekrar; AttributeError: truncate |
