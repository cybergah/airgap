# Ölçüm: statik1-kucuk-1

2026-11-14 21:03 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 2/3 (%67)**, %95 güven aralığı %21–%94

Ortanca süre 15.8 sn, toplam 45 sn, zaman aşımı 0. Tamamlanan tur 2/3. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 0.

| Tür | Başarı |
|---|---|
| cok_dosya | 1/2 |
| ozellik | 1/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| onbellek_dekorator | ozellik | ✅ | 16.2 | 12 |  |
| alan_ekle_katmanli | cok_dosya | ✅ | 15.8 | 16 |  |
| isim_degistir_tum | cok_dosya | ❌ | 12.9 | 9 | ajan durdurdu: tekrar; ImportError: cannot import name 'kdv_ekle' from 'para.vergi' (/work/para/vergi.py) |
