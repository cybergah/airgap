# Ölçüm: sigdir-eski-3

2026-11-22 19:12 · model `qwen3.6:35b-a3b` · 1 tekrar · harita 1000

**Başarı: 3/4 (%75)**, %95 güven aralığı %30–%95

Ortanca süre 332.9 sn, toplam 1114 sn, zaman aşımı 0. Tamamlanan tur 4/4. Başarısız olup bunu söylemeyen 1. Gereksiz dosya değiştiren 0.

| Tür | Başarı |
|---|---|
| gercek_hata | 1/2 |
| gercek_ozellik | 2/2 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| ct_yeni_ozellik | gercek_ozellik | ✅ | 139.5 | 11 |  |
| mi_partition | gercek_hata | ✅ | 141.1 | 10 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ✅ | 332.9 | 27 |  |
| ck_secenek_sirasi | gercek_hata | ❌ | 500.7 | 17 | başarısızlığı söylemedi; AssertionError: '-v, --verbose' not found in 'Usage: k [OPTIONS]\n\nOptions:\n  --verbose, |
