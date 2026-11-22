# Ölçüm: sigdir-eski-5

2026-11-22 20:16 · model `qwen3.6:35b-a3b` · 1 tekrar · harita 1000

**Başarı: 3/4 (%75)**, %95 güven aralığı %30–%95

Ortanca süre 225.6 sn, toplam 698 sn, zaman aşımı 0. Tamamlanan tur 4/4. Başarısız olup bunu söylemeyen 1. Gereksiz dosya değiştiren 0.

| Tür | Başarı |
|---|---|
| gercek_hata | 1/2 |
| gercek_ozellik | 2/2 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| ct_yeni_ozellik | gercek_ozellik | ✅ | 231.0 | 15 |  |
| mi_partition | gercek_hata | ✅ | 147.0 | 10 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ✅ | 225.6 | 31 |  |
| ck_secenek_sirasi | gercek_hata | ❌ | 94.4 | 9 | başarısızlığı söylemedi; AssertionError: '-v, --verbose' not found in 'Usage: k [OPTIONS]\n\nOptions:\n  --verbose, |
