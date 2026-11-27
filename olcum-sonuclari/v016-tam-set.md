# v0.16.0 adayı: tam zor set (9 görev × 3)

2026-11-26 · `qwen3.6:35b-a3b` · bağlam 32K · 30 adım · görev başına 600 sn · `qwen32k-1..3` ile aynı ayar

Aday: anlık kontrol + %60 kırpma + düşünme kesintisi sayacının düzeltilmesi + yeni devam notu (harf sınırı).

| Görev | qwen32k (v0.15, 2026-11-25) | Aday (2026-11-26) |
|---|---|---|
| zc_anahtar | 3/3 | 3/3 |
| zc_peek | 1/3 | 2/3 |
| zc_istatistik | 3/3 | 3/3 |
| zm_chunked_none | 3/3 | 2/3 |
| zm_running_sum | 2/3 | 0/3 |
| zm_windowed_adim | 1/3 | 0/3 |
| zk_envvar_oncelik | 3/3 | 1/3 |
| zk_iki_hata | 3/3 | 3/3 |
| zk_yeni_tip | 3/3 | 3/3 |
| **Toplam** | **22/27** | **17/27** |
| Zaman aşımı (600 sn) | 4 | 7 |

Turlara göre aday: 7/9, 5/9, 5/9 (v0.15: 8/9, 7/9, 7/9).

**Bu karşılaştırma geçerli değil: makine ölçüm sırasında yavaşladı.** Modelin üretim hızı (belirteç/sn, Ollama sayaçları):

| | 1. tur | 2. tur | 3. tur |
|---|---|---|---|
| Hız aralığı | 37-80 | 22-44 | 14-41 |
| Zaman aşımı | 1 | 2 | 4 |

Ölçüm bitince boş bellek 32 GB'ın 550 MB'ıydı. Android emülatörü ve OneDrive çalışıyordu. Qwen'in %40'ı işlemcide koştuğu için bellek sıkışması doğrudan üretimi yavaşlatıyor. 3. turdaki 4 zaman aşımında (zm_chunked_none, zm_running_sum, zk_envvar_oncelik, zm_windowed_adim) görev 600 sn'de bitemedi. zm_chunked_none ve zk_envvar_oncelik önceki ölçümlerde hep geçiyordu.

Hızın normal olduğu 1. tur (7/9), v0.15'in turlarıyla (8, 7, 7) aynı düzeyde.

**Değişikliklere bağlanabilecek bir bozulma görülmedi:**
- `zm_running_sum`: anlık kontrol ilk düzenlemedeki sözdizimi hatasını yakaladı ve model düzeltti. Kayıp sonradan geldi: model kendi testlerini ekledi ("test değiştirmek istedi" uyarısı) ve gizli testin bir adımı tutmadı.
- `zk_envvar_oncelik` 2. tur: 6 adımda bitti ve sonuç yanlıştı (`'map' != 'env'`). Kesinti ya da anlık kontrol notu yoktu.

**Karar:** Sürüm yok. Doğru karşılaştırma için v0.15 ile adayı **aynı oturumda dönüşümlü** ölçmek ve makineyi boş tutmak gerekiyor.

Bu dönüşümlü ölçüm yapıldı ve sonucu `v016-karsilastirma.md`'de: v0.15 27/27, aday 24/27. Sürüm çıkmadı.
