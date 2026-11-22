# Ölçüm: gpt-sigdir-yeni-3

2026-11-22 22:18 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 9/11 (%82)**, %95 güven aralığı %52–%95

Ortanca süre 59.5 sn, toplam 862 sn, zaman aşımı 0. Tamamlanan tur 6/11. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 3.

| Tür | Başarı |
|---|---|
| gercek_hata | 8/8 |
| gercek_ozellik | 1/3 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| ct_lru_okuma | gercek_hata | ✅ | 118.7 | 30 | gereksiz dosya: cachetools/__init__.py, cachetools/func.py, cachetools/keys.; tur tamamlanmadı |
| ct_ttl_sinir | gercek_hata | ✅ | 87.4 | 30 | tur tamamlanmadı |
| ct_kapasite | gercek_hata | ✅ | 36.8 | 11 |  |
| ct_yeni_ozellik | gercek_ozellik | ✅ | 100.2 | 29 | gereksiz dosya: cachetools/__init__.py, cachetools/keys.py; tur tamamlanmadı |
| mi_maxsplit | gercek_hata | ✅ | 182.6 | 11 |  |
| mi_partition | gercek_hata | ✅ | 45.2 | 12 |  |
| mi_yeni_fonksiyon | gercek_ozellik | ❌ | 59.5 | 30 | tur tamamlanmadı; ImportError: cannot import name 'every_nth' from 'more_itertools' (/work/more_itertools/__ |
| ck_aralik | gercek_hata | ✅ | 68.6 | 19 |  |
| ck_secim | gercek_hata | ✅ | 58.7 | 19 |  |
| ck_secenek_sirasi | gercek_hata | ✅ | 50.1 | 17 | gereksiz dosya: tmp_test.py |
| ck_yeni_ozellik | gercek_ozellik | ❌ | 54.3 | 22 | model hatası veya boş yanıt; AttributeError: truncate |
