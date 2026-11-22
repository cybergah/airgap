# Ölçüm: gpt-sigdir-eski-2

2026-11-22 21:37 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 10/11 (%91)**, %95 güven aralığı %62–%98

Ortanca süre 59.1 sn, toplam 791 sn, zaman aşımı 0. Tamamlanan tur 7/11. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 3.

| Tür | Başarı |
|---|---|
| gercek_hata | 8/8 |
| gercek_ozellik | 2/3 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| ct_lru_okuma | gercek_hata | ✅ | 81.8 | 30 | tur tamamlanmadı |
| ct_ttl_sinir | gercek_hata | ✅ | 43.4 | 15 |  |
| ct_kapasite | gercek_hata | ✅ | 95.2 | 28 | gereksiz dosya: cachetools/__init__.py; model hatası veya boş yanıt |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 43.4 | 19 |  |
| mi_maxsplit | gercek_hata | ✅ | 126.4 | 16 |  |
| mi_partition | gercek_hata | ✅ | 44.0 | 10 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 115.0 | 26 | gereksiz dosya: more_itertools/__init__.py; model hatası veya boş yanıt; FAILED (failures=1) |
| ck_aralik | gercek_hata | ✅ | 53.2 | 19 |  |
| ck_secim | gercek_hata | ✅ | 46.5 | 19 |  |
| ck_secenek_sirasi | gercek_hata | ✅ | 59.1 | 30 | tur tamamlanmadı |
| ck_yeni_ozellik | gercek_ozellik | ✅ | 83.4 | 27 | gereksiz dosya: src/click/truncate.py |
