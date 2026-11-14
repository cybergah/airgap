# Ölçüm: tekrar-tek

2026-11-12 14:52 · model `gpt-oss:20b` · 3 tekrar · harita 1000

**Başarı: 25/33 (%76)**, %95 güven aralığı %59–%87

Ortanca süre 44.1 sn, toplam 1969 sn, zaman aşımı 0. Tamamlanan tur 23/33. Başarısız olup bunu söylemeyen 2. Gereksiz dosya değiştiren 6.

| Tür | Başarı |
|---|---|
| gercek_hata | 20/24 |
| gercek_ozellik | 5/9 |

## Karşılaştırma: guclendirme-oncesi

Önceki: 25/33
Kötüleşen: ck_aralik
İyileşen: ck_secenek_sirasi

Güven aralıkları çakışıyorsa fark rastlantı olabilir.

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| ct_lru_okuma | gercek_hata | ✅ | 22.7 | 11 |  |
| ct_ttl_sinir | gercek_hata | ✅ | 45.2 | 19 | gereksiz dosya: cachetools/__init__.py |
| ct_kapasite | gercek_hata | ✅ | 30.4 | 16 |  |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 68.3 | 29 | gereksiz dosya: cachetools/__init__.py; adım sınırı |
| mi_maxsplit | gercek_hata | ✅ | 78.7 | 19 |  |
| mi_partition | gercek_hata | ✅ | 51.9 | 15 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 54.9 | 28 | adım sınırı; ImportError: cannot import name 'every_nth' from 'more_itertools' (/work/more_itertools/__ |
| ck_aralik | gercek_hata | ✅ | 52.1 | 17 |  |
| ck_secim | gercek_hata | ✅ | 41.2 | 19 |  |
| ck_secenek_sirasi | gercek_hata | ❌ | 35.7 | 30 | adım sınırı; AssertionError: '-v, --verbose' not found in 'Usage: k [OPTIONS]\n\nOptions:\n  --verbose, |
| ck_yeni_ozellik | gercek_ozellik | ✅ | 37.2 | 19 |  |
| ct_lru_okuma | gercek_hata | ✅ | 32.8 | 19 |  |
| ct_ttl_sinir | gercek_hata | ✅ | 22.3 | 14 |  |
| ct_kapasite | gercek_hata | ✅ | 73.7 | 24 | gereksiz dosya: cachetools/__init__.py, src/__init__.py |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 37.3 | 19 |  |
| mi_maxsplit | gercek_hata | ❌ | 292.3 | 26 | adım sınırı; AssertionError: Lists differ: [['a'], ['b', 'c', 'd', 'c', 'b', 'a']] != [['a'], ['c', 'd' |
| mi_partition | gercek_hata | ✅ | 87.8 | 12 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 44.1 | 27 | adım sınırı; FAILED (failures=1) |
| ck_aralik | gercek_hata | ❌ | 32.5 | 13 | başarısızlığı söylemedi; FAILED (errors=1) |
| ck_secim | gercek_hata | ✅ | 32.4 | 9 |  |
| ck_secenek_sirasi | gercek_hata | ✅ | 38.3 | 29 | adım sınırı |
| ck_yeni_ozellik | gercek_ozellik | ✅ | 54.4 | 9 |  |
| ct_lru_okuma | gercek_hata | ✅ | 38.9 | 19 | gereksiz dosya: cachetools/__init__.py |
| ct_ttl_sinir | gercek_hata | ✅ | 37.3 | 19 | gereksiz dosya: src/__init__.py |
| ct_kapasite | gercek_hata | ✅ | 77.6 | 29 | gereksiz dosya: cachetools/__init__.py; adım sınırı |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 30.2 | 15 |  |
| mi_maxsplit | gercek_hata | ✅ | 58.1 | 12 |  |
| mi_partition | gercek_hata | ✅ | 63.1 | 13 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 106.6 | 29 | adım sınırı; ImportError: cannot import name 'every_nth' from 'more_itertools' (/work/more_itertools/__ |
| ck_aralik | gercek_hata | ❌ | 55.4 | 19 | başarısızlığı söylemedi; FAILED (errors=1) |
| ck_secim | gercek_hata | ✅ | 25.3 | 30 | adım sınırı |
| ck_secenek_sirasi | gercek_hata | ✅ | 24.1 | 19 |  |
| ck_yeni_ozellik | gercek_ozellik | ❌ | 186.1 | 24 | adım sınırı; ImportError: cannot import name 'echo' from 'click.utils' (/work/src/click/utils.py) |
