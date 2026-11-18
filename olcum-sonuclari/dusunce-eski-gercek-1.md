# Ölçüm: dusunce-eski-gercek-1

2026-11-14 21:37 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 2/3 (%67)**, %95 güven aralığı %21–%94

Ortanca süre 26.3 sn, toplam 87 sn, zaman aşımı 0. Tamamlanan tur 3/3. Başarısız olup bunu söylemeyen 1. Gereksiz dosya değiştiren 0.

| Tür | Başarı |
|---|---|
| gercek_hata | 2/2 |
| gercek_ozellik | 0/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| ck_aralik | gercek_hata | ✅ | 26.3 | 19 |  |
| ck_secenek_sirasi | gercek_hata | ✅ | 19.8 | 11 |  |
| ck_yeni_ozellik | gercek_ozellik | ❌ | 41.1 | 18 | başarısızlığı söylemedi; ImportError: cannot import name '_make_default_short_help' from 'click.utils' (/work/src/c |
