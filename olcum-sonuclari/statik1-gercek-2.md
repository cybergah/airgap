# Ölçüm: statik1-gercek-2

2026-11-14 21:10 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 1/3 (%33)**, %95 güven aralığı %6–%79

Ortanca süre 40.6 sn, toplam 107 sn, zaman aşımı 0. Tamamlanan tur 2/3. Başarısız olup bunu söylemeyen 1. Gereksiz dosya değiştiren 1.

| Tür | Başarı |
|---|---|
| gercek_hata | 0/2 |
| gercek_ozellik | 1/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| ck_aralik | gercek_hata | ❌ | 45.5 | 22 | başarısızlığı söylemedi; FAILED (errors=1) |
| ck_secenek_sirasi | gercek_hata | ❌ | 40.6 | 30 | gereksiz dosya: src/click/core.py; adım sınırı; AssertionError: '-v, --verbose' not found in 'Usage: k [OPTIONS]\n\nOptions:\n  --verbose, |
| ck_yeni_ozellik | gercek_ozellik | ✅ | 21.3 | 10 |  |
