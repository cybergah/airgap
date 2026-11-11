"use strict";
const cp = require("child_process");
const crypto = require("crypto");
const fs = require("fs");
const path = require("path");
const readline = require("readline");
const vscode = require("vscode");

const SEMA = "kod-ajani";

/** Arayüz dili: kodAjani.dil ayarı. Varsayılan İngilizce; "tr" Türkçe. Modele gidenler etkilenmez. */
function dil() {
  return vscode.workspace.getConfiguration("kodAjani").get("dil") === "tr" ? "tr" : "en";
}
const L = (tr, en) => (dil() === "tr" ? tr : en);

/** Fark görünümünün iki yüzü: dosyanın şimdiki hali ve modelin önerdiği hali. */
class FarkIcerigi {
  constructor() {
    this.metinler = new Map();
    this.sayac = 0;
  }
  provideTextDocumentContent(uri) {
    return this.metinler.get(uri.path) || "";
  }
  async goster(yol, eski, yeni) {
    this.sayac += 1;
    if (this.metinler.size > 40) this.metinler.clear();
    const taban = `/${this.sayac}`;
    const sol = vscode.Uri.from({ scheme: SEMA, path: `${taban}/su-an/${yol}` });
    const sag = vscode.Uri.from({ scheme: SEMA, path: `${taban}/oneri/${yol}` });
    this.metinler.set(sol.path, eski);
    this.metinler.set(sag.path, yeni);
    await vscode.commands.executeCommand("vscode.diff", sol, sag, L(`Airgap önerisi: ${yol}`, `Airgap suggestion: ${yol}`), {
      preview: true,
      preserveFocus: true,
    });
    return sag;
  }
  async kapat(sag) {
    const sekmeler = vscode.window.tabGroups.all.flatMap((g) => g.tabs).filter((s) =>
      s.input instanceof vscode.TabInputTextDiff && s.input.modified.path === sag.path);
    if (sekmeler.length) await vscode.window.tabGroups.close(sekmeler);
  }
}

/** ajan.py --sunucu sürecini yönetir; satır başına bir JSON konuşur. */
class AjanSureci {
  constructor(context, olayYaz, gunluk) {
    this.context = context;
    this.olayYaz = olayYaz;
    this.gunluk = gunluk;
    this.surec = null;
  }
  ayarlar() {
    const a = vscode.workspace.getConfiguration("kodAjani");
    return {
      model: a.get("model"),
      gomme: a.get("gommeModeli"),
      haritaButcesi: a.get("haritaButcesi") ?? 1000,
      korumali: a.get("korumaliCalistirma") === true,
      korumaliImaj: a.get("korumaliImaj") || "python:3.13-slim",
      python: a.get("python"),
      // Kurulu pakette ajan.py eklentinin içinde, geliştirmede bir üst klasördedir.
      ajan: a.get("ajanYolu") || [path.join(this.context.extensionPath, "ajan.py"),
        path.join(this.context.extensionPath, "..", "ajan.py")].find((y) => fs.existsSync(y)) || "ajan.py",
      baglam: a.get("baglam"),
      maksAdim: a.get("maksAdim"),
    };
  }
  baslat() {
    if (this.surec) return true;
    const klasor = vscode.workspace.workspaceFolders && vscode.workspace.workspaceFolders[0];
    if (!klasor || klasor.uri.scheme !== "file") {
      this.olayYaz({ tur: "hata", metin: L("Önce bir proje klasörü aç (Dosya > Klasör Aç).", "Open a project folder first (File > Open Folder).") });
      return false;
    }
    const a = this.ayarlar();
    if (!fs.existsSync(a.ajan)) {
      this.olayYaz({ tur: "hata", metin: L(`ajan.py bulunamadı: ${a.ajan}. kodAjani.ajanYolu ayarını kontrol et.`,
        `ajan.py not found: ${a.ajan}. Check the kodAjani.ajanYolu setting.`) });
      return false;
    }
    const argumanlar = ["-B", a.ajan, "--sunucu", "--model", a.model, "--dizin", klasor.uri.fsPath,
      "--baglam", String(a.baglam), "--maks-adim", String(a.maksAdim)];
    if (a.gomme) argumanlar.push("--gomme-modeli", a.gomme);
    argumanlar.push("--harita-butce", String(a.haritaButcesi));
    if (a.korumali) argumanlar.push("--korumali", a.korumaliImaj);
    const surec = cp.spawn(a.python, argumanlar, {
      cwd: klasor.uri.fsPath,
      env: { ...process.env, PYTHONIOENCODING: "utf-8", PYTHONUTF8: "1", AIRGAP_LANG: dil() },
      stdio: ["pipe", "pipe", "pipe"],
      windowsHide: true,
    });
    this.surec = surec;
    surec.stdin.on("error", (hata) => this.gunluk.appendLine(`stdin: ${hata.message}`));
    surec.stderr.setEncoding("utf8");
    surec.stderr.on("data", (veri) => this.gunluk.append(veri));
    readline.createInterface({ input: surec.stdout }).on("line", (satir) => {
      try {
        this.olayYaz(JSON.parse(satir));
      } catch {
        this.gunluk.appendLine(L(`Çözülemeyen satır: ${satir}`, `Could not parse line: ${satir}`));
      }
    });
    const bitti = (metin) => {
      if (this.surec !== surec) return;
      this.surec = null;
      this.olayYaz({ tur: "surec_bitti", metin });
    };
    surec.on("error", (hata) => bitti(L(`Ajan başlatılamadı (${a.python}): ${hata.message}`, `Could not start the agent (${a.python}): ${hata.message}`)));
    surec.on("exit", (kod) => bitti(L(`Ajan süreci kapandı (kod ${kod}). Ayrıntı: Çıktı > Airgap.`,
      `The agent process exited (code ${kod}). Details: Output > Airgap.`)));
    return true;
  }
  gonder(komut) {
    if (!this.baslat()) return false;
    this.surec.stdin.write(JSON.stringify(komut) + "\n");
    return true;
  }
  kapat() {
    const surec = this.surec;
    this.surec = null;
    if (surec) surec.stdin.end();
  }
}

class SohbetPaneli {
  constructor(context) {
    this.context = context;
    this.view = null;
    this.gecmis = [];
    this.fark = new FarkIcerigi();
    this.sonFark = null;
    this.mesgul = false;
    this.secimler = new Map();
    this.secimSayac = 0;
    this.secimSuruyor = false;
    this.gunluk = vscode.window.createOutputChannel("Airgap");
    this.ajan = new AjanSureci(context, (olay) => this.olay(olay), this.gunluk);
    context.subscriptions.push(
      vscode.workspace.registerTextDocumentContentProvider(SEMA, this.fark),
      this.gunluk,
      { dispose: () => this.ajan.kapat() },
      vscode.workspace.onDidChangeConfiguration((d) => {
        if (d.affectsConfiguration("kodAjani")) {
          this.ajan.kapat();
          this.webviewYaz({ tur: "uyari", metin: L("Ayarlar değişti; ajan bir sonraki mesajda yeni ayarlarla başlar, sohbet sıfırlandı.",
            "Settings changed: the agent restarts with the new settings on your next message, and the chat was reset.") });
          this.webviewYaz({ tur: "tur_bitti", basarili: false });
          if (d.affectsConfiguration("kodAjani.dil") && this.view) this.view.webview.html = this.html();
        }
      })
    );
  }

  webviewYaz(olay) {
    this.gecmis.push(olay);
    if (this.gecmis.length > 5000) this.gecmis = this.gecmis.slice(-4000);
    if (this.view) this.view.webview.postMessage(olay);
  }

  olay(olay) {
    if (olay.tur === "secim_sonuc") {
      const bekleyen = this.secimler.get(olay.id);
      this.secimler.delete(olay.id);
      if (bekleyen) bekleyen(olay);
      return;
    }
    if (olay.tur === "tur_bitti") this.mesgul = false;
    if (olay.tur === "surec_bitti") {
      this.mesgul = false;
      for (const bekleyen of this.secimler.values()) bekleyen({ hata: olay.metin });
      this.secimler.clear();
    }
    if (olay.tur === "degisiklik") {
      this.sonFark = olay;
      this.fark.goster(olay.yol, olay.eski, olay.yeni).catch((h) => this.gunluk.appendLine(String(h)));
      const { eski, yeni, ...ozet } = olay; // tam metinler panele gerekmiyor
      this.webviewYaz(ozet);
      return;
    }
    this.webviewYaz(olay);
  }

  resolveWebviewView(view) {
    this.view = view;
    view.webview.options = { enableScripts: true };
    view.webview.html = this.html();
    view.onDidDispose(() => { this.view = null; });
    view.webview.onDidReceiveMessage((m) => this.webviewMesaji(m));
  }

  webviewMesaji(m) {
    switch (m.tur) {
      case "acildi":
        this.sayfaAcildi = true;
        for (const olay of this.gecmis) this.view.webview.postMessage(olay);
        break;
      case "mesaj":
        this.webviewYaz({ tur: "kullanici", metin: m.metin });
        this.mesgul = true;
        if (!this.ajan.gonder({ tur: "mesaj", metin: m.metin })) {
          this.mesgul = false;
          this.webviewYaz({ tur: "tur_bitti", basarili: false });
        }
        break;
      case "onay":
        this.ajan.gonder({ tur: "onay", id: m.id, yanit: m.yanit });
        break;
      case "dur":
        this.ajan.gonder({ tur: "dur" });
        break;
      case "fark":
        if (this.sonFark) this.fark.goster(this.sonFark.yol, this.sonFark.eski, this.sonFark.yeni);
        break;
      case "geri_al":
        this.geriAlSor(m).catch((h) => this.gunluk.appendLine(String(h)));
        break;
      default:
        break;
    }
  }

  /** Ctrl+Alt+K: seçimi (seçim yoksa satırı) modele düzenletir; onaysız hiçbir şey yazılmaz. */
  async seciliDuzenle() {
    const editor = vscode.window.activeTextEditor;
    if (!editor) return void vscode.window.showInformationMessage(L("Önce bir dosya aç ve kod seç.", "Open a file and select some code first."));
    if (this.mesgul || this.secimSuruyor) {
      return void vscode.window.showInformationMessage(L("Ajan şu an çalışıyor; bitince yeniden dene.", "The agent is busy; try again when it finishes."));
    }
    const belge = editor.document;
    const aralik = editor.selection.isEmpty ? belge.lineAt(editor.selection.active.line).range : editor.selection;
    const secim = belge.getText(aralik);
    if (!secim.trim()) return void vscode.window.showInformationMessage(L("Düzenlenecek kod yok: önce kod seç.", "Nothing to edit: select some code first."));
    const istek = await vscode.window.showInputBox({
      title: L("Airgap: seçili kodu düzenle", "Airgap: edit selection"),
      prompt: L("Bu kodda ne değişsin?", "What should change in this code?"),
      placeHolder: L("Örn: hata kontrolü ekle", "e.g. add error handling"),
    });
    if (!istek || !istek.trim()) return;

    this.secimSuruyor = true;
    let sonuc;
    try {
      const surum = belge.version;
      const once = belge.getText(new vscode.Range(new vscode.Position(0, 0), aralik.start));
      const sonra = belge.getText(new vscode.Range(aralik.end, belge.positionAt(belge.getText().length)));
      this.secimSayac += 1;
      const id = this.secimSayac;
      sonuc = await vscode.window.withProgress(
        { location: vscode.ProgressLocation.Notification, title: L("Airgap düzenliyor…", "Airgap is editing…"), cancellable: true },
        (_ilerleme, iptal) => new Promise((coz) => {
          this.secimler.set(id, coz);
          iptal.onCancellationRequested(() => this.ajan.surec && this.ajan.gonder({ tur: "dur" }));
          const gitti = this.ajan.gonder({
            tur: "secim", id, istek, secim, once, sonra,
            yol: vscode.workspace.asRelativePath(belge.uri), dil: belge.languageId,
          });
          if (!gitti) {
            this.secimler.delete(id);
            coz({ iptal: true });
          }
        })
      );
      if (sonuc.iptal) return;
      if (sonuc.hata) return void vscode.window.showErrorMessage(`Airgap: ${sonuc.hata}`);
      if (sonuc.yeni === secim) return void vscode.window.showInformationMessage(L("Model bir değişiklik önermedi.", "The model suggested no change."));

      const ad = path.basename(belge.fileName) || "secim";
      const sag = await this.fark.goster(ad, belge.getText(), once + sonuc.yeni + sonra);
      const uygula = L("Uygula", "Apply");
      const karar = await vscode.window.showInformationMessage(
        L(`Öneriyi ${ad} dosyasına uygulayayım mı?`, `Apply the suggestion to ${ad}?`), uygula, L("Reddet", "Reject"));
      await this.fark.kapat(sag);
      if (karar !== uygula) return;
      if (belge.version !== surum) {
        return void vscode.window.showWarningMessage(L("Dosya bu arada değişti, öneri uygulanmadı. Yeniden dene.",
          "The file changed in the meantime, so the suggestion was not applied. Try again."));
      }
      const duzenleme = new vscode.WorkspaceEdit();
      duzenleme.replace(belge.uri, aralik, sonuc.yeni);
      if (!(await vscode.workspace.applyEdit(duzenleme))) {
        return void vscode.window.showErrorMessage(L("Airgap: düzenleme uygulanamadı.", "Airgap: the edit could not be applied."));
      }
      await vscode.window.showTextDocument(belge, editor.viewColumn);
    } finally {
      this.secimSuruyor = false;
    }
  }

  async geriAlSor(m) {
    const dosyalar = (m.dosyalar || []).slice(0, 15).map((f) => `• ${f.yol}`).join("\n");
    const fazla = (m.dosyalar || []).length > 15
      ? L(`\n… ve ${m.dosyalar.length - 15} dosya daha`, `\n… and ${m.dosyalar.length - 15} more files`) : "";
    const detail = `${dosyalar}${fazla}\n\n` + L("Bu andan sonra bu dosyalarda elle yaptığın değişiklikler de geri alınır, " +
      "ama kayıt altında kalır: açılan \"Yeniden uygula\" düğmesiyle geri dönebilirsin.",
      "Changes you made by hand in these files since then are undone as well, but they stay recorded: " +
      "you can go back with the \"Reapply\" button that appears.");
    const devam = L("Devam et", "Continue");
    const secim = await vscode.window.showWarningMessage(`${m.yazi}?`, { modal: true, detail }, devam);
    if (secim === devam) this.ajan.gonder({ tur: "geri_al", nokta: m.nokta });
  }

  yeni() {
    this.gecmis = [];
    this.sonFark = null;
    if (this.ajan.surec) this.ajan.gonder({ tur: "dur" }), this.ajan.gonder({ tur: "yeni" });
    if (this.view) this.view.webview.postMessage({ tur: "temizle" });
  }

  html() {
    const webview = this.view.webview;
    const nonce = crypto.randomBytes(16).toString("hex");
    const uri = (ad) => webview.asWebviewUri(vscode.Uri.joinPath(this.context.extensionUri, "media", ad));
    const model = vscode.workspace.getConfiguration("kodAjani").get("model");
    return `<!doctype html>
<html lang="${dil()}"><head><meta charset="utf-8">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src ${webview.cspSource}; script-src 'nonce-${nonce}';">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="${uri("panel.css")}"><title>Airgap</title></head>
<body data-model="${encodeURIComponent(model)}" data-dil="${dil()}">
<main id="akis" aria-live="polite"></main>
<form id="form">
  <textarea id="girdi" rows="3" placeholder="${L("Ne yapayım? (Enter gönderir, Shift+Enter yeni satır)", "What should I do? (Enter sends, Shift+Enter adds a line)")}" aria-label="${L("Mesaj", "Message")}"></textarea>
  <div class="alt"><span id="durum"></span><button id="dur" type="button" class="ikincil" hidden>${L("Durdur", "Stop")}</button><button id="gonder" type="submit">${L("Gönder", "Send")}</button></div>
</form>
<script nonce="${nonce}" src="${uri("panel.js")}"></script>
</body></html>`;
  }
}

function activate(context) {
  const panel = new SohbetPaneli(context);
  context.subscriptions.push(
    vscode.window.registerWebviewViewProvider("kodAjani.panel", panel, {
      webviewOptions: { retainContextWhenHidden: true },
    }),
    vscode.commands.registerCommand("kodAjani.yeni", () => panel.yeni()),
    vscode.commands.registerCommand("kodAjani.seciliDuzenle", () => panel.seciliDuzenle())
  );
  return { panel }; // gerçek VS Code testleri için
}

function deactivate() {}

module.exports = { activate, deactivate };
