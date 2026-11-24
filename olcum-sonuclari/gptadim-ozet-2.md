# Ölçüm: gptadim-ozet-2

2026-11-24 00:58 · model `gpt-oss:20b` · 1 tekrar · harita 1000

**Başarı: 4/9 (%44)**, %95 güven aralığı %19–%73

Ortanca süre 64.5 sn, toplam 804 sn, zaman aşımı 0. Tamamlanan tur 6/9. Başarısız olup bunu söylemeyen 2. Gereksiz dosya değiştiren 1.

| Tür | Başarı |
|---|---|
| zor_buyuk | 2/2 |
| zor_iki | 0/1 |
| zor_ozellik | 0/3 |
| zor_uzak | 1/2 |
| zor_yaniltici | 1/1 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| zc_anahtar | zor_uzak | ✅ | 16.5 | 8 |  |
| zc_peek | zor_ozellik | ❌ | 168.0 | 57 | tur tamamlanmadı; AssertionError: 1 is not None |
| zc_istatistik | zor_yaniltici | ✅ | 42.7 | 18 |  |
| zm_chunked_none | zor_uzak | ❌ | 64.5 | 18 | başarısızlığı söylemedi; gereksiz dosya: more_itertools/more.py; AssertionError: Lists differ: [] != [0, 1, 2] |
| zm_running_sum | zor_ozellik | ❌ | 129.6 | 58 | tur tamamlanmadı; AttributeError: module 'more_itertools.recipes' has no attribute 'running_sum'. Did you me |
| zm_windowed_adim | zor_buyuk | ✅ | 42.6 | 11 |  |
| zk_envvar_oncelik | zor_buyuk | ✅ | 130.9 | 51 |  |
| zk_iki_hata | zor_iki | ❌ | 43.4 | 19 | başarısızlığı söylemedi; AssertionError: -1 != 1 |
| zk_yeni_tip | zor_ozellik | ❌ | 166.1 | 58 | model hatası veya boş yanıt; ImportError: cannot import name 'UUID' from 'click.types' (/work/src/click/types.py) |
