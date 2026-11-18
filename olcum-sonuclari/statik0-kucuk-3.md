# Ölçüm: statik0-kucuk-3

2026-11-14 21:10 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 2/3 (%67)**, %95 güven aralığı %21–%94

Ortanca süre 12.3 sn, toplam 38 sn, zaman aşımı 0. Tamamlanan tur 2/3. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 0.

| Tür | Başarı |
|---|---|
| cok_dosya | 1/2 |
| ozellik | 1/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| onbellek_dekorator | ozellik | ✅ | 14.4 | 11 |  |
| alan_ekle_katmanli | cok_dosya | ✅ | 12.3 | 12 |  |
| isim_degistir_tum | cok_dosya | ❌ | 11.0 | 8 | ajan durdurdu: tekrar; ImportError: cannot import name 'kdv_ekle' from 'para.vergi' (/work/para/vergi.py) |
