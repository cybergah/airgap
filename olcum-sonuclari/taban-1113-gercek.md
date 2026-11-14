# Ölçüm: taban-1113-gercek

2026-11-13 08:24 · model `gpt-oss:20b` · 3 tekrar · harita 1000

**Başarı: 24/33 (%73)**, %95 güven aralığı %56–%85

Ortanca süre 28.2 sn, toplam 1235 sn, zaman aşımı 0. Tamamlanan tur 26/33. Başarısız olup bunu söylemeyen 3. Gereksiz dosya değiştiren 4.

| Tür | Başarı |
|---|---|
| gercek_hata | 20/24 |
| gercek_ozellik | 4/9 |

## Karşılaştırma: dusunme-orta-gercek

Önceki: 25/33
Kötüleşen: ck_secenek_sirasi, ck_yeni_ozellik
İyileşen: ct_lru_okuma

Güven aralıkları çakışıyorsa fark rastlantı olabilir.

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| ct_lru_okuma | gercek_hata | ✅ | 32.1 | 19 | gereksiz dosya: cachetools/__init__.py |
| ct_ttl_sinir | gercek_hata | ✅ | 18.3 | 12 |  |
| ct_kapasite | gercek_hata | ✅ | 20.4 | 10 |  |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 26.5 | 17 |  |
| mi_maxsplit | gercek_hata | ✅ | 33.8 | 9 |  |
| mi_partition | gercek_hata | ✅ | 29.9 | 9 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 162.3 | 26 | başarısızlığı söylemedi; gereksiz dosya: more_itertools/every_nth.py; FAILED (failures=1) |
| ck_aralik | gercek_hata | ✅ | 24.8 | 16 |  |
| ck_secim | gercek_hata | ✅ | 41.6 | 14 |  |
| ck_secenek_sirasi | gercek_hata | ❌ | 20.9 | 18 | başarısızlığı söylemedi; AssertionError: '-v, --verbose' not found in 'Usage: k [OPTIONS]\n\nOptions:\n  --verbose, |
| ck_yeni_ozellik | gercek_ozellik | ❌ | 55.6 | 30 | adım sınırı; AttributeError: truncate |
| ct_lru_okuma | gercek_hata | ✅ | 42.7 | 28 |  |
| ct_ttl_sinir | gercek_hata | ✅ | 28.2 | 14 |  |
| ct_kapasite | gercek_hata | ✅ | 33.4 | 17 |  |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 36.0 | 19 |  |
| mi_maxsplit | gercek_hata | ✅ | 32.0 | 9 |  |
| mi_partition | gercek_hata | ✅ | 21.5 | 10 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 11.5 | 12 | model hatası veya boş yanıt; ImportError: cannot import name 'every_nth' from 'more_itertools' (/work/more_itertools/__ |
| ck_aralik | gercek_hata | ❌ | 16.6 | 9 | başarısızlığı söylemedi; FAILED (errors=1) |
| ck_secim | gercek_hata | ✅ | 25.7 | 19 |  |
| ck_secenek_sirasi | gercek_hata | ❌ | 37.5 | 29 | gereksiz dosya: src/click/core.py; adım sınırı; AssertionError: '-v, --verbose' not found in 'Usage: k [OPTIONS]\n\nOptions:\n  --verbose, |
| ck_yeni_ozellik | gercek_ozellik | ❌ | 4.4 | 2 | ajan durdurdu: tekrar; AttributeError: truncate |
| ct_lru_okuma | gercek_hata | ✅ | 29.1 | 18 |  |
| ct_ttl_sinir | gercek_hata | ✅ | 25.2 | 14 |  |
| ct_kapasite | gercek_hata | ✅ | 86.6 | 29 | gereksiz dosya: cachetools/__init__.py, cachetools/keys.py; adım sınırı |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 30.0 | 19 |  |
| mi_maxsplit | gercek_hata | ✅ | 129.2 | 11 |  |
| mi_partition | gercek_hata | ✅ | 27.4 | 8 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 21.2 | 25 | adım sınırı; ImportError: cannot import name 'every_nth' from 'more_itertools' (/work/more_itertools/__ |
| ck_aralik | gercek_hata | ✅ | 24.1 | 18 |  |
| ck_secim | gercek_hata | ✅ | 12.7 | 8 |  |
| ck_secenek_sirasi | gercek_hata | ❌ | 18.1 | 29 | adım sınırı; AssertionError: '-v, --verbose' not found in 'Usage: k [OPTIONS]\n\nOptions:\n  --verbose, |
| ck_yeni_ozellik | gercek_ozellik | ✅ | 76.0 | 21 |  |
