# Ölçüm: adim2-gercek

2026-11-13 05:51 · model `gpt-oss:20b` · 3 tekrar · harita 1000

**Başarı: 25/33 (%76)**, %95 güven aralığı %59–%87

Ortanca süre 36.8 sn, toplam 1286 sn, zaman aşımı 0. Tamamlanan tur 25/33. Başarısız olup bunu söylemeyen 2. Gereksiz dosya değiştiren 7.

| Tür | Başarı |
|---|---|
| gercek_hata | 20/24 |
| gercek_ozellik | 5/9 |

## Karşılaştırma: dusunme-orta-gercek

Önceki: 25/33
Kötüleşen: ck_secim, ct_kapasite, mi_maxsplit
İyileşen: ck_aralik, ck_secenek_sirasi, ct_lru_okuma

Güven aralıkları çakışıyorsa fark rastlantı olabilir.

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| ct_lru_okuma | gercek_hata | ✅ | 47.9 | 19 | gereksiz dosya: cachetools/__init__.py |
| ct_ttl_sinir | gercek_hata | ✅ | 22.0 | 8 |  |
| ct_kapasite | gercek_hata | ✅ | 45.7 | 15 | gereksiz dosya: cachetools/__init__.py |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 22.6 | 13 |  |
| mi_maxsplit | gercek_hata | ✅ | 22.8 | 7 |  |
| mi_partition | gercek_hata | ✅ | 25.0 | 8 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 38.7 | 24 | adım sınırı; AttributeError: module 'more_itertools.more' has no attribute 'every_nth' |
| ck_aralik | gercek_hata | ✅ | 31.1 | 18 |  |
| ck_secim | gercek_hata | ❌ | 34.5 | 29 | adım sınırı; FAILED (errors=1) |
| ck_secenek_sirasi | gercek_hata | ✅ | 27.2 | 30 | adım sınırı |
| ck_yeni_ozellik | gercek_ozellik | ✅ | 30.9 | 14 |  |
| ct_lru_okuma | gercek_hata | ✅ | 57.2 | 29 | gereksiz dosya: cachetools/__init__.py, src/__init__.py; adım sınırı |
| ct_ttl_sinir | gercek_hata | ✅ | 27.8 | 16 |  |
| ct_kapasite | gercek_hata | ❌ | 12.1 | 4 | model hatası veya boş yanıt; AssertionError: 1 != 2 |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 39.0 | 15 |  |
| mi_maxsplit | gercek_hata | ❌ | 72.2 | 12 | başarısızlığı söylemedi; FAILED (failures=1) |
| mi_partition | gercek_hata | ✅ | 31.1 | 12 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 49.7 | 16 | başarısızlığı söylemedi; gereksiz dosya: more_itertools/recipes.py; ImportError: cannot import name 'every_nth' from 'more_itertools' (/work/more_itertools/__ |
| ck_aralik | gercek_hata | ✅ | 38.2 | 18 |  |
| ck_secim | gercek_hata | ✅ | 32.9 | 12 |  |
| ck_secenek_sirasi | gercek_hata | ❌ | 41.9 | 30 | adım sınırı; AssertionError: '-v, --verbose' not found in 'Usage: k [OPTIONS]\n\nOptions:\n  --verbose, |
| ck_yeni_ozellik | gercek_ozellik | ❌ | 72.2 | 22 | gereksiz dosya: src/click/truncate.py; adım sınırı; AttributeError: truncate |
| ct_lru_okuma | gercek_hata | ✅ | 36.8 | 19 |  |
| ct_ttl_sinir | gercek_hata | ✅ | 22.1 | 11 |  |
| ct_kapasite | gercek_hata | ✅ | 51.8 | 19 | gereksiz dosya: cachetools/__init__.py |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 32.1 | 18 |  |
| mi_maxsplit | gercek_hata | ✅ | 57.2 | 11 |  |
| mi_partition | gercek_hata | ✅ | 32.5 | 13 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 45.6 | 22 | model hatası veya boş yanıt; ImportError: cannot import name 'every_nth' from 'more_itertools' (/work/more_itertools/__ |
| ck_aralik | gercek_hata | ✅ | 39.1 | 19 |  |
| ck_secim | gercek_hata | ✅ | 33.2 | 12 |  |
| ck_secenek_sirasi | gercek_hata | ✅ | 56.3 | 30 |  |
| ck_yeni_ozellik | gercek_ozellik | ✅ | 56.9 | 19 | gereksiz dosya: click/__init__.py |
