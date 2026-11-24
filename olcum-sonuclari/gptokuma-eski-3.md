# Ölçüm: gptokuma-eski-3

2026-11-24 06:29 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 3/9 (%33)**, %95 güven aralığı %12–%65

Ortanca süre 57.4 sn, toplam 554 sn, zaman aşımı 0. Tamamlanan tur 2/9. Başarısız olup bunu söylemeyen 2. Gereksiz dosya değiştiren 2.

| Tür | Başarı |
|---|---|
| zor_buyuk | 1/2 |
| zor_iki | 1/1 |
| zor_ozellik | 0/3 |
| zor_uzak | 0/2 |
| zor_yaniltici | 1/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| zc_anahtar | zor_uzak | ❌ | 21.9 | 7 | model hatası veya boş yanıt; AssertionError: Lists differ: ['a'] != ['b'] |
| zc_peek | zor_ozellik | ❌ | 53.9 | 28 | tur tamamlanmadı; AttributeError: 'LRUCache' object has no attribute 'peek' |
| zc_istatistik | zor_yaniltici | ✅ | 69.1 | 28 | gereksiz dosya: cachetools/__init__.py, tmp_test.py, tmp_test2.py; model hatası veya boş yanıt |
| zm_chunked_none | zor_uzak | ❌ | 70.0 | 25 | başarısızlığı söylemedi; gereksiz dosya: more_itertools/more.py; AssertionError: Lists differ: [] != [0, 1, 2] |
| zm_running_sum | zor_ozellik | ❌ | 75.4 | 30 | tur tamamlanmadı; ImportError: cannot import name 'running_sum' from 'more_itertools' (/work/more_itertools/ |
| zm_windowed_adim | zor_buyuk | ❌ | 119.4 | 19 | başarısızlığı söylemedi; FAILED (failures=1) |
| zk_envvar_oncelik | zor_buyuk | ✅ | 48.1 | 25 | model hatası veya boş yanıt |
| zk_iki_hata | zor_iki | ✅ | 57.4 | 28 | tur tamamlanmadı |
| zk_yeni_tip | zor_ozellik | ❌ | 38.8 | 29 | tur tamamlanmadı; AttributeError: PERCENT |
