# Ölçüm: son-eski-gercek-1

2026-11-14 22:39 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 9/11 (%82)**, %95 güven aralığı %52–%95

Ortanca süre 37.5 sn, toplam 474 sn, zaman aşımı 0. Tamamlanan tur 9/11. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 2.

| Tür | Başarı |
|---|---|
| gercek_hata | 7/8 |
| gercek_ozellik | 2/3 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| ct_lru_okuma | gercek_hata | ✅ | 20.6 | 9 |  |
| ct_ttl_sinir | gercek_hata | ✅ | 41.1 | 23 | gereksiz dosya: cachetools/__init__.py |
| ct_kapasite | gercek_hata | ❌ | 39.6 | 15 | ajan durdurdu: tekrar; AssertionError: 1 != 2 |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 70.5 | 27 | gereksiz dosya: cachetools/__init__.py |
| mi_maxsplit | gercek_hata | ✅ | 96.8 | 17 |  |
| mi_partition | gercek_hata | ✅ | 77.0 | 18 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 28.9 | 28 | adım sınırı; ImportError: cannot import name 'every_nth' from 'more_itertools' (/work/more_itertools/__ |
| ck_aralik | gercek_hata | ✅ | 25.3 | 19 |  |
| ck_secim | gercek_hata | ✅ | 20.1 | 18 |  |
| ck_secenek_sirasi | gercek_hata | ✅ | 16.3 | 14 |  |
| ck_yeni_ozellik | gercek_ozellik | ✅ | 37.5 | 19 |  |
