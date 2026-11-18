# Ölçüm: statik0-kucuk-5

2026-11-14 21:21 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 2/3 (%67)**, %95 güven aralığı %21–%94

Ortanca süre 14.6 sn, toplam 41 sn, zaman aşımı 0. Tamamlanan tur 2/3. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 0.

| Tür | Başarı |
|---|---|
| cok_dosya | 1/2 |
| ozellik | 1/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| onbellek_dekorator | ozellik | ✅ | 14.6 | 8 |  |
| alan_ekle_katmanli | cok_dosya | ✅ | 15.1 | 12 |  |
| isim_degistir_tum | cok_dosya | ❌ | 11.0 | 7 | ajan durdurdu: tekrar; ImportError: cannot import name 'kdv_ekle' from 'para.vergi' (/work/para/vergi.py) |
