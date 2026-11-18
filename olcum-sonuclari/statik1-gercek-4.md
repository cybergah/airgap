# Ölçüm: statik1-gercek-4

2026-11-14 21:20 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 2/3 (%67)**, %95 güven aralığı %21–%94

Ortanca süre 30.4 sn, toplam 91 sn, zaman aşımı 0. Tamamlanan tur 2/3. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 1.

| Tür | Başarı |
|---|---|
| gercek_hata | 1/2 |
| gercek_ozellik | 1/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| ck_aralik | gercek_hata | ❌ | 30.4 | 26 | adım sınırı; FAILED (errors=1) |
| ck_secenek_sirasi | gercek_hata | ✅ | 20.7 | 12 |  |
| ck_yeni_ozellik | gercek_ozellik | ✅ | 40.3 | 18 | gereksiz dosya: docs/__pycache__/conf.cpython-313.pyc, examples/aliases/__py |
