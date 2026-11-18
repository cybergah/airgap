# Ölçüm: statik0-kucuk-1

2026-11-14 21:00 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 1/3 (%33)**, %95 güven aralığı %6–%79

Ortanca süre 23.7 sn, toplam 72 sn, zaman aşımı 0. Tamamlanan tur 1/3. Başarısız olup bunu söylemeyen 0. Gereksiz dosya değiştiren 0.

| Tür | Başarı |
|---|---|
| cok_dosya | 0/2 |
| ozellik | 1/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| onbellek_dekorator | ozellik | ✅ | 30.7 | 8 |  |
| alan_ekle_katmanli | cok_dosya | ❌ | 17.8 | 19 | adım sınırı; TypeError: Kullanici.__init__() missing 1 required positional argument: 'telefon' |
| isim_degistir_tum | cok_dosya | ❌ | 23.7 | 15 | adım sınırı; AttributeError: module 'para.vergi' has no attribute 'hesapla_kdv' |
