# Ölçüm: adim4-gercek

2026-11-13 07:39 · model `gpt-oss:20b` · 3 tekrar · harita 1000

**Başarı: 26/33 (%79)**, %95 güven aralığı %62–%89

Ortanca süre 35.9 sn, toplam 1274 sn, zaman aşımı 0. Tamamlanan tur 25/33. Başarısız olup bunu söylemeyen 2. Gereksiz dosya değiştiren 4.

| Tür | Başarı |
|---|---|
| gercek_hata | 20/24 |
| gercek_ozellik | 6/9 |

## Karşılaştırma: dusunme-orta-gercek

Önceki: 25/33
Kötüleşen: ck_aralik
İyileşen: ck_secenek_sirasi, ck_yeni_ozellik, ct_lru_okuma

Güven aralıkları çakışıyorsa fark rastlantı olabilir.

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| ct_lru_okuma | gercek_hata | ✅ | 44.2 | 30 | adım sınırı |
| ct_ttl_sinir | gercek_hata | ✅ | 35.9 | 19 |  |
| ct_kapasite | gercek_hata | ✅ | 37.7 | 22 |  |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 29.6 | 12 | ajan durdurdu: tekrar |
| mi_maxsplit | gercek_hata | ✅ | 92.4 | 13 |  |
| mi_partition | gercek_hata | ✅ | 34.2 | 12 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 33.4 | 30 | adım sınırı; ImportError: cannot import name 'every_nth' from 'more_itertools' (/work/more_itertools/__ |
| ck_aralik | gercek_hata | ❌ | 47.4 | 18 | başarısızlığı söylemedi; FAILED (errors=1) |
| ck_secim | gercek_hata | ✅ | 35.9 | 14 |  |
| ck_secenek_sirasi | gercek_hata | ✅ | 46.0 | 27 |  |
| ck_yeni_ozellik | gercek_ozellik | ✅ | 36.7 | 19 |  |
| ct_lru_okuma | gercek_hata | ✅ | 32.4 | 19 |  |
| ct_ttl_sinir | gercek_hata | ✅ | 25.2 | 19 | gereksiz dosya: cachetools/__init__.py |
| ct_kapasite | gercek_hata | ✅ | 40.1 | 19 | gereksiz dosya: cachetools/__init__.py |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 23.2 | 15 |  |
| mi_maxsplit | gercek_hata | ✅ | 56.6 | 8 |  |
| mi_partition | gercek_hata | ✅ | 25.1 | 8 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 25.4 | 30 | adım sınırı; ImportError: cannot import name 'every_nth' from 'more_itertools' (/work/more_itertools/__ |
| ck_aralik | gercek_hata | ❌ | 41.3 | 18 | ajan durdurdu: tekrar; FAILED (errors=1) |
| ck_secim | gercek_hata | ✅ | 29.8 | 14 |  |
| ck_secenek_sirasi | gercek_hata | ❌ | 38.7 | 30 | adım sınırı; AssertionError: '-v, --verbose' not found in 'Usage: k [OPTIONS]\n\nOptions:\n  --verbose, |
| ck_yeni_ozellik | gercek_ozellik | ✅ | 31.1 | 14 |  |
| ct_lru_okuma | gercek_hata | ✅ | 27.9 | 18 |  |
| ct_ttl_sinir | gercek_hata | ✅ | 16.4 | 12 |  |
| ct_kapasite | gercek_hata | ✅ | 33.1 | 19 | gereksiz dosya: cachetools/__init__.py |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 18.7 | 9 |  |
| mi_maxsplit | gercek_hata | ✅ | 71.3 | 14 |  |
| mi_partition | gercek_hata | ✅ | 51.3 | 11 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 35.2 | 27 | adım sınırı; ImportError: cannot import name 'every_nth' from 'more_itertools' (/work/more_itertools/__ |
| ck_aralik | gercek_hata | ❌ | 52.9 | 13 | başarısızlığı söylemedi; FAILED (errors=1) |
| ck_secim | gercek_hata | ✅ | 18.2 | 14 |  |
| ck_secenek_sirasi | gercek_hata | ✅ | 48.8 | 30 | adım sınırı |
| ck_yeni_ozellik | gercek_ozellik | ✅ | 58.2 | 16 | gereksiz dosya: src/click/_textwrap.py |
