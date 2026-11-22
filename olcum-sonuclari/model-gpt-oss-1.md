# Ölçüm: model-gpt-oss-1

2026-11-22 14:57 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 10/11 (%91)**, %95 güven aralığı %62–%98

Ortanca süre 45.7 sn, toplam 676 sn, zaman aşımı 0. Tamamlanan tur 4/11. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 4.

| Tür | Başarı |
|---|---|
| gercek_hata | 8/8 |
| gercek_ozellik | 2/3 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| ct_lru_okuma | gercek_hata | ✅ | 118.4 | 30 | gereksiz dosya: cachetools/__init__.py, tests/__init__.py; tur tamamlanmadı |
| ct_ttl_sinir | gercek_hata | ✅ | 88.7 | 30 | gereksiz dosya: cachetools/__init__.py; tur tamamlanmadı |
| ct_kapasite | gercek_hata | ✅ | 84.0 | 30 | gereksiz dosya: cachetools/__init__.py; tur tamamlanmadı |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 65.7 | 29 | gereksiz dosya: cachetools/__init__.py; tur tamamlanmadı |
| mi_maxsplit | gercek_hata | ✅ | 99.4 | 19 |  |
| mi_partition | gercek_hata | ✅ | 30.7 | 8 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 45.7 | 29 | tur tamamlanmadı; ImportError: cannot import name 'every_nth' from 'more_itertools' (/work/more_itertools/__ |
| ck_aralik | gercek_hata | ✅ | 44.5 | 14 | model hatası veya boş yanıt |
| ck_secim | gercek_hata | ✅ | 28.7 | 15 |  |
| ck_secenek_sirasi | gercek_hata | ✅ | 39.0 | 30 | tur tamamlanmadı |
| ck_yeni_ozellik | gercek_ozellik | ✅ | 31.3 | 11 |  |
