# Ölçüm: statik0-kucuk-2

2026-11-14 21:05 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 1/3 (%33)**, %95 güven aralığı %6–%79

Ortanca süre 18.7 sn, toplam 49 sn, zaman aşımı 0. Tamamlanan tur 2/3. Başarısız olup bunu söylemeyen 1. Gereksiz dosya değiştiren 0.

| Tür | Başarı |
|---|---|
| cok_dosya | 0/2 |
| ozellik | 1/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| onbellek_dekorator | ozellik | ✅ | 18.7 | 14 |  |
| alan_ekle_katmanli | cok_dosya | ❌ | 21.2 | 20 | adım sınırı; AttributeError: 'Kullanici' object has no attribute 'eposta' |
| isim_degistir_tum | cok_dosya | ❌ | 8.8 | 10 | başarısızlığı söylemedi; ImportError: cannot import name 'hesapla_kdv' from 'para.vergi' (/work/para/vergi.py) |
