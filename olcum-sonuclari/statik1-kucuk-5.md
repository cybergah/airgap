# Ölçüm: statik1-kucuk-5

2026-11-14 21:24 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 2/3 (%67)**, %95 güven aralığı %21–%94

Ortanca süre 13.5 sn, toplam 45 sn, zaman aşımı 0. Tamamlanan tur 1/3. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 0.

| Tür | Başarı |
|---|---|
| cok_dosya | 1/2 |
| ozellik | 1/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| onbellek_dekorator | ozellik | ✅ | 18.3 | 18 | adım sınırı |
| alan_ekle_katmanli | cok_dosya | ✅ | 13.5 | 11 |  |
| isim_degistir_tum | cok_dosya | ❌ | 13.5 | 9 | ajan durdurdu: tekrar; ImportError: cannot import name 'kdv_ekle' from 'para.vergi' (/work/para/vergi.py) |
