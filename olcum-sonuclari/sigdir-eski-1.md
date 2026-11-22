# Ölçüm: sigdir-eski-1

2026-11-22 18:00 · model `qwen3.6:35b-a3b` · 1 tekrar · harita 1000

**Başarı: 3/4 (%75)**, %95 güven aralığı %30–%95

Ortanca süre 89.5 sn, toplam 339 sn, zaman aşımı 0. Tamamlanan tur 4/4. Başarısız olup bunu söylemeyen 1. Gereksiz dosya değiştiren 0.

| Tür | Başarı |
|---|---|
| gercek_hata | 2/2 |
| gercek_ozellik | 1/2 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| ct_yeni_ozellik | gercek_ozellik | ✅ | 89.5 | 15 |  |
| mi_partition | gercek_hata | ✅ | 62.6 | 9 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 107.0 | 19 | başarısızlığı söylemedi; ImportError: cannot import name 'every_nth' from 'more_itertools' (/work/more_itertools/__ |
| ck_secenek_sirasi | gercek_hata | ✅ | 79.5 | 20 |  |
