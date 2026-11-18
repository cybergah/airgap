# Ölçüm: son-eski-gercek-3

2026-11-14 23:31 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 8/11 (%73)**, %95 güven aralığı %43–%90

Ortanca süre 24.5 sn, toplam 333 sn, zaman aşımı 0. Tamamlanan tur 6/11. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 0.

| Tür | Başarı |
|---|---|
| gercek_hata | 6/8 |
| gercek_ozellik | 2/3 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| ct_lru_okuma | gercek_hata | ✅ | 13.2 | 9 |  |
| ct_ttl_sinir | gercek_hata | ✅ | 22.5 | 17 |  |
| ct_kapasite | gercek_hata | ❌ | 14.1 | 11 | model hatası veya boş yanıt; AssertionError: 1 != 2 |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 24.5 | 13 |  |
| mi_maxsplit | gercek_hata | ✅ | 55.8 | 14 |  |
| mi_partition | gercek_hata | ✅ | 33.1 | 9 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 18.9 | 16 | ajan durdurdu: tekrar; ImportError: cannot import name 'every_nth' from 'more_itertools' (/work/more_itertools/__ |
| ck_aralik | gercek_hata | ✅ | 50.5 | 27 | adım sınırı |
| ck_secim | gercek_hata | ✅ | 26.3 | 15 |  |
| ck_secenek_sirasi | gercek_hata | ❌ | 23.4 | 29 | adım sınırı; AssertionError: '-v, --verbose' not found in 'Usage: k [OPTIONS]\n\nOptions:\n  --verbose, |
| ck_yeni_ozellik | gercek_ozellik | ✅ | 50.8 | 24 | adım sınırı |
