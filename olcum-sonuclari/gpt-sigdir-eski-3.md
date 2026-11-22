# Ölçüm: gpt-sigdir-eski-3

2026-11-22 22:03 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 9/11 (%82)**, %95 güven aralığı %52–%95

Ortanca süre 70.1 sn, toplam 848 sn, zaman aşımı 0. Tamamlanan tur 5/11. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 4.

| Tür | Başarı |
|---|---|
| gercek_hata | 8/8 |
| gercek_ozellik | 1/3 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| ct_lru_okuma | gercek_hata | ✅ | 159.0 | 28 | gereksiz dosya: cachetools.py, cachetools/__init__.py, cachetools/keys.py, t; model hatası veya boş yanıt |
| ct_ttl_sinir | gercek_hata | ✅ | 94.6 | 28 | gereksiz dosya: cachetools/__init__.py, cachetools/func.py |
| ct_kapasite | gercek_hata | ✅ | 70.1 | 28 | gereksiz dosya: cachetools/__init__.py; model hatası veya boş yanıt |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 116.9 | 30 | gereksiz dosya: cachetools/__init__.py, tests/__init__.py; tur tamamlanmadı |
| mi_maxsplit | gercek_hata | ✅ | 58.6 | 10 |  |
| mi_partition | gercek_hata | ✅ | 44.6 | 8 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 83.0 | 29 | tur tamamlanmadı; ImportError: cannot import name 'every_nth' from 'more_itertools' (/work/more_itertools/__ |
| ck_aralik | gercek_hata | ✅ | 45.6 | 18 |  |
| ck_secim | gercek_hata | ✅ | 41.0 | 17 |  |
| ck_secenek_sirasi | gercek_hata | ✅ | 50.8 | 30 | tur tamamlanmadı |
| ck_yeni_ozellik | gercek_ozellik | ❌ | 83.5 | 19 | model hatası veya boş yanıt; AttributeError: truncate |
