# Ölçüm: gptadim-a60-1

2026-11-24 00:06 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 3/9 (%33)**, %95 güven aralığı %12–%65

Ortanca süre 113.8 sn, toplam 1241 sn, zaman aşımı 0. Tamamlanan tur 6/9. Başarısız olup bunu söylemeyen 2. Gereksiz dosya değiştiren 2.

| Tür | Başarı |
|---|---|
| zor_buyuk | 1/2 |
| zor_iki | 0/1 |
| zor_ozellik | 0/3 |
| zor_uzak | 2/2 |
| zor_yaniltici | 0/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| zc_anahtar | zor_uzak | ✅ | 84.5 | 28 | gereksiz dosya: cachetools/__init__.py, cachetools/func.py, cachetools/keys. |
| zc_peek | zor_ozellik | ❌ | 113.8 | 60 | tur tamamlanmadı; AttributeError: 'LRUCache' object has no attribute 'peek' |
| zc_istatistik | zor_yaniltici | ❌ | 170.9 | 55 | başarısızlığı söylemedi; AssertionError: Tuples differ: (1, 2) != (2, 1) |
| zm_chunked_none | zor_uzak | ✅ | 55.9 | 28 |  |
| zm_running_sum | zor_ozellik | ❌ | 160.3 | 36 | model hatası veya boş yanıt; FAILED (failures=1) |
| zm_windowed_adim | zor_buyuk | ❌ | 372.1 | 55 | AssertionError: Lists differ: [(1, 2), (2, 3), (3, 4), (4, None)] != [(1, 2), (2, 3), (3,  |
| zk_envvar_oncelik | zor_buyuk | ✅ | 85.8 | 32 | gereksiz dosya: click/__init__.py |
| zk_iki_hata | zor_iki | ❌ | 64.2 | 34 | başarısızlığı söylemedi; AssertionError: 11 != 9 |
| zk_yeni_tip | zor_ozellik | ❌ | 133.4 | 50 | model hatası veya boş yanıt; AttributeError: PERCENT |
