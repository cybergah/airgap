# Ölçüm: gptkilit-ikisi-3

2026-11-24 18:52 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 2/9 (%22)**, %95 güven aralığı %6–%55

Ortanca süre 79.0 sn, toplam 828 sn, zaman aşımı 0. Tamamlanan tur 3/9. Başarısız olup bunu söylemeyen 1. Gereksiz dosya değiştiren 1.

| Tür | Başarı |
|---|---|
| zor_buyuk | 0/2 |
| zor_iki | 0/1 |
| zor_ozellik | 0/3 |
| zor_uzak | 1/2 |
| zor_yaniltici | 1/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| zc_anahtar | zor_uzak | ✅ | 25.5 | 12 |  |
| zc_peek | zor_ozellik | ❌ | 49.3 | 16 | başarısızlığı söylemedi; AssertionError: None != 1 |
| zc_istatistik | zor_yaniltici | ✅ | 39.9 | 11 |  |
| zm_chunked_none | zor_uzak | ❌ | 97.5 | 27 | gereksiz dosya: more_itertools/more.py; model hatası veya boş yanıt; AssertionError: Lists differ: [] != [0, 1, 2] |
| zm_running_sum | zor_ozellik | ❌ | 79.0 | 24 | model hatası veya boş yanıt; ImportError: cannot import name 'running_sum' from 'more_itertools' (/work/more_itertools/ |
| zm_windowed_adim | zor_buyuk | ❌ | 162.4 | 27 | tur tamamlanmadı; FAILED (failures=1) |
| zk_envvar_oncelik | zor_buyuk | ❌ | 74.8 | 28 | tur tamamlanmadı; AssertionError: 'map' != 'env' |
| zk_iki_hata | zor_iki | ❌ | 213.4 | 29 | tur tamamlanmadı; AssertionError: False is not true |
| zk_yeni_tip | zor_ozellik | ❌ | 86.0 | 24 | model hatası veya boş yanıt; NameError: name 'ParamType' is not defined |
