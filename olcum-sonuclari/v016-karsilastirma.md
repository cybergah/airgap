# v0.15 ve v0.16 adayı: aynı oturumda dönüşümlü ölçüm

2026-11-26/27 · `qwen3.6:35b-a3b` · bağlam 32K · 30 adım · görev başına 600 sn · zor set (9 görev) × 2 kol × 3 tur

- v0.15: `deb24ca` (git worktree).
- Aday: anlık kontrol, %60 kırpma, düşünme kesintisi sayacının düzeltilmesi ve yeni devam notu.
- Sıra: v0.15 önce, sonra aday önce, sonra v0.15 önce.
- Android emülatörü kapalıydı.

## Makine durumu (her kolun başında)

| Yoklama | Saat | Boş RAM | Model bellekte | Hız (belirteç/sn) |
|---|---|---|---|---|
| 1. tur v0.15 | 22:18 | 6153 MB | 9646 MB | 70,8 |
| 1. tur aday | 22:38 | 2348 MB | 16042 MB | 70,9 |
| 2. tur aday | 23:04 | 2108 MB | 15859 MB | 71,0 |
| 2. tur v0.15 | 23:32 | 2130 MB | 15961 MB | 53,6 |
| 3. tur v0.15 | 23:59 | 3645 MB | 14584 MB | 63,2 |
| 3. tur aday | 00:27 | 2480 MB | 9500 MB | 67,7 |
| Son | 00:47 | 2283 MB | 15070 MB | 67,1 |

Hız sabit bir istemle ölçüldü (400 belirteç, düşünme kapalı). 54-71 aralığında kaldı. Önceki tam set ölçümünde hız 14 belirteç/sn'ye kadar düşmüştü; bu ölçümde öyle bir çöküş yok. Model bellekten atılmadı.

## Sonuç

Her hücrede başarı ve saniye cinsinden süre var: ✓ geçti, ✗ kaldı.

| Görev | v0.15 (tur 1 / 2 / 3) | Aday (tur 1 / 2 / 3) |
|---|---|---|
| zc_anahtar | ✓37 ✓98 ✓110 | ✓46 ✓50 ✓31 |
| zc_peek | ✓410 ✓199 ✓505 | ✓191 ✓181 ✓196 |
| zc_istatistik | ✓100 ✓107 ✓158 | ✓67 ✓100 ✓167 |
| zm_chunked_none | ✓77 ✓157 ✓64 | ✓98 ✓246 ✓128 |
| zm_running_sum | ✓156 ✓138 ✓134 | ✓177 ✓159 ✗153 |
| zm_windowed_adim | ✓100 ✓428 ✓267 | ✗600 ✗600 ✓158 |
| zk_envvar_oncelik | ✓112 ✓140 ✓183 | ✓87 ✓105 ✓97 |
| zk_iki_hata | ✓87 ✓104 ✓117 | ✓61 ✓81 ✓71 |
| zk_yeni_tip | ✓102 ✓195 ✓80 | ✓147 ✓128 ✓154 |
| **Toplam** | **27/27** | **24/27** |
| Turlar | 9 / 9 / 9 | 8 / 8 / 8 |
| Zaman aşımı | 0 | 2 |
| Toplam süre | 4363 sn | 4281 sn |

Fark anlamlı değil (Fisher, iki yönlü p ≈ 0,24). Ama aday daha iyi de değil.

## Kayıplar

- **zm_windowed_adim, aday 1 ve 2. tur (600 sn zaman aşımı):**
  - Model çok uzun düşündü: tek koşuda toplam 100 bin ve 72 bin harf, tek adımda 15-24 bin harf.
  - Her koşuda yalnız 1 düşünme kesintisi oldu; art arda kesinti döngüsü yoktu. Anlık kontrol notu da yoktu.
  - Üretim hızı düşmedi: aday-1 585 sn'de 23,8 bin belirteç üretti, v0.15-2 427 sn'de 11,8 bin.
  - Yani zaman, makinenin yavaşlamasına değil, düşünme miktarına gitti.
  - v0.15'te de bu görev tek koşuda 88 bin harf düşündü ama 427 sn'de bitti.
  - Görev önceki ölçümlerde de oynaktı: qwen32k'de v0.15 1/3 geçmişti.
- **zm_running_sum, aday 3. tur:**
  - Bir düzenleme tutmadı (`old_text` bulunamadı).
  - Gizli test, belgeye (`autofunction`) eklenmesi gereken satırda kaldı.
  - Anlık kontrol 3 not verdi; hata onlardan gelmedi.

## Karar

Temiz değil. Aday v0.15'i geçemedi: 24/27'ye karşı 27/27. Kayıpların ikisi değişikliklerin ölçtüğümüz bir etkisine bağlanamıyor (makine normaldi, kesinti döngüsü yoktu). Yine de "bozulma yok" demek için kanıt yetmiyor. v0.16.0 bu ölçümle çıkmıyor.
