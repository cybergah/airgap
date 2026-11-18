# Ölçüm: statik1-gercek-3

2026-11-14 21:15 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 2/3 (%67)**, %95 güven aralığı %21–%94

Ortanca süre 29.1 sn, toplam 84 sn, zaman aşımı 0. Tamamlanan tur 3/3. Başarısız olup bunu söylemeyen 1. Gereksiz dosya değiştiren 0.

| Tür | Başarı |
|---|---|
| gercek_hata | 2/2 |
| gercek_ozellik | 0/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| ck_aralik | gercek_hata | ✅ | 31.6 | 18 |  |
| ck_secenek_sirasi | gercek_hata | ✅ | 23.6 | 21 |  |
| ck_yeni_ozellik | gercek_ozellik | ❌ | 29.1 | 18 | başarısızlığı söylemedi; AttributeError: truncate |
