# Ölçüm: gptornek-yeni-2

2026-11-23 23:10 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 3/9 (%33)**, %95 güven aralığı %12–%65

Ortanca süre 68.1 sn, toplam 885 sn, zaman aşımı 0. Tamamlanan tur 4/9. Başarısız olup bunu söylemeyen 2. Gereksiz dosya değiştiren 1.

| Tür | Başarı |
|---|---|
| zor_buyuk | 1/2 |
| zor_iki | 1/1 |
| zor_ozellik | 0/3 |
| zor_uzak | 1/2 |
| zor_yaniltici | 0/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| zc_anahtar | zor_uzak | ✅ | 109.5 | 26 | model hatası veya boş yanıt |
| zc_peek | zor_ozellik | ❌ | 86.2 | 25 | model hatası veya boş yanıt; AssertionError: 1 is not None |
| zc_istatistik | zor_yaniltici | ❌ | 52.0 | 30 | tur tamamlanmadı; AssertionError: Tuples differ: (1, 2) != (2, 1) |
| zm_chunked_none | zor_uzak | ❌ | 68.1 | 13 | başarısızlığı söylemedi; gereksiz dosya: more_itertools/more.py; AssertionError: Lists differ: [] != [0, 1, 2] |
| zm_running_sum | zor_ozellik | ❌ | 53.9 | 30 | tur tamamlanmadı; ImportError: cannot import name 'running_sum' from 'more_itertools' (/work/more_itertools/ |
| zm_windowed_adim | zor_buyuk | ❌ | 362.6 | 25 | başarısızlığı söylemedi; AssertionError: Lists differ: [(1, 2), (2, 3), (3, 4), (4, None)] != [(1, 2), (2, 3), (3,  |
| zk_envvar_oncelik | zor_buyuk | ✅ | 40.2 | 19 |  |
| zk_iki_hata | zor_iki | ✅ | 44.5 | 19 |  |
| zk_yeni_tip | zor_ozellik | ❌ | 68.2 | 29 | tur tamamlanmadı; AttributeError: PERCENT |
