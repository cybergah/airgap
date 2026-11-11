# Ölçüm: baglam-olcum

2026-11-11 16:52 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 1/3 (%33)**, %95 güven aralığı %6–%79

Ortanca süre 26.1 sn, toplam 91 sn, zaman aşımı 0. Tamamlanan tur 1/3. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 0.

| Tür | Başarı |
|---|---|
| gercek_hata | 1/2 |
| gercek_ozellik | 0/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| mi_maxsplit | gercek_hata | ✅ | 26.1 | 7 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 43.4 | 27 | adım sınırı; AttributeError: module 'more_itertools.more' has no attribute 'every_nth' |
| ck_secenek_sirasi | gercek_hata | ❌ | 21.6 | 30 | adım sınırı; AssertionError: '-v, --verbose' not found in 'Usage: k [OPTIONS]\n\nOptions:\n  --verbose, |
