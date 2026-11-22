# Ölçüm: sigdir-eski-2

2026-11-22 18:26 · model `qwen3.6:35b-a3b` · 1 tekrar · harita 1000

**Başarı: 3/4 (%75)**, %95 güven aralığı %30–%95

Ortanca süre 311.0 sn, toplam 989 sn, zaman aşımı 0. Tamamlanan tur 2/4. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 0.

| Tür | Başarı |
|---|---|
| gercek_hata | 2/2 |
| gercek_ozellik | 1/2 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| ct_yeni_ozellik | gercek_ozellik | ✅ | 107.1 | 15 |  |
| mi_partition | gercek_hata | ✅ | 191.7 | 14 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 311.0 | 22 | model hatası veya boş yanıt; ImportError: cannot import name 'every_nth' from 'more_itertools' (/work/more_itertools/__ |
| ck_secenek_sirasi | gercek_hata | ✅ | 379.0 | 31 | tur tamamlanmadı |
