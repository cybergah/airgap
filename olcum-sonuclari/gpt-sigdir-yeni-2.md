# Ölçüm: gpt-sigdir-yeni-2

2026-11-22 21:48 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 8/11 (%73)**, %95 güven aralığı %43–%90

Ortanca süre 61.4 sn, toplam 684 sn, zaman aşımı 0. Tamamlanan tur 6/11. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 0.

| Tür | Başarı |
|---|---|
| gercek_hata | 8/8 |
| gercek_ozellik | 0/3 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| ct_lru_okuma | gercek_hata | ✅ | 28.5 | 12 |  |
| ct_ttl_sinir | gercek_hata | ✅ | 31.0 | 11 |  |
| ct_kapasite | gercek_hata | ✅ | 39.3 | 13 |  |
| ct_yeni_ozellik | gercek_ozellik | ❌ | 61.4 | 30 | tur tamamlanmadı; AttributeError: 'LRUCache' object has no attribute 'fill_ratio' |
| mi_maxsplit | gercek_hata | ✅ | 121.8 | 8 |  |
| mi_partition | gercek_hata | ✅ | 102.0 | 13 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 50.3 | 29 | tur tamamlanmadı; ImportError: cannot import name 'every_nth' from 'more_itertools' (/work/more_itertools/__ |
| ck_aralik | gercek_hata | ✅ | 75.9 | 27 | tur tamamlanmadı |
| ck_secim | gercek_hata | ✅ | 40.1 | 15 |  |
| ck_secenek_sirasi | gercek_hata | ✅ | 62.1 | 29 | tur tamamlanmadı |
| ck_yeni_ozellik | gercek_ozellik | ❌ | 72.0 | 24 | model hatası veya boş yanıt; AttributeError: truncate |
