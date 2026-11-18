# Ölçüm: statik1-gercek-5

2026-11-14 21:27 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 2/3 (%67)**, %95 güven aralığı %21–%94

Ortanca süre 35.4 sn, toplam 166 sn, zaman aşımı 0. Tamamlanan tur 2/3. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 1.

| Tür | Başarı |
|---|---|
| gercek_hata | 1/2 |
| gercek_ozellik | 1/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| ck_aralik | gercek_hata | ✅ | 101.6 | 26 |  |
| ck_secenek_sirasi | gercek_hata | ❌ | 29.4 | 30 | adım sınırı; AssertionError: '-v, --verbose' not found in 'Usage: k [OPTIONS]\n\nOptions:\n  --verbose, |
| ck_yeni_ozellik | gercek_ozellik | ✅ | 35.4 | 19 | gereksiz dosya: src/click/_textwrap.py |
