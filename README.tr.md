# Airgap (Kod Ajanı)

[English](README.md) · **Türkçe**

Yerel Ollama modeliyle çalışan, ajan modunda kod asistanı: terminalde ve VS Code panelinde.
Dosya okur ve düzenler, komut çalıştırır, sonucu kontrol eder. Yazma ve komut için onay ister.

## Gerekenler

- Python 3.10 veya üstü, git, [Ollama](https://ollama.com)
- Modeller: `ollama pull gpt-oss:20b` ve `ollama pull nomic-embed-text`
- VS Code (panel için)

## Kullanım

Terminalde, proje klasöründe:

```bash
python kod-ajani/ajan.py --dizin C:\projem
```

Komutlar: `/geri`, `/yeni`, `/onay`, `/yardim`, `/cik`.

VS Code eklentisini paketleyip kurmak için:

```bash
python kod-ajani/paketle.py
```

```bash
code --install-extension dist/kod-ajani-0.11.0.vsix --force
```

Sonra bir klasör aç ve soldaki `</>` simgesine bas. Ayarlar: **Airgap** (model, Python komutu, bağlam).

**Arayüz dili:** Varsayılan İngilizcedir. Türkçe için VS Code'da **Airgap › Dil** ayarını `tr` yap; terminalde `AIRGAP_LANG=tr` (PowerShell: `$env:AIRGAP_LANG="tr"`). Yalnız ekranda gördüklerin değişir; modele giden metinler aynı kalır.

Kod seçip **Ctrl+Alt+K**'ye basınca (veya sağ tık menüsünden) ne değişeceğini yazarsın; öneriyi fark görünümünde görüp uygular ya da reddedersin. Seçim yoksa bulunduğun satır düzenlenir. Uygulanan değişiklik kaydedilmez ve Ctrl+Z ile geri alınır.

## Özellikler

- Ajan döngüsü: oku, düzenle, komut çalıştır, doğrula
- Fark görünümü ve onay düğmeleri
- Modelin yanıtı ve düşünmesi panelde yazıldıkça akar. Ollama araç çağrısını (dosya içeriği dahil) tek parça hâlinde en sonda gönderdiği için model dosya yazarken 15–20 sn hiçbir şey akmayabilir; bu sırada durum satırı ne olduğunu ve geçen süreyi gösterir ("Model yazıyor · 12 sn", "Onayını bekliyor", "Komut çalışıyor · 3 sn").
- Geri alma noktaları (`%LOCALAPPDATA%\kod-ajani`; projenin `.git` klasörüne dokunmaz)
- Yerel anlamsal proje araması (`.gitignore` dosyaları dizine girmez)
- Seçili kodu düzenleme (Ctrl+Alt+K)
- Proje haritası: en önemli tanımlar her turda modele verilir (Aider'in yönteminden uyarlandı). Python için `ast`; JavaScript, TypeScript ve C# için Tree-sitter (kuruluysa); diğer diller için düzenli ifade. Fonksiyonların içindeki yerel tanımlar haritaya girmez. Tree-sitter isteğe bağlıdır, yoksa düzenli ifadeye dönülür:

```bash
python -m pip install tree-sitter tree-sitter-javascript tree-sitter-typescript tree-sitter-c-sharp
```

  Ölçüm: `python kod-ajani/harita_olc.py` (örnek dosyalar) ve `python kod-ajani/harita_karsilastir.py dosya...` (iki yöntemin farkı).

## Güvenlik

- Dosya yazma ve komut için onay istenir. `.env`, anahtar ve kimlik dosyalarını okumak da onay ister; bunlar aramaya ve haritaya girmez.
- Riskli görünen komutlarda (silme, ağ, paket kurma, git push, proje dışı yol) uyarı çıkar ve "hep izin ver" geçerli olmaz.
- Projedeki `AGENTS.md` modele kural olarak değil, depoyu yazan kişinin güvenilmez notu olarak verilir: yetki veremez, onay atlatamaz. İçinde ağ, gizli dosya, riskli komut veya "onay gerekmez" gibi ifadeler varsa başta uyarı çıkar. Proje dışını veya gizli bir dosyayı gösteriyorsa hiç okunmaz.
- Riskli komut algılaması iki katmanlı: metinde kalıp arama, ve komutun PowerShell'in kendi ayrıştırıcısıyla (kapsayıcıda `sh` için `shlex` ile) parçalarına ayrılması. Böylece ``Rem`ove-`Item``, `/bin/rm`, `git -C . push`, `[IO.Directory]::Delete(...)` gibi yazımlar da tanınır; adı çalışırken hesaplanan komutlar ve ayrıştırılamayan komutlar uyarı alır. Bu da güvenlik sınırı değildir: çalışırken üretilen kod okunamaz, yalnız işaretlenir. Ölçüm için `komut_ornekleri.py` ve `komut_sinav.py`.
- Komutlara adında `TOKEN`, `SECRET`, `PASSWORD`, `API_KEY` gibi ifadeler geçen ortam değişkenleri verilmez.
- İzin kuralları yalnız `%LOCALAPPDATA%\kod-ajani\izinler.json` dosyasından okunur, proje içinden izin verilemez:

```json
{ "izinli": ["python -m unittest", "npm test"], "yasak": ["docker"] }
```

`izinli` komutlar sormadan çalışır. Testleri izinli yaparsan modelin yazdığı kod da sormadan çalışabilir, bunu bilerek karar ver.

### Korumalı çalıştırma (Docker)

VS Code'da `kodAjani.korumaliCalistirma` ayarını aç veya terminalde `--korumali` kullan. Önce imajı indir: `docker pull python:3.13-slim`.

Komut ağı kapalı, yetkisiz bir kapsayıcıda çalışır: proje `/work` altında yazılabilir, `.git` ve benzeri klasörler salt okunur, gizli dosyalar boş görünür; bilgisayarın diski, ortam değişkenleri ve Docker görünmez. Docker çalışmıyorsa veya imaj yoksa komut **reddedilir**, bilgisayarda çalıştırılmaz.

Ajan ilk komuttan önce Docker'ın sistem çağrısı filtresinin (seccomp) gerçekten açık olduğunu dener: kapsayıcıda yasak bir çağrı (`unshare`) çalışırsa ya da deneme yapılamazsa (imajda `python3` veya `unshare` yoksa) komutlar reddedilir. `/proc` içindeki "Seccomp" satırına güvenilmez; Docker Desktop'ta filtre kapalıyken de açık görünüyor.

Sınırlar: Komutlar Linux'ta çalışır ve yalnız imajdaki araçları görür; ağ kapalı olduğu için paket kurulamaz. Proje dosyalarını yine değiştirebilir, bu yüzden değişiklikleri kontrol et: modelin yazdığı kodu sonradan bilgisayarında çalıştırırsan koruma geçerli olmaz. Gizli sayılmayan bir dosyadaki parola da kapsayıcıda görünür.

## Sınırlar

- **Korumalı çalıştırma kapalıyken bu kurallar güvenlik sınırı değildir.** Onayladığın komut senin yetkinle çalışır ve risk algılaması düzenli ifadeyle yapıldığı için atlatılabilir. Onaylamadan önce komutu oku; bilmediğin projelerde korumalı çalıştırmayı aç.
  "Bu sohbette hep izin ver" seçeneğini önemli projelerde kullanma.
- `.gitignore` dosyaları geri alma kapsamında değildir. Eski kayıtlar otomatik silinmez.
- Yerel model küçük ve orta görevler için ölçüldü; testlerin geçmesi her zaman asıl hatanın düzeldiği anlamına gelmez.

## Ölçüm

`kod-ajani/olcum.py` 24 görevlik seti gerçek modelle çalıştırır. Görevler modelin görmediği testlerle ölçülür; modelin kodu kapsayıcıda çalışır (Docker ve `python:3.13-slim` gerekir). Sonuçlar `olcum-sonuclari/` altına yazılır.

```bash
python kod-ajani/olcum.py --dogrula
```

```bash
python kod-ajani/olcum.py --etiket yeni --karsilastir taban --tekrar 3
```

`--set gercek` ise click, more-itertools ve cachetools'a yerleştirilen hatalarla ölçer (kaynaklar `%LOCALAPPDATA%\kod-ajani\olcum-projeler` altında olmalı).

Son ölçüm: küçük set 68/72 (%94), %87–%98 ([rapor](olcum-sonuclari/bitirme.md)); gerçek projeler 24/33 (%73), %56–%85 ([rapor](olcum-sonuclari/gercek-bitirme.md)). Hataları kendimiz yerleştirdiğimiz için bu oranlar kullanıcının gerçek projelerindeki başarıyı göstermez.

## Testler

GitHub'a her gönderimde birim testleri ve duman testi otomatik çalışır (`.github/workflows/testler.yml`, Windows). Gerçek modelli ölçümler ve gerçek VS Code testi yalnız yerelde çalışır.

```bash
cd kod-ajani && python -B -m unittest discover -p "test_*.py"
```

```bash
node kod-ajani/vscode-eklenti/test/duman.js
```

```powershell
powershell -ExecutionPolicy Bypass -File kod-ajani\vscode-eklenti\test\gercek-calistir.ps1
```

Gerçek modelle ölçüm: `deneme.py` (zor görev), `deneme_geri.py` (geri alma), `deneme_arama.py` ve `deneme_turkce.py` (arama), `deneme_secim.py` (seçili kod), `deneme_harita.py` (haritalı ve haritasız), `deneme_enjeksiyon.py` (dosyadaki kötü niyetli talimatlar).
