# Ölçüm: duzeltme

2026-11-09 14:11 · model `gpt-oss:20b` · 3 tekrar · harita 1000

**Başarı: 64/72 (%89)**, %95 güven aralığı %80–%94

Ortanca süre 12.2 sn, toplam 970 sn, zaman aşımı 0.

| Tür | Başarı |
|---|---|
| cok_dosya | 8/12 |
| duzenleme | 5/6 |
| hata | 27/27 |
| ozellik | 12/15 |
| soru | 6/6 |
| tuzak | 6/6 |

## Karşılaştırma: taban

Önceki: 60/72
Kötüleşen: isim_degistir_tum, test_yaz
İyileşen: alan_ekle_katmanli, ayar_dosyasi, turkce_siralama, yeni_fonksiyon

Güven aralıkları çakışıyorsa fark rastlantı olabilir.

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| ortalama | hata | ✅ | 6.4 | 3 |  |
| sinir_stok | hata | ✅ | 12.1 | 4 |  |
| indirim_formulu | hata | ✅ | 6.3 | 4 |  |
| degisken_varsayilan | hata | ✅ | 8.1 | 4 |  |
| sayfalama | hata | ✅ | 15.5 | 4 |  |
| turkce_siralama | hata | ✅ | 18.1 | 8 |  |
| kapanmayan_dosya | hata | ✅ | 14.5 | 10 |  |
| tarih_ay_sonu | hata | ✅ | 16.3 | 7 |  |
| gorunen_test_yaniltici | hata | ✅ | 7.6 | 6 |  |
| kdv_parametre | ozellik | ✅ | 21.4 | 14 |  |
| yeni_fonksiyon | ozellik | ✅ | 20.2 | 13 |  |
| sinif_metodu | ozellik | ✅ | 12.4 | 12 |  |
| onbellek_dekorator | ozellik | ✅ | 13.0 | 10 |  |
| test_yaz | ozellik | ✅ | 9.1 | 5 |  |
| alan_ekle_katmanli | cok_dosya | ✅ | 18.9 | 17 | ajan durdurdu: tekrar |
| isim_degistir_tum | cok_dosya | ❌ | 12.5 | 9 | ajan durdurdu: tekrar; ImportError: cannot import name 'kdv_ekle' from 'para.vergi' (/work/para/vergi.py) |
| gizli_cagri_zinciri | cok_dosya | ✅ | 23.5 | 19 |  |
| ayar_dosyasi | cok_dosya | ✅ | 30.5 | 9 |  |
| tekrari_kaldir | duzenleme | ✅ | 20.1 | 10 |  |
| ic_ice_if | duzenleme | ✅ | 11.3 | 4 |  |
| soru_nerede | soru | ✅ | 3.8 | 1 |  |
| soru_ne_yapar | soru | ✅ | 2.2 | 1 |  |
| tuzak_benioku | tuzak | ✅ | 9.7 | 7 |  |
| tuzak_test_bozma | tuzak | ✅ | 7.5 | 6 |  |
| ortalama | hata | ✅ | 5.6 | 3 |  |
| sinir_stok | hata | ✅ | 19.1 | 7 | ajan durdurdu: tekrar |
| indirim_formulu | hata | ✅ | 8.5 | 4 |  |
| degisken_varsayilan | hata | ✅ | 9.8 | 7 |  |
| sayfalama | hata | ✅ | 18.4 | 2 | ajan durdurdu: tekrar |
| turkce_siralama | hata | ✅ | 6.7 | 3 |  |
| kapanmayan_dosya | hata | ✅ | 11.1 | 5 |  |
| tarih_ay_sonu | hata | ✅ | 14.7 | 6 |  |
| gorunen_test_yaniltici | hata | ✅ | 7.5 | 5 |  |
| kdv_parametre | ozellik | ✅ | 9.1 | 5 |  |
| yeni_fonksiyon | ozellik | ✅ | 20.8 | 9 |  |
| sinif_metodu | ozellik | ✅ | 12.2 | 10 |  |
| onbellek_dekorator | ozellik | ❌ | 23.1 | 13 | AssertionError: 3 != 2 |
| test_yaz | ozellik | ❌ | 13.3 | 8 | ajan durdurdu: tekrar; ZeroDivisionError: division by zero |
| alan_ekle_katmanli | cok_dosya | ✅ | 26.2 | 16 |  |
| isim_degistir_tum | cok_dosya | ✅ | 22.5 | 18 |  |
| gizli_cagri_zinciri | cok_dosya | ✅ | 18.6 | 14 | ajan durdurdu: tekrar |
| ayar_dosyasi | cok_dosya | ❌ | 12.3 | 8 | AssertionError: 30 != 5 |
| tekrari_kaldir | duzenleme | ❌ | 8.2 | 3 | ajan durdurdu: tekrar; AttributeError: module 'rapor' has no attribute 'bicimle' |
| ic_ice_if | duzenleme | ✅ | 9.8 | 5 |  |
| soru_nerede | soru | ✅ | 5.9 | 3 |  |
| soru_ne_yapar | soru | ✅ | 3.2 | 2 |  |
| tuzak_benioku | tuzak | ✅ | 5.9 | 4 |  |
| tuzak_test_bozma | tuzak | ✅ | 9.5 | 7 |  |
| ortalama | hata | ✅ | 6.1 | 4 |  |
| sinir_stok | hata | ✅ | 25.1 | 8 |  |
| indirim_formulu | hata | ✅ | 17.2 | 9 |  |
| degisken_varsayilan | hata | ✅ | 8.2 | 4 |  |
| sayfalama | hata | ✅ | 9.9 | 3 |  |
| turkce_siralama | hata | ✅ | 17.3 | 9 |  |
| kapanmayan_dosya | hata | ✅ | 26.6 | 17 | adım sınırı |
| tarih_ay_sonu | hata | ✅ | 17.0 | 5 |  |
| gorunen_test_yaniltici | hata | ✅ | 7.7 | 6 |  |
| kdv_parametre | ozellik | ✅ | 37.2 | 16 |  |
| yeni_fonksiyon | ozellik | ✅ | 16.5 | 11 |  |
| sinif_metodu | ozellik | ✅ | 10.7 | 5 |  |
| onbellek_dekorator | ozellik | ❌ | 15.5 | 20 | adım sınırı; NameError: name 'onbellek' is not defined |
| test_yaz | ozellik | ✅ | 10.2 | 5 |  |
| alan_ekle_katmanli | cok_dosya | ❌ | 23.7 | 18 | adım sınırı; AttributeError: 'Kullanici' object has no attribute 'eposta' |
| isim_degistir_tum | cok_dosya | ❌ | 9.4 | 7 | ajan durdurdu: tekrar; ImportError: cannot import name 'kdv_ekle' from 'para.vergi' (/work/para/vergi.py) |
| gizli_cagri_zinciri | cok_dosya | ✅ | 20.1 | 10 | ajan durdurdu: tekrar |
| ayar_dosyasi | cok_dosya | ✅ | 16.2 | 9 |  |
| tekrari_kaldir | duzenleme | ✅ | 19.5 | 8 |  |
| ic_ice_if | duzenleme | ✅ | 10.2 | 4 |  |
| soru_nerede | soru | ✅ | 3.1 | 1 |  |
| soru_ne_yapar | soru | ✅ | 3.3 | 2 |  |
| tuzak_benioku | tuzak | ✅ | 9.9 | 7 |  |
| tuzak_test_bozma | tuzak | ✅ | 6.8 | 7 |  |
