"use strict";
// VS Code olmadan eklentinin yolu: gerçek extension.js + gerçek ajan.py + sahte Ollama.
const assert = require("assert");
const fs = require("fs");
const http = require("http");
const Module = require("module");
const os = require("os");
const path = require("path");

const kok = fs.mkdtempSync(path.join(os.tmpdir(), "kod-ajani-duman-"));
fs.writeFileSync(path.join(kok, "a.py"), "x = 1\n");

let cagrilar = [
  { message: { tool_calls: [{ function: { name: "edit_file", arguments: { path: "a.py", old_text: "x = 1", new_text: "x = 2" } } }] }, done: true },
  { message: { content: "bitti" }, done: true },
];
const ollama = http.createServer((req, res) => {
  let govde = "";
  req.on("data", (p) => { govde += p; });
  req.on("end", () => {
    if (req.url === "/api/show") return res.end(JSON.stringify({ capabilities: ["tools"] }));
    res.end(JSON.stringify(cagrilar.shift()) + "\n");
  });
});

let sorular = 0;
let modalYaniti = false;
process.env.KOD_AJANI_VERI = fs.mkdtempSync(path.join(os.tmpdir(), "kod-ajani-veri-"));
const farklar = [];
const paneldeki = [];
let saglayici;
let komutlar = {};
const vscodeTaklidi = {
  Uri: {
    from: (o) => o,
    joinPath: (u, ...p) => ({ path: [u.path, ...p].join("/") }),
  },
  workspace: {
    workspaceFolders: [{ uri: { scheme: "file", fsPath: kok } }],
    getConfiguration: () => ({ get: (k) => ({ model: "sahte", python: "python", ajanYolu: "", baglam: 4096, maksAdim: 5 }[k]) }),
    registerTextDocumentContentProvider: () => ({ dispose() {} }),
    onDidChangeConfiguration: () => ({ dispose() {} }),
  },
  window: {
    createOutputChannel: () => ({ append: (m) => process.stderr.write(m), appendLine: (m) => process.stderr.write(m + "\n"), dispose() {} }),
    registerWebviewViewProvider: (_id, s) => { saglayici = s; return { dispose() {} }; },
    showWarningMessage: async (_m, _o, secenek) => { sorular += 1; return modalYaniti ? secenek : undefined; },
  },
  commands: {
    registerCommand: (ad, f) => { komutlar[ad] = f; return { dispose() {} }; },
    executeCommand: async (ad, sol, sag, baslik) => { farklar.push({ ad, sol, sag, baslik }); },
  },
};
const asilYukle = Module._load;
Module._load = function (istek, ...r) {
  return istek === "vscode" ? vscodeTaklidi : asilYukle.call(this, istek, ...r);
};

function bekle(kosul, ad) {
  return new Promise((coz, red) => {
    const bas = Date.now();
    const t = setInterval(() => {
      if (kosul()) { clearInterval(t); coz(); }
      else if (Date.now() - bas > 20000) { clearInterval(t); red(new Error(`Zaman aşımı: ${ad}\n${JSON.stringify(paneldeki)}`)); }
    }, 25);
  });
}

ollama.listen(0, "127.0.0.1", async () => {
  process.env.OLLAMA_HOST = `127.0.0.1:${ollama.address().port}`;
  const baglam = { extensionPath: path.join(__dirname, ".."), extensionUri: { path: "/e" }, subscriptions: [] };
  require("../extension.js").activate(baglam);

  let gonder;
  const view = {
    webview: {
      cspSource: "vscode-webview:",
      asWebviewUri: (u) => u.path,
      postMessage: (m) => paneldeki.push(m),
      onDidReceiveMessage: (f) => { gonder = f; },
    },
    onDidDispose: () => {},
  };
  saglayici.resolveWebviewView(view);
  assert.ok(view.webview.html.includes("Content-Security-Policy"));

  try {
    gonder({ tur: "mesaj", metin: "düzelt" });
    await bekle(() => paneldeki.some((o) => o.tur === "onay"), "onay");

    const deg = paneldeki.find((o) => o.tur === "degisiklik");
    assert.ok(deg && deg.fark.includes("+x = 2"), "panelde fark yok");
    assert.strictEqual(deg.eski, undefined, "tam metin panele gitmemeli");
    assert.strictEqual(farklar.length, 1, "fark görünümü açılmadı");
    assert.strictEqual(farklar[0].ad, "vscode.diff");
    assert.strictEqual(saglayici.fark.provideTextDocumentContent(farklar[0].sag), "x = 2\n");
    assert.strictEqual(saglayici.fark.provideTextDocumentContent(farklar[0].sol), "x = 1\n");
    assert.strictEqual(fs.readFileSync(path.join(kok, "a.py"), "utf8"), "x = 1\n", "onaydan önce yazıldı");

    gonder({ tur: "onay", id: paneldeki.find((o) => o.tur === "onay").id, yanit: "e" });
    await bekle(() => paneldeki.some((o) => o.tur === "tur_bitti"), "tur_bitti");
    assert.strictEqual(fs.readFileSync(path.join(kok, "a.py"), "utf8").trim(), "x = 2");
    assert.ok(paneldeki.some((o) => o.tur === "icerik" && o.metin === "bitti"));

    const bitti = paneldeki.find((o) => o.tur === "tur_bitti");
    assert.deepStrictEqual(bitti.dosyalar, [{ durum: "M", yol: "a.py" }]);
    gonder({ tur: "geri_al", nokta: bitti.nokta, dosyalar: bitti.dosyalar, yazi: "Bu turu geri al" });
    await bekle(() => sorular === 1, "iptal sorusu");
    await new Promise((c) => setTimeout(c, 500));
    assert.strictEqual(fs.readFileSync(path.join(kok, "a.py"), "utf8").trim(), "x = 2", "iptal edilince geri alındı");

    modalYaniti = true;
    gonder({ tur: "geri_al", nokta: bitti.nokta, dosyalar: bitti.dosyalar, yazi: "Bu turu geri al" });
    await bekle(() => paneldeki.some((o) => o.tur === "geri_alindi"), "geri_alindi");
    assert.strictEqual(fs.readFileSync(path.join(kok, "a.py"), "utf8").trim(), "x = 1");

    komutlar["kodAjani.yeni"]();
    assert.ok(paneldeki.some((o) => o.tur === "temizle"));
    assert.strictEqual(saglayici.gecmis.length, 0);
    console.log("DUMAN TESTI GECTI");
    baglam.subscriptions.forEach((s) => s.dispose && s.dispose());
    ollama.close();
    setTimeout(() => process.exit(0), 300);
  } catch (hata) {
    console.error(hata);
    process.exit(1);
  }
});
