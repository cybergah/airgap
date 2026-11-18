# Ölçüm: araç sonuçları modele İngilizce

2026-11-18 · model `gpt-oss:20b` · harita 1000

Araç sonuçları (dosya düzenlendi, çıkış kodu, hata mesajları) artık modele her zaman İngilizce gidiyor.
Önceden Türkçe gidiyordu ve model İngilizce yazan kullanıcıya Türkçe cevap veriyordu.

**Küçük set, 2 tekrar:** 46/48 (%96), %95 güven aralığı %86–%99 ([ayrıntı](ingilizce-sonuc.md)).
Önceki tek turluk ölçüm 24/24'tü; düşen iki görev zor çok dosyalı görevler.

**Düşen iki görev, eski ve yeni ajan sırayla, 5 tur** (`alan_ekle_katmanli`, `gizli_cagri_zinciri`):

| Tur | Eski (Türkçe sonuç) | Yeni (İngilizce sonuç) |
|---|---|---|
| 1 | 2/2 | 2/2 |
| 2 | 1/2 | 2/2 |
| 3 | 2/2 | 2/2 |
| 4 | 2/2 | 1/2 |
| 5 | 2/2 | 1/2 |
| **Toplam** | **9/10** | **8/10** |

Fark rastlantı sınırları içinde: iki ajan da bu görevlerde ara sıra başarısız oluyor. Değişiklik başarıyı ölçülebilir biçimde düşürmedi.
