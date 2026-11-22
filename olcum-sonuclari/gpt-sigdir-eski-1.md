# Ölçüm: gpt-sigdir-eski-1

2026-11-22 21:07 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 7/11 (%64)**, %95 güven aralığı %35–%85

Ortanca süre 48.1 sn, toplam 702 sn, zaman aşımı 0. Tamamlanan tur 8/11. Başarısız olup bunu söylemeyen 1. Gereksiz dosya değiştiren 0.

| Tür | Başarı |
|---|---|
| gercek_hata | 6/8 |
| gercek_ozellik | 1/3 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| ct_lru_okuma | gercek_hata | ✅ | 60.2 | 19 |  |
| ct_ttl_sinir | gercek_hata | ✅ | 30.0 | 11 |  |
| ct_kapasite | gercek_hata | ✅ | 37.7 | 16 |  |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 80.4 | 24 |  |
| mi_maxsplit | gercek_hata | ✅ | 114.0 | 10 |  |
| mi_partition | gercek_hata | ✅ | 42.5 | 8 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 66.0 | 29 | tur tamamlanmadı; ImportError: cannot import name 'every_nth' from 'more_itertools' (/work/more_itertools/__ |
| ck_aralik | gercek_hata | ❌ | 48.1 | 19 | başarısızlığı söylemedi; FAILED (errors=1) |
| ck_secim | gercek_hata | ✅ | 42.7 | 18 |  |
| ck_secenek_sirasi | gercek_hata | ❌ | 34.6 | 28 | tur tamamlanmadı; AssertionError: '-v, --verbose' not found in 'Usage: k [OPTIONS]\n\nOptions:\n  --verbose, |
| ck_yeni_ozellik | gercek_ozellik | ❌ | 146.1 | 22 | model hatası veya boş yanıt; AttributeError: truncate |
