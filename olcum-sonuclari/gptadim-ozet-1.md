# Ölçüm: gptadim-ozet-1

2026-11-24 00:23 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 5/9 (%56)**, %95 güven aralığı %27–%81

Ortanca süre 117.4 sn, toplam 991 sn, zaman aşımı 0. Tamamlanan tur 5/9. Başarısız olup bunu söylemeyen 2. Gereksiz dosya değiştiren 2.

| Tür | Başarı |
|---|---|
| zor_buyuk | 2/2 |
| zor_iki | 0/1 |
| zor_ozellik | 1/3 |
| zor_uzak | 1/2 |
| zor_yaniltici | 1/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| zc_anahtar | zor_uzak | ✅ | 87.4 | 42 |  |
| zc_peek | zor_ozellik | ❌ | 67.4 | 36 | model hatası veya boş yanıt; AttributeError: 'LRUCache' object has no attribute 'peek' |
| zc_istatistik | zor_yaniltici | ✅ | 159.7 | 58 | tur tamamlanmadı |
| zm_chunked_none | zor_uzak | ❌ | 99.1 | 27 | başarısızlığı söylemedi; gereksiz dosya: more_itertools/more.py; AssertionError: Lists differ: [] != [0, 1, 2] |
| zm_running_sum | zor_ozellik | ❌ | 137.2 | 56 | gereksiz dosya: docs/versions.rst; model hatası veya boş yanıt; FAILED (failures=1) |
| zm_windowed_adim | zor_buyuk | ✅ | 117.4 | 16 |  |
| zk_envvar_oncelik | zor_buyuk | ✅ | 148.8 | 60 | tur tamamlanmadı |
| zk_iki_hata | zor_iki | ❌ | 32.5 | 19 | başarısızlığı söylemedi; AssertionError: False is not true |
| zk_yeni_tip | zor_ozellik | ✅ | 141.8 | 45 |  |
