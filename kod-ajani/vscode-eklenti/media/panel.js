"use strict";
// Model çıktısı güvenilmez metindir: her yerde textContent kullanılır, innerHTML asla.
(function () {
  const vscode = acquireVsCodeApi();
  const akis = document.getElementById("akis");
  const girdi = document.getElementById("girdi");
  const form = document.getElementById("form");
  const durum = document.getElementById("durum");
  const gonder = document.getElementById("gonder");
  const durBtn = document.getElementById("dur");
  const model = decodeURIComponent(document.body.dataset.model || "");
  // Arayüz dili eklentiden gelir (kodAjani.dil); varsayılan İngilizce.
  const DIL = document.body.dataset.dil === "tr" ? "tr" : "en";
  const L = (tr, en) => (DIL === "tr" ? tr : en);

  let mesgul = false;
  let dusunce = null;
  let icerik = null;
  let sonKart = null;
  // Ollama arac cagrisini (dosya icerigi dahil) tek parca halinde, en sonda gonderir: model dosya yazarken
  // panelde 15-20 sn hicbir sey akmaz (olculdu). Durum satiri ne olduğunu ve gecen sureyi gosterir.
  let asama = "model"; // "model" | "onay" | "komut"
  let sonCikti = Date.now();
  let sayac = null;

  function ogeOlustur(etiket, sinif, metin) {
    const o = document.createElement(etiket);
    if (sinif) o.className = sinif;
    if (metin !== undefined) o.textContent = metin;
    return o;
  }

  function ekle(o) {
    const altta = akis.scrollHeight - akis.scrollTop - akis.clientHeight < 80;
    akis.appendChild(o);
    if (altta) akis.scrollTop = akis.scrollHeight;
    return o;
  }

  function kaydir() {
    if (akis.scrollHeight - akis.scrollTop - akis.clientHeight < 200) akis.scrollTop = akis.scrollHeight;
  }

  function durumMetni(sn) {
    if (asama === "onay") {
      return [L("Onayını bekliyor", "Waiting for your approval"),
        L("Ajan devam etmek için onayını bekliyor.", "The agent needs your approval to continue.")];
    }
    if (asama === "komut") {
      return [L(`Komut çalışıyor · ${sn} sn`, `Command running · ${sn} s`),
        L("Onayladığın komut çalışıyor.", "The command you approved is running.")];
    }
    if (sn >= 5) {
      return [L(`Model yazıyor · ${sn} sn`, `Model writing · ${sn} s`),
        L("Model dosya içeriği veya komut hazırlıyor olabilir; bunlar bitince tek seferde görünür.",
          "The model may be preparing file contents or a command; they appear all at once when done.")];
    }
    return [L(`Model çalışıyor · ${sn} sn`, `Model working · ${sn} s`),
      L("Model düşünüyor veya yanıt yazıyor.", "The model is thinking or writing a reply.")];
  }

  function durumYaz() {
    const sn = Math.max(0, Math.floor((Date.now() - sonCikti) / 1000));
    const [kisa, uzun] = mesgul ? durumMetni(sn) : [model, ""];
    durum.textContent = kisa;
    durum.title = uzun || kisa; // dar panelde ayrinti uzerine gelince okunur
    durum.classList.toggle("calisiyor", mesgul && asama !== "onay");
    gonder.disabled = mesgul;
    durBtn.hidden = !mesgul;
  }

  function asamaYap(yeni) {
    asama = yeni;
    sonCikti = Date.now();
    durumYaz();
  }

  function mesgulYap(deger) {
    mesgul = deger;
    if (deger && !sayac) {
      asama = "model";
      sonCikti = Date.now();
      sayac = setInterval(durumYaz, 1000);
    } else if (!deger && sayac) {
      clearInterval(sayac);
      sayac = null;
    }
    durumYaz();
  }

  function akisKapat() {
    dusunce = null;
    icerik = null;
  }

  function farkOlustur(fark) {
    const pre = ogeOlustur("pre", "fark");
    const satirlar = (fark || "").split("\n");
    satirlar.slice(0, 400).forEach((satir) => {
      let sinif = "";
      if (satir.startsWith("+") && !satir.startsWith("+++")) sinif = "ekle";
      else if (satir.startsWith("-") && !satir.startsWith("---")) sinif = "sil";
      else if (satir.startsWith("@@")) sinif = "konum";
      pre.appendChild(ogeOlustur("div", sinif, satir || " "));
    });
    if (satirlar.length > 400) pre.appendChild(ogeOlustur("div", "konum", L(`… ${satirlar.length - 400} satır daha`, `… ${satirlar.length - 400} more lines`)));
    return pre;
  }

  function kartOlustur(baslik) {
    const kart = ogeOlustur("section", "kart");
    kart.appendChild(ogeOlustur("div", "kart-baslik", baslik));
    return kart;
  }

  function onayGoster(olay) {
    const kart = sonKart || ekle(kartOlustur(olay.soru));
    const dugmeler = ogeOlustur("div", "dugmeler");
    const secenekler = [
      ["e", kart.dataset.tur === "komut" ? L("Çalıştır", "Run")
        : kart.dataset.tur === "degisiklik" ? L("Uygula", "Apply") : L("İzin ver", "Allow"), ""],
      ["h", L("Reddet", "Reject"), "ikincil"],
      ["t", L("Bu sohbette hep izin ver", "Always allow in this chat"), "ikincil"],
    ];
    // Riskli işlemde "hep izin ver" sunulmaz: ajan bunu yalnız tek seferlik onay sayar.
    secenekler.filter(([yanit]) => yanit !== "t" || olay.hep_izin !== false).forEach(([yanit, etiket, sinif]) => {
      const b = ogeOlustur("button", sinif, etiket);
      b.type = "button";
      b.addEventListener("click", () => {
        vscode.postMessage({ tur: "onay", id: olay.id, yanit });
        asamaYap(yanit !== "h" && kart.dataset.tur === "komut" ? "komut" : "model");
        dugmeler.replaceChildren(ogeOlustur("span", "karar",
          yanit === "h" ? L("Reddedildi", "Rejected")
            : yanit === "t" ? L("Bu sohbette izin verildi", "Allowed for this chat") : L("Onaylandı", "Approved")));
      });
      dugmeler.appendChild(b);
    });
    kart.appendChild(dugmeler);
    sonKart = null; // sonraki onay eski karta yapışmasın
    kaydir();
  }

  function onaylariKapat() {
    akis.querySelectorAll(".dugmeler button").forEach((b) => { b.disabled = true; });
  }

  const DURUMLAR = DIL === "tr" ? { A: "eklendi", M: "değişti", D: "silindi" } : { A: "added", M: "changed", D: "deleted" };

  function dosyaListesi(dosyalar) {
    const liste = ogeOlustur("ul", "dosyalar");
    dosyalar.slice(0, 30).forEach((f) => {
      liste.appendChild(ogeOlustur("li", "", `${f.yol} (${DURUMLAR[f.durum] || f.durum})`));
    });
    if (dosyalar.length > 30) liste.appendChild(ogeOlustur("li", "", L(`… ${dosyalar.length - 30} dosya daha`, `… ${dosyalar.length - 30} more files`)));
    return liste;
  }

  function geriKarti(baslik, dosyalar, nokta, dugmeYazisi) {
    const kart = ogeOlustur("section", "kart geri-kart");
    kart.dataset.nokta = nokta;
    kart.appendChild(ogeOlustur("div", "kart-baslik", baslik));
    kart.appendChild(dosyaListesi(dosyalar));
    const b = ogeOlustur("button", "ikincil geri-dugme", dugmeYazisi);
    b.type = "button";
    b.addEventListener("click", () => {
      if (!mesgul) vscode.postMessage({ tur: "geri_al", nokta, dosyalar, yazi: dugmeYazisi });
    });
    kart.appendChild(b);
    return ekle(kart);
  }

  function isle(olay) {
    switch (olay.tur) {
      case "temizle":
        akis.replaceChildren();
        akisKapat();
        sonKart = null;
        mesgulYap(false);
        break;
      case "hazir":
      case "sifirlandi":
      case "mesaj_bitti":
        if (olay.tur === "mesaj_bitti") akisKapat();
        break;
      case "kullanici":
        akisKapat();
        ekle(ogeOlustur("div", "kullanici", olay.metin));
        mesgulYap(true);
        break;
      case "dusunce":
        if (!dusunce) {
          const d = ogeOlustur("details", "dusunce");
          d.appendChild(ogeOlustur("summary", "", L("Düşünüyor", "Thinking")));
          dusunce = ogeOlustur("div", "dusunce-metin");
          d.appendChild(dusunce);
          ekle(d);
          icerik = null;
        }
        dusunce.textContent += olay.metin;
        kaydir();
        break;
      case "icerik":
        if (!icerik) {
          icerik = ekle(ogeOlustur("div", "ajan"));
          dusunce = null;
        }
        icerik.textContent += olay.metin;
        kaydir();
        break;
      case "ara_not":
        // Arac cagrisindan onceki not (cogu zaman Ingilizce ic ses): sohbet balonu degil, kapali "Düşünüyor".
        if (icerik) {
          const onceki = icerik.previousElementSibling;
          if (onceki && onceki.tagName === "DETAILS" && onceki.className === "dusunce") {
            onceki.lastChild.textContent += "\n" + icerik.textContent;
            icerik.remove();
          } else {
            const d = ogeOlustur("details", "dusunce");
            d.appendChild(ogeOlustur("summary", "", L("Düşünüyor", "Thinking")));
            d.appendChild(ogeOlustur("div", "dusunce-metin", icerik.textContent));
            icerik.replaceWith(d);
          }
          icerik = null;
        }
        break;
      case "arac": {
        akisKapat();
        const hedef = (olay.arg && (olay.arg.path || olay.arg.pattern || olay.arg.query)) || "";
        const adlar = DIL === "tr"
          ? { read_file: "Okundu", list_files: "Listelendi", search_text: "Arandı", search_code: "Projede arandı" }
          : { read_file: "Read", list_files: "Listed", search_text: "Searched", search_code: "Searched the project" };
        ekle(ogeOlustur("div", "arac", `${adlar[olay.ad] || olay.ad}: ${hedef || "."}`));
        break;
      }
      case "komut":
        akisKapat();
        sonKart = kartOlustur(L("Komut", "Command"));
        sonKart.dataset.tur = "komut";
        sonKart.appendChild(ogeOlustur("pre", "komut", olay.komut));
        ekle(sonKart);
        break;
      case "degisiklik": {
        akisKapat();
        sonKart = kartOlustur(olay.yol);
        sonKart.dataset.tur = "degisiklik";
        const ac = ogeOlustur("button", "bag", L("Editörde karşılaştır", "Compare in editor"));
        ac.type = "button";
        ac.addEventListener("click", () => vscode.postMessage({ tur: "fark" }));
        sonKart.appendChild(ac);
        sonKart.appendChild(farkOlustur(olay.fark));
        ekle(sonKart);
        break;
      }
      case "onay":
        onayGoster(olay);
        break;
      case "sonuc": {
        akisKapat();
        const d = ogeOlustur("details", "sonuc");
        d.open = true;
        d.appendChild(ogeOlustur("summary", "", olay.ad === "run_command" ? L("Komut çıktısı", "Command output") : L("Sonuç", "Result")));
        d.appendChild(ogeOlustur("pre", "", olay.metin));
        ekle(d);
        sonKart = null;
        break;
      }
      case "uyari":
        akisKapat();
        ekle(ogeOlustur("div", "uyari", olay.metin));
        break;
      case "hata":
        akisKapat();
        ekle(ogeOlustur("div", "hata", olay.metin));
        break;
      case "surec_bitti":
        akisKapat();
        ekle(ogeOlustur("div", "hata", olay.metin));
        onaylariKapat();
        mesgulYap(false);
        break;
      case "tur_bitti":
        akisKapat();
        onaylariKapat();
        sonKart = null;
        mesgulYap(false);
        if (olay.nokta && olay.dosyalar && olay.dosyalar.length) {
          geriKarti(L(`Bu turda ${olay.dosyalar.length} dosya değişti`, `${olay.dosyalar.length} file(s) changed in this turn`),
            olay.dosyalar, olay.nokta, L("Bu turu geri al", "Undo this turn"));
        }
        girdi.focus();
        break;
      case "geri_alindi": {
        akis.querySelectorAll(".geri-kart").forEach((k) => {
          if (k.dataset.nokta === olay.nokta) {
            const b = k.querySelector(".geri-dugme");
            b.replaceWith(ogeOlustur("span", "karar", L("Geri alındı", "Undone")));
          }
        });
        if (olay.dosyalar && olay.dosyalar.length) {
          geriKarti(L(`${olay.dosyalar.length} dosya geri alındı`, `${olay.dosyalar.length} file(s) restored`),
            olay.dosyalar, olay.guvenlik, L("Yeniden uygula", "Reapply"));
        } else {
          ekle(ogeOlustur("div", "uyari", L("Geri alınacak bir değişiklik yoktu.", "There was nothing to undo.")));
        }
        break;
      }
      default:
        break;
    }
    // Gorunur her cikti sayaci sifirlar; onay bekleniyorsa veya komut calisiyorsa asama ona gore.
    if (mesgul && olay.tur !== "kullanici") {
      asamaYap(olay.tur === "onay" ? "onay" : olay.tur === "komut" ? "komut" : "model");
    }
  }

  window.addEventListener("message", (e) => isle(e.data));

  function gonderMesaj() {
    const metin = girdi.value.trim();
    if (!metin || mesgul) return;
    girdi.value = "";
    vscode.postMessage({ tur: "mesaj", metin });
  }

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    gonderMesaj();
  });
  girdi.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey && !e.isComposing) {
      e.preventDefault();
      gonderMesaj();
    }
  });
  durBtn.addEventListener("click", () => vscode.postMessage({ tur: "dur" }));

  durumYaz();
  vscode.postMessage({ tur: "acildi" });
  girdi.focus();
})();
