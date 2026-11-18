import { useCallback, useEffect, useLayoutEffect, useReducer, useRef, useState } from "react";
import clsx from "clsx";
import { ArrowUp, CircleStop, Folder, FolderOpen, PanelLeftClose, PanelLeftOpen, Plus, Settings, Sparkles, WifiOff } from "lucide-react";
import { dinle, gonder, type Olay } from "./baglanti";
import { BASLANGIC, indirge, type Oge, type Onay, type OnayDurumu } from "./durum";
import { cevir, DilBaglami, sistemDili, type Dil } from "./dil";
import { Akis } from "./bilesenler/Akis";
import { AyarPenceresi, OnayPenceresi, type Ayar } from "./bilesenler/Pencereler";
import { Yazici, type YaziciRef } from "./bilesenler/Yazici";
import { Kalkan, Yazi } from "./bilesenler/Logo";

type Proje = { klasor: string; ad: string };
type Soru = { baslik: string; ayrinti: string; dugme: string; evet: () => void };
type Saglik = { ollama: boolean | null; surum?: string };
type Ceviri = (a: Parameters<typeof cevir>[1], d?: Record<string, string | number>) => string;

export function App() {
  const [durum, olayIsle] = useReducer(indirge, BASLANGIC);
  const [proje, setProje] = useState<Proje | null>(null);
  const [projeler, setProjeler] = useState<Proje[]>([]);
  const [model, setModel] = useState("");
  const [dilAyari, setDilAyari] = useState("");
  const [saglik, setSaglik] = useState<Saglik>({ ollama: null });
  const [bagli, setBagli] = useState(true);
  const [klasorYok, setKlasorYok] = useState(false);
  const [ayar, setAyar] = useState<Ayar | null>(null);
  const [soru, setSoru] = useState<Soru | null>(null);
  const [kenar, setKenar] = useState(() => window.innerWidth > 900);
  const [girdi, setGirdi] = useState("");
  const [dosyalar, setDosyalar] = useState<string[] | null>(null);
  const [, yenile] = useReducer((x: number) => x + 1, 0);
  const akisRef = useRef<HTMLDivElement>(null);
  const altta = useRef(true);
  const yaziciRef = useRef<YaziciRef>(null);
  const klasorRef = useRef<string | null>(null);

  const dil: Dil = dilAyari === "tr" || dilAyari === "en" ? dilAyari : sistemDili();
  const t: Ceviri = (a, d) => cevir(dil, a, d);

  const olay = useCallback((o: Olay) => {
    switch (o.tur) {
      case "klasor":
        if (klasorRef.current !== String(o.klasor)) setDosyalar(null); // baska proje: oneriler yeniden alinir
        klasorRef.current = String(o.klasor);
        setProje({ klasor: String(o.klasor), ad: String(o.ad) });
        setKlasorYok(false);
        return;
      case "klasor_yok":
        setProje(null);
        setKlasorYok(true);
        return;
      case "projeler":
        setProjeler(Array.isArray(o.liste) ? (o.liste as Proje[]) : []);
        return;
      case "dosyalar":
        if (String(o.klasor) === klasorRef.current) setDosyalar(Array.isArray(o.liste) ? (o.liste as string[]) : []);
        return;
      case "model":
        setModel(String(o.model));
        return;
      case "dil":
        setDilAyari(String(o.dil ?? ""));
        return;
      case "saglik":
        setSaglik({ ollama: Boolean(o.ollama), surum: o.surum ? String(o.surum) : undefined });
        return;
      case "ayarlar":
        setAyar(o.ayar as Ayar);
        return;
    }
    olayIsle(o);
  }, []);

  useEffect(() => dinle(olay, () => olayIsle({ tur: "_sifirla" }), setBagli), [olay]);
  useEffect(() => { document.title = proje ? `${proje.ad} · Airgap` : "Airgap"; }, [proje]);
  useEffect(() => { document.documentElement.lang = dil; }, [dil]);

  // Calisirken gecen sureyi gostermek icin saniyede bir yeniden ciz.
  useEffect(() => {
    if (!durum.mesgul) return;
    const z = setInterval(yenile, 1000);
    return () => clearInterval(z);
  }, [durum.mesgul]);

  // Kullanici asagidaysa yeni cikti geldikce asagida kal.
  useLayoutEffect(() => {
    const a = akisRef.current;
    if (a && altta.current) a.scrollTop = a.scrollHeight;
  }, [durum.ogeler]);

  const gonderMesaj = (metin = girdi) => {
    const m = metin.trim();
    if (!m || durum.mesgul) return;
    setGirdi("");
    altta.current = true;
    void gonder({ tur: "mesaj", metin: m });
  };

  const onayla = (onay: Onay, yanit: OnayDurumu) => {
    olayIsle({ tur: "_onayla", id: onay.id, yanit });
    void gonder({ tur: "onay", id: onay.id, yanit });
  };

  const geriAl = (o: Extract<Oge, { k: "geri" }>) => {
    if (durum.mesgul) return;
    const dugme = t(o.tip === "tur" ? "buTuruGeriAl" : "yenidenUygula");
    setSoru({
      baslik: `${dugme}?`,
      ayrinti:
        o.dosyalar.slice(0, 15).map((f) => `• ${f.yol}`).join("\n") +
        (o.dosyalar.length > 15 ? "\n" + t("dosyaDaha", { n: o.dosyalar.length - 15 }) : "") +
        "\n\n" + t("geriAlAyrinti"),
      dugme: t("devamEt"),
      evet: () => void gonder({ tur: "geri_al", nokta: o.nokta }),
    });
  };

  const yeniSohbet = () => {
    if (durum.mesgul) {
      setSoru({ baslik: t("yeniSohbet"), ayrinti: t("yeniSohbetSoru"), dugme: t("durdurBaslat"), evet: () => void gonder({ tur: "yeni" }) });
    } else void gonder({ tur: "yeni" });
  };

  const sn = Math.max(0, Math.floor((Date.now() - durum.sonCikti) / 1000));
  const durumYazisi = !durum.mesgul
    ? null
    : durum.asama === "onay"
      ? t("onayBekliyor")
      : durum.asama === "komut"
        ? t("komutCalisiyor", { sn })
        : sn >= 5 ? t("modelYaziyor", { sn }) : t("modelCalisiyor", { sn });
  const bos = durum.ogeler.length === 0;

  return (
    <DilBaglami.Provider value={dil}>
      <div className="flex h-full bg-zemin text-metin">
        {/* ------------------------------------------------ kenar cubugu */}
        <aside className={clsx("flex shrink-0 flex-col overflow-hidden border-r border-kenar-2 bg-derin transition-[width] duration-300 ease-out", kenar ? "w-[264px]" : "w-0 border-r-0")}>
          <div className="flex items-center gap-2.5 px-4 pb-4 pt-4">
            <Kalkan boyut={30} />
            <div className="leading-none">
              <Yazi className="text-[15px]" />
              <div className="mt-1 font-mono text-[10px] tracking-wide text-soluk">local · private · gated</div>
            </div>
          </div>
          <div className="px-3">
            <button type="button" onClick={yeniSohbet} disabled={!proje} className="dugme w-full justify-start">
              <Plus size={15} className="text-vurgu" />{t("yeniSohbet")}
            </button>
          </div>
          <div className="mt-6 flex items-center justify-between px-4 font-mono text-[10.5px] uppercase tracking-[0.16em] text-soluk">
            {t("projeler")}
            <button type="button" onClick={() => void gonder({ tur: "klasor_sec" })} className="rounded p-1 transition hover:bg-yuzey hover:text-vurgu" title={t("klasorAc")} aria-label={t("klasorAc")}>
              <FolderOpen size={14} />
            </button>
          </div>
          <nav className="mt-1.5 flex-1 space-y-0.5 overflow-y-auto px-2">
            {projeler.map((p) => {
              const secili = proje && p.klasor === proje.klasor;
              return (
                <button
                  key={p.klasor}
                  type="button"
                  title={p.klasor}
                  disabled={durum.mesgul && !secili}
                  onClick={() => !secili && void gonder({ tur: "klasor_ac", klasor: p.klasor })}
                  className={clsx(
                    "group relative flex w-full items-center gap-2 rounded-lg px-2.5 py-1.5 text-left text-[13px] transition disabled:opacity-40",
                    secili ? "bg-yuzey text-parlak" : "text-soluk hover:bg-yuzey/60 hover:text-metin",
                  )}
                >
                  {secili && <span className="absolute inset-y-1.5 left-0 w-[2px] rounded-full bg-vurgu shadow-[0_0_8px_#00ff41]" />}
                  <Folder size={14} className={secili ? "text-vurgu" : "opacity-70"} />
                  <span className="truncate">{p.ad}</span>
                </button>
              );
            })}
            {!projeler.length && <p className="px-2.5 py-2 text-xs text-soluk">{t("projeYok")}</p>}
          </nav>
          <div className="space-y-2.5 border-t border-kenar-2 p-3">
            <button type="button" onClick={() => void gonder({ tur: "ayar_al" })} className="flex w-full items-center gap-2 rounded-lg px-2.5 py-1.5 text-[13px] text-soluk transition hover:bg-yuzey hover:text-metin">
              <Settings size={15} />{t("ayarlar")}
            </button>
            <div className="flex flex-wrap gap-1.5 px-1">
              <span className="cip">● cloud: 0</span>
              <span className="cip">● api keys: 0</span>
              <span className="cip">● telemetry: 0</span>
            </div>
            <div className="flex items-center justify-between gap-2 px-1.5 font-mono text-[10.5px] text-soluk">
              <span className="truncate" title="model">{model}</span>
              <span className={clsx("flex shrink-0 items-center gap-1", saglik.ollama === false && "text-sil")} title={saglik.surum ? `ollama ${saglik.surum}` : undefined}>
                <span className={clsx("h-1.5 w-1.5 rounded-full", saglik.ollama ? "bg-vurgu shadow-[0_0_6px_#00ff41]" : saglik.ollama === false ? "bg-sil" : "bg-soluk")} />
                {saglik.ollama === false ? t("ollamaKapali") : t("ollamaAcik")}
              </span>
            </div>
          </div>
        </aside>

        {/* ------------------------------------------------ ana alan */}
        <main className="izgara relative flex min-w-0 flex-1 flex-col">
          <header className="flex h-12 shrink-0 items-center gap-2 border-b border-kenar-2 bg-zemin/70 px-3 backdrop-blur">
            <button type="button" onClick={() => setKenar(!kenar)} className="rounded-md p-1.5 text-soluk transition hover:bg-yuzey hover:text-metin" aria-label="sidebar">
              {kenar ? <PanelLeftClose size={17} /> : <PanelLeftOpen size={17} />}
            </button>
            {!kenar && <Kalkan boyut={20} />}
            <div className="min-w-0 truncate text-[13px]">
              <span className="font-medium text-parlak">{proje?.ad ?? t("klasorSecilmedi")}</span>
              {proje && <span className="ml-2 hidden font-mono text-[11px] text-soluk md:inline">{proje.klasor}</span>}
            </div>
            <span className="flex-1" />
            {!bagli && <span className="flex items-center gap-1 text-xs text-sil"><WifiOff size={13} />{t("baglantiKoptu")}</span>}
          </header>

          {saglik.ollama === false && (
            <div className="mx-auto mt-3 w-full max-w-3xl px-5">
              <div className="rounded-lg border border-sil/40 bg-sil/10 px-3 py-2 text-[13px] text-sil">{t("ollamaKapaliUyari")}</div>
            </div>
          )}

          <div ref={akisRef} className="flex-1 overflow-y-auto" onScroll={(e) => {
            const a = e.currentTarget;
            altta.current = a.scrollHeight - a.scrollTop - a.clientHeight < 120;
          }}>
            {bos ? (
              <Karsilama proje={proje} klasorYok={klasorYok} t={t} ornek={(m) => { setGirdi(m); yaziciRef.current?.odakla(); }} />
            ) : (
              <Akis ogeler={durum.ogeler} eylemler={{ onayla, geriAl, goster: (yol) => void gonder({ tur: "goster", yol }) }} mesgul={durum.mesgul} />
            )}
          </div>

          {/* ------------------------------------------------ yazma alani */}
          <div className="shrink-0 px-5 pb-4 pt-2">
            <form
              className={clsx(
                "cam mx-auto max-w-3xl rounded-2xl border border-kenar transition duration-200 focus-within:border-vurgu/60 focus-within:shadow-[0_0_0_4px_rgb(0_255_65/0.08),0_0_40px_-12px_rgb(0_255_65/0.45)]",
                durum.mesgul && durum.asama !== "onay" && "tarama",
              )}
              onSubmit={(e) => { e.preventDefault(); gonderMesaj(); }}
            >
              <Yazici
                ref={yaziciRef}
                deger={girdi}
                degistir={setGirdi}
                gonder={() => gonderMesaj()}
                kapali={!proje}
                yerTutucu={proje ? t("yerTutucu") : t("yerTutucuKlasor")}
                dosyalar={dosyalar}
                dosyaIste={() => void gonder({ tur: "dosya_listesi" })}
                altSatir={
                  <div className="flex items-center gap-2 px-3 pb-2.5 pt-1">
                    <span className={clsx("flex items-center gap-1.5 font-mono text-[11px]", durum.asama === "onay" && durum.mesgul ? "text-uyari" : durumYazisi ? "text-vurgu" : "text-soluk")}>
                      {durumYazisi && <span className={clsx("inline-block h-3 w-1.5", durum.asama === "onay" ? "bg-uyari" : "animate-imlec bg-vurgu")} />}
                      {durumYazisi ?? t("ipucu")}
                    </span>
                    <span className="flex-1" />
                    {durum.mesgul ? (
                      <button type="button" onClick={() => void gonder({ tur: "dur" })} className="dugme"><CircleStop size={15} className="text-sil" />{t("durdur")}</button>
                    ) : (
                      <button type="submit" disabled={!girdi.trim() || !proje} className="flex h-8 w-8 items-center justify-center rounded-full bg-vurgu text-derin shadow-[0_0_18px_-2px_rgb(0_255_65/0.7)] transition hover:scale-105 hover:bg-[#33ff67] disabled:scale-100 disabled:bg-kenar disabled:text-soluk disabled:shadow-none" aria-label={t("gonder")}>
                        <ArrowUp size={17} strokeWidth={2.5} />
                      </button>
                    )}
                  </div>
                }
              />
            </form>
          </div>
        </main>

        <AyarPenceresi ayar={ayar} kapat={() => setAyar(null)} kaydet={(a) => { void gonder({ tur: "ayar_kaydet", ayar: a }); setAyar(null); }} />
        <OnayPenceresi soru={soru} kapat={() => setSoru(null)} />
      </div>
    </DilBaglami.Provider>
  );
}

function Karsilama({ proje, klasorYok, ornek, t }: { proje: Proje | null; klasorYok: boolean; ornek: (m: string) => void; t: Ceviri }) {
  const ornekler = [t("ornek1"), t("ornek2"), t("ornek3")];
  return (
    <div className="flex min-h-full flex-col items-center justify-center px-6 py-10 text-center">
      <div className="relative mb-6 animate-yuzme">
        <div className="isinma absolute inset-0 -z-10 scale-150 rounded-full bg-vurgu/20 blur-3xl" />
        <Kalkan boyut={96} canli />
      </div>
      <Yazi className="yazi-parilti text-[34px]" />
      <p className="mt-2 font-mono text-[14px] text-vurgu">
        {t("slogan")}<span className="animate-imlec">_</span>
      </p>
      <p className="mt-2 font-mono text-[11.5px] text-soluk">$ {t("ozellikler")}</p>

      {proje ? (
        <>
          <h1 className="mt-10 text-[17px] font-semibold text-parlak">{t("karsilamaBaslik", { ad: proje.ad })}</h1>
          <p className="mt-1.5 max-w-md text-[13px] leading-relaxed text-soluk">{t("karsilamaAlt")}</p>
          <div className="mt-6 grid w-full max-w-2xl gap-2.5 sm:grid-cols-3">
            {ornekler.map((m, i) => (
              <button
                key={m}
                type="button"
                onClick={() => ornek(m)}
                style={{ animationDelay: `${120 + i * 70}ms` }}
                className="cam group animate-gir rounded-xl border border-kenar p-3.5 text-left text-[13px] leading-snug text-soluk transition duration-200 hover:-translate-y-0.5 hover:border-vurgu/50 hover:text-metin hover:shadow-[0_8px_30px_-12px_rgb(0_255_65/0.45)]"
              >
                <Sparkles size={14} className="mb-2 text-vurgu/70 transition group-hover:text-vurgu" />
                {m}
              </button>
            ))}
          </div>
        </>
      ) : (
        <>
          <h1 className="mt-10 text-[17px] font-semibold text-parlak">{t("klasorBaslik")}</h1>
          <p className="mt-1.5 max-w-md text-[13px] text-soluk">{klasorYok ? t("klasorAlt") : t("baglaniyor")}</p>
          <button type="button" onClick={() => void gonder({ tur: "klasor_sec" })} className="dugme-ana mt-6"><FolderOpen size={15} />{t("klasorSec")}</button>
        </>
      )}
    </div>
  );
}
