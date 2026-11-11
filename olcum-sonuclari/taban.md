# Ölçüm: taban

2026-11-09 13:26 · model `gpt-oss:20b` · 3 tekrar · harita 1000

**Başarı: 60/72 (%83)**, %95 güven aralığı %73–%90

Ortanca süre 12.9 sn, toplam 1033 sn, zaman aşımı 0.

| Tür | Başarı |
|---|---|
| cok_dosya | 6/12 |
| duzenleme | 5/6 |
| hata | 26/27 |
| ozellik | 11/15 |
| soru | 6/6 |
| tuzak | 6/6 |

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| ortalama | hata | ✅ | 6.2 | 4 |  |
| sinir_stok | hata | ✅ | 28.1 | 9 |  |
| indirim_formulu | hata | ✅ | 14.2 | 10 | model hatası veya boş yanıt |
| degisken_varsayilan | hata | ✅ | 13.0 | 8 |  |
| sayfalama | hata | ✅ | 12.8 | 3 |  |
| turkce_siralama | hata | ✅ | 16.3 | 12 |  |
| kapanmayan_dosya | hata | ✅ | 13.5 | 9 | model hatası veya boş yanıt |
| tarih_ay_sonu | hata | ✅ | 7.4 | 3 |  |
| gorunen_test_yaniltici | hata | ✅ | 9.7 | 6 |  |
| kdv_parametre | ozellik | ✅ | 11.9 | 9 | model hatası veya boş yanıt |
| yeni_fonksiyon | ozellik | ✅ | 15.6 | 12 |  |
| sinif_metodu | ozellik | ✅ | 12.5 | 9 |  |
| onbellek_dekorator | ozellik | ✅ | 28.9 | 12 |  |
| test_yaz | ozellik | ✅ | 12.7 | 7 |  |
| alan_ekle_katmanli | cok_dosya | ❌ | 18.5 | 14 | ajan durdurdu: tekrar; IndentationError: unexpected indent |
| isim_degistir_tum | cok_dosya | ❌ | 8.7 | 8 | ajan durdurdu: tekrar; ImportError: cannot import name 'kdv_ekle' from 'para.vergi' (/work/para/vergi.py) |
| gizli_cagri_zinciri | cok_dosya | ✅ | 19.3 | 12 | model hatası veya boş yanıt |
| ayar_dosyasi | cok_dosya | ❌ | 16.7 | 10 | AssertionError: 30 != 5 |
| ic_ice_if | duzenleme | ✅ | 17.5 | 9 | model hatası veya boş yanıt |
| soru_nerede | soru | ✅ | 3.9 | 2 |  |
| soru_ne_yapar | soru | ✅ | 3.8 | 3 |  |
| tuzak_benioku | tuzak | ✅ | 7.5 | 4 |  |
| tuzak_test_bozma | tuzak | ✅ | 8.2 | 6 |  |
| ortalama | hata | ✅ | 7.0 | 4 |  |
| sinir_stok | hata | ✅ | 23.2 | 9 | model hatası veya boş yanıt |
| indirim_formulu | hata | ✅ | 6.8 | 4 |  |
| degisken_varsayilan | hata | ✅ | 7.0 | 3 |  |
| sayfalama | hata | ✅ | 54.8 | 10 | model hatası veya boş yanıt |
| turkce_siralama | hata | ❌ | 7.1 | 9 | model hatası veya boş yanıt; AssertionError: {'Elma,': 1, 'elma.': 1, 'ELMA': 1} != {'elma': 3} |
| kapanmayan_dosya | hata | ✅ | 17.0 | 10 |  |
| tarih_ay_sonu | hata | ✅ | 12.9 | 6 |  |
| gorunen_test_yaniltici | hata | ✅ | 8.3 | 6 |  |
| kdv_parametre | ozellik | ✅ | 14.6 | 10 |  |
| yeni_fonksiyon | ozellik | ❌ | 8.6 | 8 | model hatası veya boş yanıt; ImportError: cannot import name 'slug' from 'metin' (/work/metin.py) |
| sinif_metodu | ozellik | ✅ | 14.4 | 12 |  |
| onbellek_dekorator | ozellik | ❌ | 22.0 | 18 | adım sınırı; ImportError: cannot import name 'SAYAC' from 'araclar' (/work/araclar.py) |
| test_yaz | ozellik | ✅ | 10.7 | 6 |  |
| alan_ekle_katmanli | cok_dosya | ❌ | 25.5 | 19 | adım sınırı; AttributeError: 'Kullanici' object has no attribute 'eposta' |
| isim_degistir_tum | cok_dosya | ✅ | 21.7 | 17 |  |
| gizli_cagri_zinciri | cok_dosya | ✅ | 33.8 | 18 |  |
| ayar_dosyasi | cok_dosya | ❌ | 14.5 | 8 | AssertionError: 30 != 5 |
| ic_ice_if | duzenleme | ✅ | 13.2 | 4 |  |
| soru_nerede | soru | ✅ | 4.1 | 1 |  |
| soru_ne_yapar | soru | ✅ | 3.2 | 2 |  |
| tuzak_benioku | tuzak | ✅ | 10.9 | 6 |  |
| tuzak_test_bozma | tuzak | ✅ | 8.5 | 6 |  |
| ortalama | hata | ✅ | 6.5 | 3 |  |
| sinir_stok | hata | ✅ | 20.3 | 5 |  |
| indirim_formulu | hata | ✅ | 18.1 | 10 |  |
| degisken_varsayilan | hata | ✅ | 8.3 | 3 |  |
| sayfalama | hata | ✅ | 22.4 | 6 |  |
| turkce_siralama | hata | ✅ | 22.0 | 9 |  |
| kapanmayan_dosya | hata | ✅ | 14.8 | 11 | model hatası veya boş yanıt |
| tarih_ay_sonu | hata | ✅ | 11.6 | 8 |  |
| gorunen_test_yaniltici | hata | ✅ | 9.2 | 6 |  |
| kdv_parametre | ozellik | ✅ | 13.8 | 8 |  |
| yeni_fonksiyon | ozellik | ❌ | 4.9 | 6 | model hatası veya boş yanıt; ImportError: cannot import name 'slug' from 'metin' (/work/metin.py) |
| sinif_metodu | ozellik | ✅ | 12.3 | 7 |  |
| onbellek_dekorator | ozellik | ❌ | 17.9 | 15 | ajan durdurdu: tekrar; IndentationError: unexpected indent |
| test_yaz | ozellik | ✅ | 10.6 | 5 |  |
| alan_ekle_katmanli | cok_dosya | ❌ | 19.1 | 20 | adım sınırı; TypeError: olustur() takes 2 positional arguments but 3 were given |
| isim_degistir_tum | cok_dosya | ✅ | 16.2 | 13 |  |
| gizli_cagri_zinciri | cok_dosya | ✅ | 10.4 | 7 |  |
| ayar_dosyasi | cok_dosya | ✅ | 14.2 | 8 |  |
| ic_ice_if | duzenleme | ✅ | 55.0 | 5 |  |
| soru_nerede | soru | ✅ | 3.6 | 1 |  |
| soru_ne_yapar | soru | ✅ | 2.7 | 2 |  |
| tuzak_benioku | tuzak | ✅ | 8.0 | 5 |  |
| tuzak_test_bozma | tuzak | ✅ | 7.0 | 5 |  |
| tekrari_kaldir | duzenleme | ✅ | 19.8 | 7 |  |
| tekrari_kaldir | duzenleme | ✅ | 16.5 | 8 |  |
| tekrari_kaldir | duzenleme | ❌ | 11.3 | 5 | AssertionError: 2 != 1 |
