"use strict";
// Gerçek VS Code içinde çalışır: gerçek panel sayfası, gerçek fark sekmesi, gerçek ajan.py; yalnız model sahte.
const assert = require("assert");
const fs = require("fs");
const http = require("http");
const path = require("path");
const vscode = require("vscode");

function bekle(kosul, ad, sure = 30000) {
  return new Promise((coz, red) => {
    const bas = Date.now();
    const t = setInterval(() => {
      if (kosul()) { clearInterval(t); coz(); }
      else if (Date.now() - bas > sure) { clearInterval(t); red(new Error(`Zaman aşımı: ${ad}`)); }
    }, 50);
  });
}

async function secimiDene({ vscode, panel, belgeYolu, yanitEkle, adim }) {
  const v = vscode;
  const editor = await v.window.showTextDocument(await v.workspace.openTextDocument(v.Uri.file(belgeYolu)));
  const belge = editor.document;
  const asil = { girdi: v.window.showInputBox, bilgi: v.window.showInformationMessage };
  const secili = () => { editor.selection = new v.Selection(0, 0, 0, belge.lineAt(0).text.length); };
  const sekmeler = () => v.window.tabGroups.all.flatMap((g) => g.tabs).filter((s) => s.input instanceof v.TabInputTextDiff);
  const asilMetin = belge.getText();
  // "revert" odaktaki editöre gider ve pencere odaksızken çalışmayabilir; belgeyi doğrudan geri yükle.
  const geriYukle = async () => {
    const d = new v.WorkspaceEdit();
    d.replace(belge.uri, new v.Range(0, 0, belge.lineCount, 0), asilMetin);
    assert.ok(await v.workspace.applyEdit(d), "geri yüklenemedi");
    await belge.save();
    assert.strictEqual(belge.getText(), asilMetin, "geri yükleme");
  };
  const onizleme = {};
  let karar = "Uygula";
  let karardan_once = async () => {};
  v.window.showInputBox = async () => "iki yap";
  v.window.showInformationMessage = async (_m, ...d) => {
    if (d.length) {
      onizleme.sekme = sekmeler().at(-1);
      const bel = await v.workspace.openTextDocument(onizleme.sekme.input.modified);
      onizleme.metin = bel.getText();
      await karardan_once();
      return karar;
    }
    return undefined;
  };
  try {
    secili();
    yanitEkle({ message: { content: "```python\nx = 42\n```" }, done: true });
    karar = "Reddet";
    await panel.seciliDuzenle();
    assert.strictEqual(onizleme.metin.trim(), "x = 42", "fark sekmesi yanlış");
    assert.strictEqual(belge.getText().trim(), "x = 1", "reddedilince değişti");
    assert.strictEqual(sekmeler().filter((s) => s.input.modified.path === onizleme.sekme.input.modified.path).length, 0, "fark sekmesi kapanmadı");
    adim("seçim: reddedilince dosya değişmedi, fark sekmesi kapandı");

    await v.window.showTextDocument(belge);
    secili();
    yanitEkle({ message: { content: "x = 42" }, done: true });
    karar = "Uygula";
    await panel.seciliDuzenle();
    assert.strictEqual(belge.getText().trim(), "x = 42", "uygulanmadı");
    assert.ok(belge.isDirty, "düzenleme kaydedilmeden kalmalı");
    adim("seçim: uygulanınca editöre yazıldı, dosya kaydedilmedi");

    // "undo" odaktaki yere gider: kullanıcı gibi önce editöre odaklan, tek kez gönder, sonucu bekle.
    await v.window.showTextDocument(belge, { preview: false, preserveFocus: false });
    await v.commands.executeCommand("workbench.action.focusActiveEditorGroup");
    await new Promise((c) => setTimeout(c, 300));
    const oncekiOdak = v.window.state.focused;
    await v.commands.executeCommand("undo");
    await bekle(() => belge.getText().trim() === "x = 1", "Ctrl+Z", 5000).catch(() => {});
    if (belge.getText().trim() === "x = 1") {
      adim("seçim: Ctrl+Z ile geri alındı");
    } else if (oncekiOdak && v.window.state.focused) {
      assert.fail(`Ctrl+Z çalışmadı, pencere odaktaydı: ${belge.getText().trim()}`);
    } else {
      // Odaksız pencerede undo çoğunlukla çalışmıyor (4/4 ölçüldü); tuşa basan kullanıcıda bu durum olmaz.
      adim("ATLANDI seçim: Ctrl+Z denenemedi, pencere odakta değildi");
      await geriYukle();
    }

    await v.window.showTextDocument(belge);
    secili();
    yanitEkle({ message: { content: "x = 42" }, done: true });
    karardan_once = async () => {
      const araya = new v.WorkspaceEdit();
      araya.insert(belge.uri, new v.Position(0, 0), "# elle\n");
      await v.workspace.applyEdit(araya);
    };
    await panel.seciliDuzenle();
    assert.ok(!belge.getText().includes("x = 42"), "değişen dosyaya yazıldı");
    adim("seçim: dosya bu arada değişirse öneri uygulanmadı");
    karardan_once = async () => {};
    await geriYukle();

    await v.window.showTextDocument(belge);
    editor.selection = new v.Selection(0, 0, 0, 0);
    const satir = belge.lineAt(0).text;
    yanitEkle({ message: { content: `${satir}  # satir` }, done: true });
    await panel.seciliDuzenle();
    assert.ok(belge.lineAt(0).text.endsWith("# satir"), "seçimsiz satır düzenlenmedi");
    adim("seçim: seçim yokken bulunduğu satır düzenlendi");
    await geriYukle();

    const komutlar = await v.commands.getCommands(true);
    assert.ok(komutlar.includes("kodAjani.seciliDuzenle"));
  } finally {
    v.window.showInputBox = asil.girdi;
    v.window.showInformationMessage = asil.bilgi;
  }
}

async function run() {
  const adimlar = [];
  const sonucDosyasi = process.env.KOD_AJANI_SONUC;
  const adim = (m) => { adimlar.push(m); fs.writeFileSync(sonucDosyasi, JSON.stringify({ bitti: false, adimlar }, null, 1)); };
  const kok = vscode.workspace.workspaceFolders[0].uri.fsPath;
  const dosya = path.join(kok, "a.py");
  let yanitlar = [
    { message: { tool_calls: [{ function: { name: "edit_file", arguments: { path: "a.py", old_text: "x = 1", new_text: "x = 2" } } }] }, done: true },
    { message: { content: "bitti" }, done: true },
  ];
  const govdeler = [];
  const ollama = http.createServer((req, res) => {
    let govde = "";
    req.on("data", (p) => { govde += p; });
    req.on("end", () => {
      govdeler.push(govde);
      if (req.url === "/api/show") return res.end(JSON.stringify({ capabilities: ["tools"] }));
      res.end(JSON.stringify(yanitlar.shift() || { message: { content: "bitti" }, done: true }) + "\n");
    });
  });
  await new Promise((c) => ollama.listen(0, "127.0.0.1", c));
  process.env.OLLAMA_HOST = `127.0.0.1:${ollama.address().port}`;

  try {
    const eklenti = vscode.extensions.getExtension("yerel.kod-ajani");
    assert.ok(eklenti, "eklenti bulunamadı");
    const { panel } = await eklenti.activate();
    adim(`eklenti etkinleşti (kurulu paket kipi: ${Boolean(process.env.KOD_AJANI_KURULU_PAKET)}, yol: ${eklenti.extensionPath})`);

    await vscode.commands.executeCommand("kodAjani.panel.focus");
    await bekle(() => panel.view, "panel görünümü");
    adim("panel görünümü oluştu");
    await bekle(() => panel.sayfaAcildi, "panel sayfası (panel.js, CSP)");
    adim("panel sayfası yüklendi: panel.js gerçek webview ve CSP altında çalıştı");

    panel.webviewMesaji({ tur: "mesaj", metin: "düzelt" });
    await bekle(() => panel.gecmis.some((o) => o.tur === "onay"), "onay");
    adim("ajan başladı, onay istendi");

    await bekle(() => vscode.window.tabGroups.all.flatMap((g) => g.tabs)
      .some((s) => s.input instanceof vscode.TabInputTextDiff), "fark sekmesi");
    const sekme = vscode.window.tabGroups.all.flatMap((g) => g.tabs).find((s) => s.input instanceof vscode.TabInputTextDiff);
    assert.ok(sekme.label.includes("a.py"), sekme.label);
    const [sol, sag] = await Promise.all([
      vscode.workspace.openTextDocument(sekme.input.original),
      vscode.workspace.openTextDocument(sekme.input.modified),
    ]);
    assert.strictEqual(sol.getText().trim(), "x = 1");
    assert.strictEqual(sag.getText().trim(), "x = 2");
    adim(`fark sekmesi açıldı ve içeriği doğru: ${sekme.label}`);
    assert.strictEqual(fs.readFileSync(dosya, "utf8").trim(), "x = 1", "onaydan önce yazıldı");
    adim("onaydan önce dosya değişmedi");

    panel.webviewMesaji({ tur: "onay", id: panel.gecmis.find((o) => o.tur === "onay").id, yanit: "e" });
    await bekle(() => panel.gecmis.some((o) => o.tur === "tur_bitti"), "tur_bitti");
    assert.strictEqual(fs.readFileSync(dosya, "utf8").trim(), "x = 2");
    const bitti = panel.gecmis.find((o) => o.tur === "tur_bitti");
    assert.deepStrictEqual(bitti.dosyalar, [{ durum: "M", yol: "a.py" }]);
    adim("onaylanınca dosya değişti, tur değişen dosyayı bildirdi");

    const belge = await vscode.workspace.openTextDocument(vscode.Uri.file(dosya));
    assert.strictEqual(belge.getText().trim(), "x = 2");

    const asil = vscode.window.showWarningMessage;
    let modal = null;
    try {
      vscode.window.showWarningMessage = async (m, o, secenek) => { modal = { m, o }; return secenek; };
    } catch { /* API değiştirilemezse aşağıda ajana doğrudan gönderilir */ }
    // Test dosyası kurulu paketin dışındayken taklit eklentiye ulaşmaz; gerçek pencere tıklama bekler.
    if (vscode.window.showWarningMessage !== asil && !process.env.KOD_AJANI_KURULU_PAKET) {
      panel.webviewMesaji({ tur: "geri_al", nokta: bitti.nokta, dosyalar: bitti.dosyalar, yazi: "Bu turu geri al" });
      adim("geri alma onay akışı çağrıldı (modal pencere taklit edildi)");
    } else {
      panel.ajan.gonder({ tur: "geri_al", nokta: bitti.nokta });
      modal = null;
      adim("modal taklit edilemedi; geri alma doğrudan gönderildi");
    }
    await bekle(() => panel.gecmis.some((o) => o.tur === "geri_alindi"), "geri_alindi");
    assert.strictEqual(fs.readFileSync(dosya, "utf8").trim(), "x = 1");
    await bekle(async () => true, "yenileme", 100);
    adim("geri alındı: dosya eski haline döndü");
    if (modal) assert.ok(modal.o.detail.includes("a.py") && modal.o.modal === true);

    if (!process.env.KOD_AJANI_KURULU_PAKET) {
      await secimiDene({ vscode, panel, belgeYolu: dosya, yanitEkle: (y) => yanitlar.push(y), adim });
    }

    // Açık dosya ve seçim mesajla birlikte modele gider; panel neyin gittiğini gösterir.
    const ed = await vscode.window.showTextDocument(await vscode.workspace.openTextDocument(vscode.Uri.file(dosya)));
    ed.selection = new vscode.Selection(0, 0, 0, ed.document.lineAt(0).text.length);
    const onceki = panel.gecmis.filter((o) => o.tur === "tur_bitti").length;
    yanitlar.push({ message: { content: "tamam" }, done: true });
    panel.webviewMesaji({ tur: "mesaj", metin: "bu satır ne yapıyor" });
    await bekle(() => panel.gecmis.filter((o) => o.tur === "tur_bitti").length > onceki, "baglamli tur");
    const not = panel.gecmis.find((o) => o.tur === "baglam_eklendi");
    assert.ok(not && not.dosya === "a.py" && not.secim_bas === 1, JSON.stringify(not));
    assert.ok(govdeler.some((g) => g.includes("Open file: a.py") && g.includes("Selected lines 1-1")), "modele bağlam gitmedi");
    adim("bağlam: açık dosya ve seçim modele gitti, panel bildirdi");

    const kayit = () => panel.context.workspaceState.get("kodAjani.gecmis", []);
    await bekle(() => kayit().some((o) => o.tur === "kullanici" && o.metin === "bu satır ne yapıyor"), "sohbet kaydı", 5000);
    assert.ok(!kayit().some((o) => o.tur === "ayrac"), "ayraç kayda girmemeli");
    adim("kalıcı sohbet: tur sonunda panel geçmişi kaydedildi");

    panel.yeni();
    await bekle(() => panel.gecmis.length === 0 || panel.gecmis.every((o) => o.tur !== "degisiklik"), "yeni sohbet");
    await bekle(() => kayit().length === 0, "yeni sohbet kaydı sildi", 5000);
    adim("yeni sohbet paneli temizledi");

    fs.writeFileSync(sonucDosyasi, JSON.stringify({ bitti: true, gecti: true, adimlar }, null, 1));
  } catch (hata) {
    fs.writeFileSync(sonucDosyasi, JSON.stringify({ bitti: true, gecti: false, hata: String(hata && hata.stack || hata), adimlar }, null, 1));
    throw hata;
  } finally {
    ollama.close();
  }
}

module.exports = { run };
