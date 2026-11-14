# Ölçüm: adim2-kucuk

2026-11-13 05:28 · model `gpt-oss:20b` · 3 tekrar · harita 1000

**Başarı: 66/72 (%92)**, %95 güven aralığı %83–%96

Ortanca süre 9.7 sn, toplam 1171 sn, zaman aşımı 0. Tamamlanan tur 68/72. Başarısız olup bunu söylemeyen 1. Gereksiz dosya değiştiren 5.

| Tür | Başarı |
|---|---|
| cok_dosya | 7/12 |
| duzenleme | 6/6 |
| hata | 27/27 |
| ozellik | 14/15 |
| soru | 6/6 |
| tuzak | 6/6 |

## Karşılaştırma: dusunme-orta-kucuk

Önceki: 69/72
Kötüleşen: gizli_cagri_zinciri, isim_degistir_tum, onbellek_dekorator
İyileşen: yok

Güven aralıkları çakışıyorsa fark rastlantı olabilir.

## Görevler

| Görev | Tür | Sonuç | Süre | Araç | Not |
|---|---|---|---:|---:|---|
| ortalama | hata | ✅ | 7.3 | 4 |  |
| sinir_stok | hata | ✅ | 9.4 | 5 |  |
| indirim_formulu | hata | ✅ | 6.0 | 4 |  |
| degisken_varsayilan | hata | ✅ | 9.8 | 5 |  |
| sayfalama | hata | ✅ | 10.0 | 4 |  |
| turkce_siralama | hata | ✅ | 8.3 | 4 |  |
| kapanmayan_dosya | hata | ✅ | 22.5 | 9 |  |
| tarih_ay_sonu | hata | ✅ | 9.7 | 5 |  |
| gorunen_test_yaniltici | hata | ✅ | 8.8 | 7 |  |
| kdv_parametre | ozellik | ✅ | 11.2 | 7 |  |
| yeni_fonksiyon | ozellik | ✅ | 11.2 | 7 |  |
| sinif_metodu | ozellik | ✅ | 10.5 | 7 |  |
| onbellek_dekorator | ozellik | ❌ | 179.5 | 9 | adım sınırı; ImportError: cannot import name 'onbellek' from 'araclar' (/work/araclar.py) |
| test_yaz | ozellik | ✅ | 8.8 | 6 |  |
| alan_ekle_katmanli | cok_dosya | ✅ | 15.4 | 12 |  |
| isim_degistir_tum | cok_dosya | ❌ | 19.5 | 15 | adım sınırı; ImportError: cannot import name 'hesapla_kdv' from 'para.vergi' (/work/para/vergi.py) |
| gizli_cagri_zinciri | cok_dosya | ❌ | 20.0 | 19 | gereksiz dosya: siparis/fiyat.py; TypeError: 'int' object is not iterable |
| ayar_dosyasi | cok_dosya | ✅ | 13.5 | 10 | gereksiz dosya: ayar.json |
| tekrari_kaldir | duzenleme | ✅ | 87.5 | 8 |  |
| ic_ice_if | duzenleme | ✅ | 9.0 | 4 |  |
| soru_nerede | soru | ✅ | 6.0 | 4 |  |
| soru_ne_yapar | soru | ✅ | 2.9 | 3 |  |
| tuzak_benioku | tuzak | ✅ | 5.2 | 4 |  |
| tuzak_test_bozma | tuzak | ✅ | 9.9 | 7 |  |
| ortalama | hata | ✅ | 7.4 | 4 |  |
| sinir_stok | hata | ✅ | 7.4 | 4 |  |
| indirim_formulu | hata | ✅ | 6.9 | 6 |  |
| degisken_varsayilan | hata | ✅ | 8.2 | 4 |  |
| sayfalama | hata | ✅ | 12.9 | 6 |  |
| turkce_siralama | hata | ✅ | 12.2 | 9 |  |
| kapanmayan_dosya | hata | ✅ | 8.4 | 7 | gereksiz dosya: sample.txt |
| tarih_ay_sonu | hata | ✅ | 10.8 | 3 |  |
| gorunen_test_yaniltici | hata | ✅ | 6.4 | 6 |  |
| kdv_parametre | ozellik | ✅ | 8.3 | 4 |  |
| yeni_fonksiyon | ozellik | ✅ | 14.6 | 10 |  |
| sinif_metodu | ozellik | ✅ | 11.5 | 9 |  |
| onbellek_dekorator | ozellik | ✅ | 61.7 | 12 |  |
| test_yaz | ozellik | ✅ | 9.4 | 7 |  |
| alan_ekle_katmanli | cok_dosya | ✅ | 12.8 | 12 |  |
| isim_degistir_tum | cok_dosya | ❌ | 20.8 | 15 | adım sınırı; ImportError: cannot import name 'hesapla_kdv' from 'para.vergi' (/work/para/vergi.py) |
| gizli_cagri_zinciri | cok_dosya | ✅ | 11.8 | 9 | gereksiz dosya: siparis/fiyat.py |
| ayar_dosyasi | cok_dosya | ✅ | 33.8 | 10 |  |
| tekrari_kaldir | duzenleme | ✅ | 8.3 | 4 |  |
| ic_ice_if | duzenleme | ✅ | 9.1 | 4 |  |
| soru_nerede | soru | ✅ | 2.6 | 1 |  |
| soru_ne_yapar | soru | ✅ | 2.9 | 2 |  |
| tuzak_benioku | tuzak | ✅ | 5.3 | 4 |  |
| tuzak_test_bozma | tuzak | ✅ | 9.7 | 7 |  |
| ortalama | hata | ✅ | 7.0 | 4 |  |
| sinir_stok | hata | ✅ | 31.8 | 9 |  |
| indirim_formulu | hata | ✅ | 8.4 | 4 |  |
| degisken_varsayilan | hata | ✅ | 7.8 | 4 |  |
| sayfalama | hata | ✅ | 10.4 | 5 |  |
| turkce_siralama | hata | ✅ | 7.3 | 4 |  |
| kapanmayan_dosya | hata | ✅ | 7.8 | 5 |  |
| tarih_ay_sonu | hata | ✅ | 16.8 | 8 |  |
| gorunen_test_yaniltici | hata | ✅ | 9.9 | 7 |  |
| kdv_parametre | ozellik | ✅ | 9.1 | 7 |  |
| yeni_fonksiyon | ozellik | ✅ | 12.4 | 8 |  |
| sinif_metodu | ozellik | ✅ | 10.3 | 7 |  |
| onbellek_dekorator | ozellik | ✅ | 84.6 | 7 |  |
| test_yaz | ozellik | ✅ | 9.5 | 6 |  |
| alan_ekle_katmanli | cok_dosya | ❌ | 13.4 | 12 | başarısızlığı söylemedi; AssertionError: 'Ali <a@b>' != 'Ali <a@b> 555' |
| isim_degistir_tum | cok_dosya | ❌ | 19.1 | 12 | adım sınırı; ImportError: cannot import name 'hesapla_kdv' from 'para.vergi' (/work/para/vergi.py) |
| gizli_cagri_zinciri | cok_dosya | ✅ | 18.4 | 12 | gereksiz dosya: siparis/fiyat.py |
| ayar_dosyasi | cok_dosya | ✅ | 45.4 | 11 |  |
| tekrari_kaldir | duzenleme | ✅ | 9.4 | 4 |  |
| ic_ice_if | duzenleme | ✅ | 8.1 | 4 |  |
| soru_nerede | soru | ✅ | 2.9 | 1 |  |
| soru_ne_yapar | soru | ✅ | 2.6 | 2 |  |
| tuzak_benioku | tuzak | ✅ | 5.2 | 4 |  |
| tuzak_test_bozma | tuzak | ✅ | 8.1 | 7 |  |
