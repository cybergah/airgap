# Ölçüm: gercek-taban

2026-11-09 15:46 · model `gpt-oss:20b` · 2 tekrar · harita 1000

**Başarı: 15/22 (%68)**, %95 güven aralığı %47–%84

Ortanca süre 39.4 sn, toplam 1059 sn, zaman aşımı 0. Tamamlanan tur 15/22. Başarısızken başardığını söyleyen 0.

| Tür | Başarı |
|---|---|
| gercek_hata | 12/16 |
| gercek_ozellik | 3/6 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| ct_lru_okuma | gercek_hata | ✅ | 39.4 | 23 |  |
| ct_ttl_sinir | gercek_hata | ✅ | 37.3 | 25 |  |
| ct_kapasite | gercek_hata | ❌ | 43.1 | 29 | adım sınırı; AssertionError: 1 != 2 |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 79.4 | 29 | adım sınırı |
| mi_maxsplit | gercek_hata | ✅ | 34.5 | 10 |  |
| mi_partition | gercek_hata | ✅ | 37.0 | 12 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 37.9 | 29 | adım sınırı; ImportError: cannot import name 'every_nth' from 'more_itertools' (/work/more_itertools/__ |
| ck_aralik | gercek_hata | ✅ | 62.9 | 25 | model hatası veya boş yanıt |
| ck_secim | gercek_hata | ✅ | 60.6 | 28 |  |
| ck_secenek_sirasi | gercek_hata | ❌ | 9.3 | 10 | AssertionError: '-v, --verbose' not found in 'Usage: k [OPTIONS]\n\nOptions:\n  --verbose, |
| ck_yeni_ozellik | gercek_ozellik | ❌ | 36.2 | 22 | ajan durdurdu: tekrar; AttributeError: truncate |
| ct_lru_okuma | gercek_hata | ✅ | 163.8 | 27 | adım sınırı |
| ct_ttl_sinir | gercek_hata | ✅ | 29.4 | 16 |  |
| ct_kapasite | gercek_hata | ✅ | 28.5 | 13 |  |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 31.0 | 14 |  |
| mi_maxsplit | gercek_hata | ✅ | 36.0 | 9 |  |
| mi_partition | gercek_hata | ✅ | 81.0 | 11 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 48.0 | 28 | adım sınırı; AttributeError: module 'more_itertools.more' has no attribute 'every_nth' |
| ck_aralik | gercek_hata | ❌ | 55.0 | 21 | FAILED (errors=1) |
| ck_secim | gercek_hata | ✅ | 41.0 | 16 |  |
| ck_secenek_sirasi | gercek_hata | ❌ | 23.3 | 22 | AssertionError: '-v, --verbose' not found in 'Usage: k [OPTIONS]\n\nOptions:\n  --verbose, |
| ck_yeni_ozellik | gercek_ozellik | ✅ | 44.3 | 21 |  |
