# Ölçüm: gptkilit-ikisi-1

2026-11-24 17:40 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 1/9 (%11)**, %95 güven aralığı %2–%44

Ortanca süre 68.0 sn, toplam 793 sn, zaman aşımı 0. Tamamlanan tur 3/9. Başarısız olup bunu söylemeyen 3. Gereksiz dosya değiştiren 2.

| Tür | Başarı |
|---|---|
| zor_buyuk | 0/2 |
| zor_iki | 0/1 |
| zor_ozellik | 0/3 |
| zor_uzak | 1/2 |
| zor_yaniltici | 0/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| zc_anahtar | zor_uzak | ✅ | 68.0 | 27 | gereksiz dosya: tests/__init__.py; model hatası veya boş yanıt |
| zc_peek | zor_ozellik | ❌ | 41.8 | 14 | başarısızlığı söylemedi; AttributeError: 'LRUCache' object has no attribute 'peek' |
| zc_istatistik | zor_yaniltici | ❌ | 64.6 | 26 | başarısızlığı söylemedi; gereksiz dosya: src/cachetools/_decorator.py; AssertionError: Tuples differ: (1, 2) != (2, 1) |
| zm_chunked_none | zor_uzak | ❌ | 101.5 | 24 | model hatası veya boş yanıt; ImportError: cannot import name 'chunked' from partially initialized module 'more_itertool |
| zm_running_sum | zor_ozellik | ❌ | 142.7 | 24 | model hatası veya boş yanıt; AttributeError: module 'more_itertools.recipes' has no attribute 'running_sum'. Did you me |
| zm_windowed_adim | zor_buyuk | ❌ | 202.3 | 24 | model hatası veya boş yanıt; ImportError: cannot import name 'windowed' from 'more_itertools' (/work/more_itertools/__i |
| zk_envvar_oncelik | zor_buyuk | ❌ | 52.6 | 13 | model hatası veya boş yanıt; AssertionError: 'map' != 'env' |
| zk_iki_hata | zor_iki | ❌ | 41.9 | 15 | başarısızlığı söylemedi; AssertionError: 11 != 9 |
| zk_yeni_tip | zor_ozellik | ❌ | 77.2 | 24 | model hatası veya boş yanıt; AttributeError: PERCENT |
