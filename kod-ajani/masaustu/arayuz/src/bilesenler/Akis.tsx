import { useState, type ReactNode } from "react";
import clsx from "clsx";
import {
  AlertTriangle, Brain, Check, ChevronRight, CircleAlert, FileCode2, FilePen, FileSearch, FolderSearch, FolderTree, Paperclip,
  RotateCcw, Search, ShieldCheck, SquareTerminal, X,
} from "lucide-react";
import type { Oge, Onay, OnayDurumu } from "../durum";
import { useT, type Anahtar } from "../dil";
import { Markdown } from "./Markdown";
import { Fark } from "./Fark";
import { Kalkan } from "./Logo";

export type Eylemler = {
  onayla: (onay: Onay, yanit: OnayDurumu) => void;
  geriAl: (o: Extract<Oge, { k: "geri" }>) => void;
  goster: (yol: string) => void;
};

const ARAC: Record<string, { ad: Anahtar; simge: ReactNode }> = {
  read_file: { ad: "okudu", simge: <FileCode2 size={13} /> },
  open_file: { ad: "acti", simge: <FileCode2 size={13} /> },
  list_files: { ad: "listeledi", simge: <FolderTree size={13} /> },
  search_text: { ad: "aradi", simge: <Search size={13} /> },
  search_code: { ad: "projedeAradi", simge: <FileSearch size={13} /> },
};

/** Sohbet akisi: kullanici mesajlari balon, ajan adimlari solda yesil cizgiyle bagli bir zaman cizelgesi. */
export function Akis({ ogeler, eylemler, mesgul }: { ogeler: Oge[]; eylemler: Eylemler; mesgul: boolean }) {
  const satirlar: ReactNode[] = [];
  let i = 0;
  while (i < ogeler.length) {
    const o = ogeler[i];
    if (o.k === "arac") {
      const grup: Extract<Oge, { k: "arac" }>[] = [];
      while (i < ogeler.length && ogeler[i].k === "arac") grup.push(ogeler[i++] as Extract<Oge, { k: "arac" }>);
      satirlar.push(<AracGrubu key={grup[0].n} grup={grup} />);
      continue;
    }
    satirlar.push(<OgeSatiri key={o.n} o={o} eylemler={eylemler} />);
    i++;
  }
  return (
    <div className="mx-auto flex w-full max-w-3xl flex-col gap-3.5 px-5 py-7">
      {satirlar}
      {mesgul && ogeler[ogeler.length - 1]?.k === "kullanici" && <Bekliyor />}
    </div>
  );
}

function Bekliyor() {
  const t = useT();
  return (
    <Adim simge={<span className="h-2 w-2 animate-pulse rounded-full bg-vurgu shadow-[0_0_8px_#00ff41]" />}>
      <span className="font-mono text-[12.5px] text-vurgu">{t("dusunmeyeBasliyor")}<span className="animate-imlec">▍</span></span>
    </Adim>
  );
}

/** Zaman cizelgesinde bir adim: solda simge noktasi, altinda bir sonraki adima uzanan ince cizgi. */
function Adim({ simge, children, ton }: { simge: ReactNode; children: ReactNode; ton?: "uyari" | "hata" | "ajan" }) {
  return (
    <div className="group/adim relative flex animate-gir gap-3">
      <div className="relative flex w-6 shrink-0 justify-center">
        <span className="absolute -bottom-4 top-7 w-px bg-gradient-to-b from-kenar to-transparent" />
        <div
          className={clsx(
            "relative z-[1] mt-0.5 flex h-6 w-6 items-center justify-center rounded-full border",
            ton === "hata" ? "border-sil/50 bg-sil/10 text-sil"
              : ton === "uyari" ? "border-uyari/50 bg-uyari/10 text-uyari"
                : ton === "ajan" ? "border-vurgu/40 bg-derin text-vurgu shadow-[0_0_10px_-2px_rgb(0_255_65/0.5)]"
                  : "border-kenar bg-derin text-soluk",
          )}
        >
          {simge}
        </div>
      </div>
      <div className="min-w-0 flex-1">{children}</div>
    </div>
  );
}

function AracGrubu({ grup }: { grup: Extract<Oge, { k: "arac" }>[] }) {
  const t = useT();
  const [acik, setAcik] = useState(false);
  if (grup.length === 1) {
    const a = grup[0];
    const tur = ARAC[a.ad];
    return (
      <Adim simge={tur?.simge ?? <FileCode2 size={13} />}>
        <div className="truncate py-0.5 text-[13px] text-soluk">
          {tur ? t(tur.ad) : a.ad} <span className="font-mono text-[12px] text-metin/85">{a.hedef || "."}</span>
        </div>
      </Adim>
    );
  }
  const okunan = grup.filter((a) => a.ad === "read_file" || a.ad === "open_file").length;
  const aranan = grup.length - okunan;
  const ozet = [okunan && t("grupOkuma", { n: okunan }), aranan && t("grupArama", { n: aranan })].filter(Boolean).join(" · ");
  return (
    <Adim simge={<FileSearch size={13} />}>
      <button type="button" onClick={() => setAcik(!acik)} className="flex items-center gap-1 py-0.5 text-[13px] text-soluk transition hover:text-metin">
        <ChevronRight size={14} className={clsx("transition-transform duration-200", acik && "rotate-90")} />
        {ozet}
      </button>
      {acik && (
        <ul className="mt-1.5 animate-gir space-y-1 border-l border-kenar pl-3">
          {grup.map((a) => {
            const tur = ARAC[a.ad];
            return (
              <li key={a.n} className="flex items-center gap-1.5 truncate text-[12.5px] text-soluk">
                {tur?.simge}{tur ? t(tur.ad) : a.ad} <span className="truncate font-mono text-[11.5px] text-metin/85">{a.hedef || "."}</span>
              </li>
            );
          })}
        </ul>
      )}
    </Adim>
  );
}

function Dusunce({ metin }: { metin: string }) {
  const t = useT();
  const [acik, setAcik] = useState(false);
  if (!metin.trim()) return null;
  return (
    <Adim simge={<Brain size={13} />}>
      <button type="button" onClick={() => setAcik(!acik)} className="flex items-center gap-1 py-0.5 text-[13px] text-soluk transition hover:text-metin">
        <ChevronRight size={14} className={clsx("transition-transform duration-200", acik && "rotate-90")} />
        {t("dusundu")}
      </button>
      {acik && <div className="mt-1.5 animate-gir whitespace-pre-wrap border-l border-vurgu/30 pl-3 font-mono text-[12px] leading-relaxed text-soluk">{metin}</div>}
    </Adim>
  );
}

function OnayDugmeleri({ onay, tur, onayla }: { onay: Onay; tur: "komut" | "degisiklik" | "diger"; onayla: Eylemler["onayla"] }) {
  const t = useT();
  if (onay.durum !== "bekliyor") {
    const yazi = { e: t("onaylandi"), t: t("hepIzinVerildi"), h: t("reddedildi"), kapandi: t("yanitlanmadi"), bekliyor: "" }[onay.durum];
    return (
      <div className={clsx("flex items-center gap-1.5 border-t border-kenar-2 px-3 py-2 font-mono text-[11px]", onay.durum === "h" ? "text-sil" : onay.durum === "kapandi" ? "text-soluk" : "text-vurgu/90")}>
        {onay.durum === "h" ? <X size={12} /> : <Check size={12} />}{yazi}
      </div>
    );
  }
  const evet = tur === "komut" ? t("calistir") : tur === "degisiklik" ? t("uygula") : t("izinVer");
  return (
    <div className="flex flex-wrap items-center gap-2 border-t border-uyari/20 bg-uyari/[0.04] px-3 py-2.5">
      <button type="button" className="dugme-ana" onClick={() => onayla(onay, "e")}><Check size={14} strokeWidth={2.5} />{evet}</button>
      <button type="button" className="dugme" onClick={() => onayla(onay, "h")}><X size={14} />{t("reddet")}</button>
      {onay.hepIzin && (
        <button type="button" className="dugme" onClick={() => onayla(onay, "t")}><ShieldCheck size={14} />{t("hepIzin")}</button>
      )}
      <span className="ml-auto flex items-center gap-1.5 font-mono text-[11px] text-uyari">
        <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-uyari" />{t("onayBekliyor")}
      </span>
    </div>
  );
}

function Kart({ baslik, simge, children, bekliyor, ek }: { baslik: ReactNode; simge: ReactNode; children: ReactNode; bekliyor?: boolean; ek?: ReactNode }) {
  return (
    <div className={clsx("cam overflow-hidden rounded-xl border transition", bekliyor ? "nabiz border-uyari/60" : "border-kenar")}>
      <div className="flex items-center gap-2 border-b border-kenar-2 px-3 py-2 text-[13px] font-medium text-parlak">
        <span className="text-soluk">{simge}</span>
        <span className="min-w-0 flex-1 truncate">{baslik}</span>
        {ek}
      </div>
      {children}
    </div>
  );
}

function OgeSatiri({ o, eylemler }: { o: Oge; eylemler: Eylemler }) {
  const t = useT();
  switch (o.k) {
    case "kullanici":
      return (
        <div className="mt-2 flex animate-gir justify-end">
          <div className="max-w-[85%] whitespace-pre-wrap rounded-2xl rounded-br-md border border-vurgu/20 bg-balon px-4 py-2.5 text-[14.5px] leading-relaxed text-balon-metin shadow-[0_6px_24px_-14px_rgb(0_255_65/0.5)]">{o.metin}</div>
        </div>
      );
    case "dusunce":
      return <Dusunce metin={o.metin} />;
    case "ajan":
      return (
        <Adim simge={<Kalkan boyut={14} zemin={false} />} ton="ajan">
          <Markdown metin={o.metin} />
        </Adim>
      );
    case "komut":
      return (
        <Adim simge={<SquareTerminal size={13} />}>
          <Kart baslik={t("komut")} simge={<SquareTerminal size={14} />} bekliyor={o.onay?.durum === "bekliyor"}>
            <pre className="overflow-x-auto bg-kod px-3.5 py-3 font-mono text-[12.5px] leading-relaxed text-metin"><span className="select-none text-vurgu">$ </span>{o.komut}</pre>
            {o.onay && <OnayDugmeleri onay={o.onay} tur="komut" onayla={eylemler.onayla} />}
            {o.cikti !== undefined && <Cikti metin={o.cikti} />}
          </Kart>
        </Adim>
      );
    case "degisiklik":
      return (
        <Adim simge={<FilePen size={13} />}>
          <Kart
            baslik={<span className="font-mono text-[12.5px]">{o.yol}</span>}
            simge={<FilePen size={14} />}
            bekliyor={o.onay?.durum === "bekliyor"}
            ek={<GezgindeGoster yol={o.yol} goster={eylemler.goster} />}
          >
            <div className="p-2"><Fark fark={o.fark} /></div>
            {o.onay && <OnayDugmeleri onay={o.onay} tur="degisiklik" onayla={eylemler.onayla} />}
          </Kart>
        </Adim>
      );
    case "onay":
      return (
        <Adim simge={<ShieldCheck size={13} />}>
          <Kart baslik={o.onay.soru} simge={<ShieldCheck size={14} />} bekliyor={o.onay.durum === "bekliyor"}>
            <OnayDugmeleri onay={o.onay} tur="diger" onayla={eylemler.onayla} />
          </Kart>
        </Adim>
      );
    case "sonuc":
      return (
        <Adim simge={<SquareTerminal size={13} />}>
          <div className="cam overflow-hidden rounded-xl border border-kenar"><Cikti metin={o.metin} baslik={t("sonuc")} /></div>
        </Adim>
      );
    case "uyari":
      return <Adim simge={<AlertTriangle size={12} />} ton="uyari"><div className="py-0.5 text-[13px] text-uyari">{o.anahtar ? t(o.anahtar) : o.metin}</div></Adim>;
    case "hata":
      return <Adim simge={<CircleAlert size={12} />} ton="hata"><div className="py-0.5 text-[13px] text-sil">{o.anahtar ? t(o.anahtar) : o.metin}</div></Adim>;
    case "ayrac":
      return (
        <div className="my-4 flex items-center gap-3 font-mono text-[11px] text-soluk">
          <div className="h-px flex-1 bg-gradient-to-r from-transparent to-kenar" />{o.metin}<div className="h-px flex-1 bg-gradient-to-l from-transparent to-kenar" />
        </div>
      );
    case "baglam":
      return (
        <div className="-mt-1.5 flex justify-end gap-1.5 font-mono text-[11px] text-soluk">
          <Paperclip size={11} className="mt-0.5" />{o.parcalar.join(" · ")}
        </div>
      );
    case "geri":
      return (
        <Adim simge={<RotateCcw size={13} />}>
          <div className="cam rounded-xl border border-kenar px-3.5 py-3">
            <div className="mb-2 text-[13px] font-medium text-parlak">
              {t(o.tip === "tur" ? "turDegisti" : "geriAlindiBaslik", { n: o.dosyalar.length })}
            </div>
            <ul className="mb-2.5 space-y-0.5">
              {o.dosyalar.slice(0, 30).map((f) => (
                <li key={f.yol} className="flex items-center gap-2 font-mono text-[12px]">
                  <span className={clsx("w-4 text-center text-[11px] font-bold", f.durum === "A" ? "text-ekle" : f.durum === "D" ? "text-sil" : "text-uyari")}>{f.durum}</span>
                  <span className="min-w-0 flex-1 truncate">{f.yol}</span>
                  {f.durum !== "D" && <GezgindeGoster yol={f.yol} goster={eylemler.goster} />}
                </li>
              ))}
            </ul>
            {o.bitti ? (
              <span className="font-mono text-[11px] text-soluk">{t("geriAlindi")}</span>
            ) : (
              <button type="button" className="dugme" onClick={() => eylemler.geriAl(o)}>
                <RotateCcw size={13} />{t(o.tip === "tur" ? "buTuruGeriAl" : "yenidenUygula")}
              </button>
            )}
          </div>
        </Adim>
      );
    default:
      return null;
  }
}

function GezgindeGoster({ yol, goster }: { yol: string; goster: (yol: string) => void }) {
  const t = useT();
  return (
    <button type="button" onClick={() => goster(yol)} title={t("gezgindeGoster")} aria-label={t("gezgindeGoster")}
      className="rounded p-1 text-soluk transition hover:bg-yuzey-2 hover:text-vurgu">
      <FolderSearch size={13} />
    </button>
  );
}

function Cikti({ metin, baslik }: { metin: string; baslik?: string }) {
  const t = useT();
  const [acik, setAcik] = useState(true);
  const kod = /\[cikis kodu: (-?\d+)\]\s*$/.exec(metin)?.[1];
  return (
    <div className="border-t border-kenar-2 first:border-t-0">
      <button type="button" onClick={() => setAcik(!acik)} className="flex w-full items-center gap-1 px-3 py-1.5 font-mono text-[11px] text-soluk transition hover:text-metin">
        <ChevronRight size={13} className={clsx("transition-transform duration-200", acik && "rotate-90")} />
        {baslik ?? t("cikti")}
        {kod !== undefined && (
          <span className={clsx("ml-auto rounded px-1.5 py-px", kod === "0" ? "bg-ekle/15 text-ekle" : "bg-sil/15 text-sil")}>{t("cikis", { k: kod })}</span>
        )}
      </button>
      {acik && <pre className="max-h-72 overflow-auto bg-kod px-3.5 py-2.5 font-mono text-[12px] leading-relaxed text-metin/90">{metin.replace(/\n?\[cikis kodu: -?\d+\]\s*$/, "")}</pre>}
    </div>
  );
}
