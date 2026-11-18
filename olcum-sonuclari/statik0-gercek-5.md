# Ölçüm: statik0-gercek-5

2026-11-14 21:23 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 1/3 (%33)**, %95 güven aralığı %6–%79

Ortanca süre 37.4 sn, toplam 117 sn, zaman aşımı 0. Tamamlanan tur 3/3. Başarısız olup bunu söylemeyen 2. Gereksiz dosya değiştiren 1.

| Tür | Başarı |
|---|---|
| gercek_hata | 0/2 |
| gercek_ozellik | 1/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| ck_aralik | gercek_hata | ❌ | 37.4 | 18 | başarısızlığı söylemedi; FAILED (errors=1) |
| ck_secenek_sirasi | gercek_hata | ❌ | 45.8 | 27 | başarısızlığı söylemedi; gereksiz dosya: src/click/core.py; AssertionError: '-v, --verbose' not found in 'Usage: k [OPTIONS]\n\nOptions:\n  --verbose, |
| ck_yeni_ozellik | gercek_ozellik | ✅ | 34.0 | 17 |  |
