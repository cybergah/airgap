// Iki dilli arayuz (Airgap kurali: her gorunen metin Turkce ve Ingilizce). Dil ayarlardan; bossa sistem dili.
import { createContext, useContext } from "react";

export type Dil = "tr" | "en";

const METINLER = {
  slogan: ["kodun bu makineden hiç çıkmaz", "your code never leaves the machine"],
  ozellikler: ["yerel model · onaylı adımlar · docker kutusu", "local LLM · approval-gated · docker sandbox"],
  yeniSohbet: ["Yeni sohbet", "New chat"],
  projeler: ["Projeler", "Projects"],
  klasorAc: ["Klasör aç", "Open folder"],
  klasorSec: ["Klasör seç", "Choose folder"],
  projeYok: ["Henüz proje yok.", "No projects yet."],
  ayarlar: ["Ayarlar", "Settings"],
  klasorSecilmedi: ["Klasör seçilmedi", "No folder selected"],
  baglantiKoptu: ["Bağlantı koptu", "Disconnected"],
  karsilamaBaslik: ["{ad} üzerinde ne yapalım?", "What should we do in {ad}?"],
  karsilamaAlt: [
    "Ajan dosyaları okur, değişiklik önerir ve komut çalıştırır. Her değişiklik ve komut için onayını ister.",
    "The agent reads files, proposes edits and runs commands. It asks for your approval before every edit and command.",
  ],
  klasorBaslik: ["Bir proje klasörü seç", "Choose a project folder"],
  klasorAlt: ["Ajan yalnız seçtiğin klasörün içinde çalışır.", "The agent works only inside the folder you choose."],
  baglaniyor: ["Bağlanıyor…", "Connecting…"],
  ornek1: ["Bu proje ne işe yarıyor? Kısaca anlat.", "What does this project do? Explain briefly."],
  ornek2: ["Testleri çalıştır ve başarısız olanları düzelt.", "Run the tests and fix the failing ones."],
  ornek3: ["README dosyasını güncel koda göre yenile.", "Update the README to match the current code."],
  yerTutucu: ["Ne yapayım? Dosya eklemek için @ yaz", "What should I do? Type @ to attach a file"],
  yerTutucuKlasor: ["Önce bir proje klasörü seç", "Choose a project folder first"],
  ipucu: ["Enter gönderir · Shift+Enter yeni satır", "Enter to send · Shift+Enter for a new line"],
  gonder: ["Gönder", "Send"],
  durdur: ["Durdur", "Stop"],
  onayBekliyor: ["Onayını bekliyor", "Waiting for your approval"],
  komutCalisiyor: ["Komut çalışıyor · {sn} sn", "Running command · {sn}s"],
  modelYaziyor: ["Model yazıyor · {sn} sn", "Model is writing · {sn}s"],
  modelCalisiyor: ["Model düşünüyor · {sn} sn", "Model is thinking · {sn}s"],
  dusunmeyeBasliyor: ["Düşünmeye başlıyor…", "Starting to think…"],
  dusundu: ["Düşündü", "Thought"],
  okudu: ["Okudu", "Read"],
  acti: ["Açtı", "Opened"],
  listeledi: ["Listeledi", "Listed"],
  aradi: ["Aradı", "Searched"],
  projedeAradi: ["Projede aradı", "Searched project"],
  grupOkuma: ["{n} dosya okudu", "read {n} file|read {n} files"],
  grupArama: ["{n} arama yaptı", "ran {n} search|ran {n} searches"],
  komut: ["Komut", "Command"],
  cikti: ["Çıktı", "Output"],
  sonuc: ["Sonuç", "Result"],
  cikis: ["çıkış {k}", "exit {k}"],
  calistir: ["Çalıştır", "Run"],
  uygula: ["Uygula", "Apply"],
  izinVer: ["İzin ver", "Allow"],
  reddet: ["Reddet", "Reject"],
  hepIzin: ["Bu sohbette hep izin ver", "Always allow in this chat"],
  onaylandi: ["Onaylandı", "Approved"],
  hepIzinVerildi: ["Bu sohbette izin verildi", "Allowed for this chat"],
  reddedildi: ["Reddedildi", "Rejected"],
  yanitlanmadi: ["Yanıtlanmadı", "Not answered"],
  altAlta: ["Alt alta", "Unified"],
  yanYana: ["Yan yana", "Split"],
  satirDaha: ["… {n} satır daha", "… {n} more line|… {n} more lines"],
  dosyaDaha: ["… ve {n} dosya daha", "… and {n} more file|… and {n} more files"],
  turDegisti: ["Bu turda {n} dosya değişti", "{n} file changed in this turn|{n} files changed in this turn"],
  geriAlindiBaslik: ["{n} dosya geri alındı", "{n} file reverted|{n} files reverted"],
  buTuruGeriAl: ["Bu turu geri al", "Undo this turn"],
  yenidenUygula: ["Yeniden uygula", "Reapply"],
  geriAlindi: ["Geri alındı", "Reverted"],
  geriAlinacakYok: ["Geri alınacak bir değişiklik yoktu.", "There was nothing to undo."],
  geriAlinamadi: ["Geri alma yapılamadı.", "Undo failed."],
  geriAlAyrinti: [
    "Bu andan sonra bu dosyalarda elle yaptığın değişiklikler de geri alınır, ama kayıt altında kalır: açılan \"Yeniden uygula\" düğmesiyle geri dönebilirsin.",
    "Changes you made to these files by hand after this point are undone too, but they are kept: the \"Reapply\" button brings them back.",
  ],
  devamEt: ["Devam et", "Continue"],
  vazgec: ["Vazgeç", "Cancel"],
  kaydet: ["Kaydet", "Save"],
  kapat: ["Kapat", "Close"],
  yeniSohbetSoru: ["Ajan çalışıyor. Durdurup yeni sohbet başlatayım mı?", "The agent is working. Stop it and start a new chat?"],
  durdurBaslat: ["Durdur ve başlat", "Stop and start"],
  gezgindeGoster: ["Gezgin'de göster", "Show in Explorer"],
  kopyala: ["Kopyala", "Copy"],
  kopyalandi: ["Kopyalandı", "Copied"],
  metin: ["metin", "text"],
  dosyaEkle: ["Dosya ekle", "Attach file"],
  resim: ["[resim: {ad}]", "[image: {ad}]"],
  // ayarlar
  model: ["Model", "Model"],
  modelIpucu: ["Ollama'daki model adı, örneğin gpt-oss:20b", "Model name in Ollama, e.g. gpt-oss:20b"],
  dusunme: ["Düşünme seviyesi", "Reasoning effort"],
  dusunmeIpucu: ["Yüksek: daha dikkatli ama daha yavaş", "High: more careful but slower"],
  varsayilan: ["Modelin varsayılanı", "Model default"],
  dusuk: ["Düşük", "Low"],
  orta: ["Orta", "Medium"],
  yuksek: ["Yüksek", "High"],
  uyarlanir: ["İşe göre ayarla", "Adapt to the task"],
  maksAdim: ["En fazla adım", "Max steps"],
  baglam: ["Bağlam (belirteç)", "Context (tokens)"],
  korumali: ["Komutları Docker kutusunda çalıştır", "Run commands in a Docker sandbox"],
  korumaliIpucu: ["Ajanın komutları bilgisayarına değil, yalıtılmış bir kutuya erişir.", "The agent's commands reach an isolated container, not your computer."],
  imaj: ["Kutunun imajı", "Sandbox image"],
  dilAyar: ["Arayüz dili", "Interface language"],
  dilOtomatik: ["Sistem dili", "System language"],
  // durum
  ollamaAcik: ["ollama çalışıyor", "ollama online"],
  ollamaKapali: ["ollama kapalı", "ollama offline"],
  ollamaKapaliUyari: ["Ollama çalışmıyor. Ollama uygulamasını aç; ajan yerel modeli ona bağlanarak kullanır.", "Ollama is not running. Start the Ollama app; the agent uses the local model through it."],
} satisfies Record<string, readonly [string, string]>;

export type Anahtar = keyof typeof METINLER;

export function sistemDili(): Dil {
  return (navigator.language || "en").toLowerCase().startsWith("tr") ? "tr" : "en";
}

export function cevir(dil: Dil, anahtar: Anahtar, degerler: Record<string, string | number> = {}): string {
  let m: string = METINLER[anahtar][dil === "tr" ? 0 : 1];
  if (m.includes("|")) m = m.split("|")[Number(degerler.n) === 1 ? 0 : 1]; // "tekil|cogul"
  for (const [k, v] of Object.entries(degerler)) m = m.replaceAll(`{${k}}`, String(v));
  return m;
}

export const DilBaglami = createContext<Dil>("en");

export function useT() {
  const dil = useContext(DilBaglami);
  return (anahtar: Anahtar, degerler?: Record<string, string | number>) => cevir(dil, anahtar, degerler);
}
