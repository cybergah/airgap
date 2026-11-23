# Ölçüm: gptornek-yeni-1

2026-11-23 22:44 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 3/9 (%33)**, %95 güven aralığı %12–%65

Ortanca süre 76.2 sn, toplam 759 sn, zaman aşımı 0. Tamamlanan tur 7/9. Başarısız olup bunu söylemeyen 4. Gereksiz dosya değiştiren 2.

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
| zc_anahtar | zor_uzak | ✅ | 75.5 | 17 |  |
| zc_peek | zor_ozellik | ❌ | 51.4 | 19 | başarısızlığı söylemedi; FAILED (failures=1) |
| zc_istatistik | zor_yaniltici | ✅ | 76.2 | 26 |  |
| zm_chunked_none | zor_uzak | ❌ | 87.3 | 21 | başarısızlığı söylemedi; gereksiz dosya: more_itertools/more.py; AssertionError: Lists differ: [] != [0, 1, 2] |
| zm_running_sum | zor_ozellik | ❌ | 90.1 | 25 | model hatası veya boş yanıt; ImportError: cannot import name 'running_sum' from 'more_itertools' (/work/more_itertools/ |
| zm_windowed_adim | zor_buyuk | ❌ | 161.8 | 13 | başarısızlığı söylemedi; AssertionError: Lists differ: [(1, 2), (2, 3), (3, 4), (4, None)] != [(1, 2), (2, 3), (3,  |
| zk_envvar_oncelik | zor_buyuk | ✅ | 57.8 | 24 |  |
| zk_iki_hata | zor_iki | ❌ | 94.8 | 29 | gereksiz dosya: tests/run_pytest.sh; tur tamamlanmadı; AssertionError: 11 != 9 |
| zk_yeni_tip | zor_ozellik | ❌ | 64.4 | 18 | başarısızlığı söylemedi; AttributeError: PERCENT |
