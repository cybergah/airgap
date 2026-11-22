# Ölçüm: model-gpt-oss-2

2026-11-22 15:25 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 10/11 (%91)**, %95 güven aralığı %62–%98

Ortanca süre 65.2 sn, toplam 640 sn, zaman aşımı 0. Tamamlanan tur 8/11. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 2.

| Tür | Başarı |
|---|---|
| gercek_hata | 8/8 |
| gercek_ozellik | 2/3 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| ct_lru_okuma | gercek_hata | ✅ | 68.8 | 24 |  |
| ct_ttl_sinir | gercek_hata | ✅ | 24.2 | 16 |  |
| ct_kapasite | gercek_hata | ✅ | 85.9 | 29 | gereksiz dosya: cachetools/__init__.py; tur tamamlanmadı |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 69.7 | 25 | gereksiz dosya: cachetools/__init__.py, cachetools/func.py, cachetools/keys. |
| mi_maxsplit | gercek_hata | ✅ | 73.2 | 8 |  |
| mi_partition | gercek_hata | ✅ | 37.0 | 7 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 76.1 | 27 | model hatası veya boş yanıt; ImportError: cannot import name 'every_nth' from 'more_itertools' (/work/more_itertools/__ |
| ck_aralik | gercek_hata | ✅ | 65.2 | 28 |  |
| ck_secim | gercek_hata | ✅ | 31.9 | 15 |  |
| ck_secenek_sirasi | gercek_hata | ✅ | 48.3 | 30 | tur tamamlanmadı |
| ck_yeni_ozellik | gercek_ozellik | ✅ | 59.6 | 20 |  |
