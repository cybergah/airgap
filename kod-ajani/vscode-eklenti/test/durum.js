"use strict";
// panel.js'in durum satirini tarayicisiz dener: kucuk sahte DOM, sahte saat.
// Calistir: node kod-ajani/vscode-eklenti/test/durum.js
const assert = require("assert");
const fs = require("fs");
const path = require("path");
const vm = require("vm");

class Oge {
  constructor(etiket) {
    this.etiket = etiket;
    this.cocuklar = [];
    this.className = "";
    this.textContent = "";
    this.dataset = {};
    this.dinleyiciler = {};
    this.hidden = false;
    this.disabled = false;
    this.title = "";
    this.scrollHeight = 0;
    this.scrollTop = 0;
    this.clientHeight = 0;
    const o = this;
    this.classList = {
      toggle(ad, acik) {
        const s = new Set(o.className.split(" ").filter(Boolean));
        if (acik) s.add(ad); else s.delete(ad);
        o.className = [...s].join(" ");
      },
    };
  }
  get tagName() { return this.etiket.toUpperCase(); }
  get lastChild() { return this.cocuklar.at(-1) || null; }
  get previousElementSibling() {
    const k = this.parent ? this.parent.cocuklar : [];
    return k[k.indexOf(this) - 1] || null;
  }
  appendChild(c) { this.cocuklar.push(c); c.parent = this; return c; }
  replaceChildren(...c) { this.cocuklar = c; }
  replaceWith(yeni) {
    const k = this.parent.cocuklar;
    k[k.indexOf(this)] = yeni;
    yeni.parent = this.parent;
  }
  remove() { this.parent.cocuklar.splice(this.parent.cocuklar.indexOf(this), 1); }
  addEventListener(ad, f) { this.dinleyiciler[ad] = f; }
  focus() {}
  tumu() { return this.cocuklar.flatMap((c) => [c, ...c.tumu()]); }
  querySelectorAll(secici) {
    const [sinif, etiket] = secici.replace(".", "").split(" ");
    return this.tumu().filter((x) => x.etiket === etiket && x.parent && x.parent.className.split(" ").includes(sinif));
  }
  querySelector(secici) { return this.querySelectorAll(secici)[0] || null; }
}

const ogeler = Object.fromEntries(["akis", "girdi", "form", "durum", "gonder", "dur"].map((id) => [id, new Oge("div")]));
let saat = 1_000_000;
const zamanlayicilar = [];
const dinleyici = {};
const giden = [];
const ortam = {
  document: {
    getElementById: (id) => ogeler[id],
    createElement: (e) => new Oge(e),
    body: { dataset: { model: "gpt-oss%3A20b", dil: "tr" } },
  },
  window: { addEventListener: (ad, f) => { dinleyici[ad] = f; } },
  acquireVsCodeApi: () => ({ postMessage: (m) => giden.push(m) }),
  setInterval: (f) => { zamanlayicilar.push(f); return zamanlayicilar.length; },
  clearInterval: (n) => { zamanlayicilar[n - 1] = null; },
  Date: { now: () => saat },
  decodeURIComponent,
};
vm.runInNewContext(fs.readFileSync(path.join(__dirname, "..", "media", "panel.js"), "utf8"), ortam);

const gonder = (olay) => dinleyici.message({ data: olay });
const ilerle = (sn) => { saat += sn * 1000; zamanlayicilar.forEach((f) => f && f()); };
const durum = ogeler.durum;

assert.strictEqual(durum.textContent, "gpt-oss:20b", "bosta model adi");
gonder({ tur: "kullanici", metin: "yaz" });
assert.strictEqual(durum.textContent, "Model çalışıyor · 0 sn");
assert.ok(durum.className.includes("calisiyor"));
gonder({ tur: "dusunce", metin: "dusunuyorum" });
ilerle(3);
assert.strictEqual(durum.textContent, "Model çalışıyor · 3 sn");
ilerle(4);
assert.strictEqual(durum.textContent, "Model yazıyor · 7 sn", "uzun sessizlik");
assert.ok(durum.title.includes("tek seferde"), "ayrinti ipucunda");

gonder({ tur: "komut", komut: "python -m unittest" });
gonder({ tur: "onay", id: 1, soru: "?" });
assert.strictEqual(durum.textContent, "Onayını bekliyor");
assert.ok(!durum.className.includes("calisiyor"), "onay beklerken nokta yanip sonmez");
ilerle(30);
assert.strictEqual(durum.textContent, "Onayını bekliyor", "onayda sayac yok");

ogeler.akis.querySelector(".dugmeler button").dinleyiciler.click();
assert.strictEqual(JSON.stringify(giden.at(-1)), JSON.stringify({ tur: "onay", id: 1, yanit: "e" })); // nesne baska vm baglaminda
ilerle(2);
assert.strictEqual(durum.textContent, "Komut çalışıyor · 2 sn");

gonder({ tur: "sonuc", ad: "run_command", metin: "OK" });
assert.strictEqual(durum.textContent, "Model çalışıyor · 0 sn", "cikti sayaci sifirlar");

gonder({ tur: "degisiklik", ad: "edit_file", yol: "a.py", fark: "" });
gonder({ tur: "onay", id: 2, soru: "?" });
ogeler.akis.querySelectorAll(".dugmeler button")[1].dinleyiciler.click(); // Reddet
assert.strictEqual(durum.textContent, "Model çalışıyor · 0 sn", "red sonrasi model");

// Arac cagrisindan onceki not sohbet balonu olarak kalmaz, kapali "Düşünüyor" kutusuna gecer.
const balonlar = () => ogeler.akis.cocuklar.filter((o) => o.className === "ajan");
const dusunceler = () => ogeler.akis.cocuklar.filter((o) => o.className === "dusunce");
const oncekiDusunce = dusunceler().length;
gonder({ tur: "icerik", metin: "Maybe tests folder? Let's list." });
assert.strictEqual(balonlar().length, 1, "not once akar");
gonder({ tur: "ara_not" });
gonder({ tur: "mesaj_bitti" });
assert.strictEqual(balonlar().length, 0, "not sohbet balonunda kalmamali");
assert.strictEqual(dusunceler().length, oncekiDusunce + 1);
assert.ok(dusunceler().at(-1).lastChild.textContent.includes("Let's list."));
gonder({ tur: "dusunce", metin: "dusunce" });
gonder({ tur: "icerik", metin: "ikinci not" });
gonder({ tur: "ara_not" });
assert.strictEqual(dusunceler().length, oncekiDusunce + 2, "hemen onceki dusunce kutusuna eklenir");
assert.ok(dusunceler().at(-1).lastChild.textContent.endsWith("ikinci not"));
gonder({ tur: "icerik", metin: "Projede yalniz GOREV.md var." });
gonder({ tur: "mesaj_bitti" });
assert.strictEqual(balonlar().length, 1, "son cevap balonda kalir");

// Mesajla giden baglam panelde gosterilir.
const notlar = () => ogeler.akis.cocuklar.filter((o) => o.className === "baglam").map((o) => o.textContent);
gonder({ tur: "baglam_eklendi", dosya: "a.py", satir: 3, secim_bas: 2, secim_son: 5, anilan: ["hesap.py"] });
gonder({ tur: "baglam_eklendi", dosya: "a.py", satir: 3 });
gonder({ tur: "baglam_eklendi", anilan: ["x.py", "y.py"] });
gonder({ tur: "baglam_eklendi", dosya: "b.py", secim_bas: 4, secim_son: 4 });
assert.deepStrictEqual(notlar(), ["📎 a.py · satır 2–5 seçili · @hesap.py", "📎 a.py · satır 3", "📎 @x.py · @y.py", "📎 b.py · satır 4 seçili"]);

gonder({ tur: "tur_bitti", basarili: true });
assert.strictEqual(durum.textContent, "gpt-oss:20b");
assert.strictEqual(ogeler.gonder.disabled, false);
assert.ok(zamanlayicilar.every((f) => f === null), "tur bitince sayac durur");
// English is the default when the extension does not say otherwise.
{
  const o2 = Object.fromEntries(["akis", "girdi", "form", "durum", "gonder", "dur"].map((id) => [id, new Oge("div")]));
  const d2 = {};
  vm.runInNewContext(fs.readFileSync(path.join(__dirname, "..", "media", "panel.js"), "utf8"), {
    ...ortam,
    document: { ...ortam.document, getElementById: (id) => o2[id], body: { dataset: { model: "m" } } },
    window: { addEventListener: (ad, f) => { d2[ad] = f; } },
  });
  d2.message({ data: { tur: "kullanici", metin: "hi" } });
  assert.strictEqual(o2.durum.textContent, "Model working · 0 s");
  d2.message({ data: { tur: "komut", komut: "ls" } });
  d2.message({ data: { tur: "onay", id: 9, soru: "?" } });
  assert.strictEqual(o2.durum.textContent, "Waiting for your approval");
  const etiketler = o2.akis.querySelectorAll(".dugmeler button").map((b) => b.textContent);
  assert.deepStrictEqual(etiketler, ["Run", "Reject", "Always allow in this chat"]);
}
console.log("DURUM TESTI GECTI");
