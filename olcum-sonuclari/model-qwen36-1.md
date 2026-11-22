# Ölçüm: model-qwen36-1

2026-11-22 15:14 · model `qwen3.6:35b-a3b` · 1 tekrar · harita 1000

**Başarı: 9/11 (%82)**, %95 güven aralığı %52–%95

Ortanca süre 80.8 sn, toplam 982 sn, zaman aşımı 0. Tamamlanan tur 9/11. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 0.

| Tür | Başarı |
|---|---|
| gercek_hata | 7/8 |
| gercek_ozellik | 2/3 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| ct_lru_okuma | gercek_hata | ✅ | 73.3 | 14 |  |
| ct_ttl_sinir | gercek_hata | ✅ | 112.0 | 20 |  |
| ct_kapasite | gercek_hata | ✅ | 66.9 | 16 |  |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 107.6 | 17 |  |
| mi_maxsplit | gercek_hata | ✅ | 72.3 | 9 |  |
| mi_partition | gercek_hata | ✅ | 110.1 | 10 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 80.8 | 15 | model hatası veya boş yanıt; ImportError: cannot import name 'every_nth' from 'more_itertools' (/work/more_itertools/__ |
| ck_aralik | gercek_hata | ✅ | 158.5 | 19 |  |
| ck_secim | gercek_hata | ✅ | 87.0 | 19 |  |
| ck_secenek_sirasi | gercek_hata | ❌ | 72.1 | 22 | model hatası veya boş yanıt; AssertionError: '-v, --verbose' not found in 'Usage: k [OPTIONS]\n\nOptions:\n  --verbose, |
| ck_yeni_ozellik | gercek_ozellik | ✅ | 41.7 | 11 |  |
