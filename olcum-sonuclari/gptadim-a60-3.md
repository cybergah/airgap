# Ölçüm: gptadim-a60-3

2026-11-24 01:22 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 3/9 (%33)**, %95 güven aralığı %12–%65

Ortanca süre 99.7 sn, toplam 806 sn, zaman aşımı 0. Tamamlanan tur 7/9. Başarısız olup bunu söylemeyen 4. Gereksiz dosya değiştiren 1.

| Tür | Başarı |
|---|---|
| zor_buyuk | 1/2 |
| zor_iki | 0/1 |
| zor_ozellik | 0/3 |
| zor_uzak | 1/2 |
| zor_yaniltici | 1/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| zc_anahtar | zor_uzak | ✅ | 25.2 | 12 |  |
| zc_peek | zor_ozellik | ❌ | 107.5 | 47 | başarısızlığı söylemedi; AttributeError: 'LRUCache' object has no attribute 'peek' |
| zc_istatistik | zor_yaniltici | ✅ | 116.7 | 43 |  |
| zm_chunked_none | zor_uzak | ❌ | 91.9 | 23 | başarısızlığı söylemedi; gereksiz dosya: more_itertools/more.py; AssertionError: Lists differ: [] != [0, 1, 2] |
| zm_running_sum | zor_ozellik | ❌ | 149.6 | 55 | model hatası veya boş yanıt; AttributeError: module 'more_itertools.recipes' has no attribute 'running_sum'. Did you me |
| zm_windowed_adim | zor_buyuk | ✅ | 46.7 | 11 |  |
| zk_envvar_oncelik | zor_buyuk | ❌ | 108.3 | 39 | başarısızlığı söylemedi; AssertionError: 'map' != 'env' |
| zk_iki_hata | zor_iki | ❌ | 60.9 | 28 | başarısızlığı söylemedi; AssertionError: -1 != 1 |
| zk_yeni_tip | zor_ozellik | ❌ | 99.7 | 41 | model hatası veya boş yanıt; AttributeError: PERCENT |
