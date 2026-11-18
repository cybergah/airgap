import { useEffect, useRef, useState, type ReactNode } from "react";
import { X } from "lucide-react";
import { useT } from "../dil";
import { Kalkan } from "./Logo";

export type Ayar = {
  model: string;
  dusunme: string;
  maks_adim: number;
  baglam: number;
  korumali: boolean;
  korumali_imaj: string;
  dil: string;
};

function Pencere({ acik, kapat, baslik, children }: { acik: boolean; kapat: () => void; baslik: string; children: ReactNode }) {
  const ref = useRef<HTMLDialogElement>(null);
  const t = useT();
  useEffect(() => {
    const d = ref.current;
    if (!d) return;
    if (acik && !d.open) d.showModal();
    if (!acik && d.open) d.close();
  }, [acik]);
  return (
    <dialog
      ref={ref}
      onClose={kapat}
      onClick={(e) => { if (e.target === ref.current) kapat(); }}
      className="m-auto w-[min(460px,92vw)] animate-gir rounded-2xl border border-kenar bg-yuzey p-0 text-metin shadow-[0_30px_80px_-20px_rgb(0_0_0/0.9),0_0_0_1px_rgb(0_255_65/0.08)] backdrop:bg-black/60 backdrop:backdrop-blur-sm"
    >
      <div className="flex items-center gap-2.5 border-b border-kenar-2 px-5 py-3.5">
        <Kalkan boyut={18} />
        <h2 className="flex-1 text-[15px] font-semibold text-parlak">{baslik}</h2>
        <button type="button" onClick={kapat} className="rounded-md p-1 text-soluk transition hover:bg-yuzey-2 hover:text-metin" aria-label={t("kapat")}><X size={16} /></button>
      </div>
      <div className="px-5 py-4">{children}</div>
    </dialog>
  );
}

export function AyarPenceresi({ ayar, kapat, kaydet }: { ayar: Ayar | null; kapat: () => void; kaydet: (a: Partial<Ayar>) => void }) {
  const t = useT();
  const [taslak, setTaslak] = useState<Ayar | null>(ayar);
  useEffect(() => setTaslak(ayar), [ayar]);
  const alan = (ad: keyof Ayar, deger: string | number | boolean) => setTaslak((x) => (x ? { ...x, [ad]: deger } : x));
  return (
    <Pencere acik={!!ayar} kapat={kapat} baslik={t("ayarlar")}>
      {taslak && (
        <form
          className="space-y-4"
          onSubmit={(e) => {
            e.preventDefault();
            kaydet({ ...taslak, model: taslak.model.trim() || ayar!.model });
          }}
        >
          <Etiket ad={t("model")} ipucu={t("modelIpucu")}>
            <input className="girdi font-mono" value={taslak.model} onChange={(e) => alan("model", e.target.value)} />
          </Etiket>
          <div className="grid grid-cols-2 gap-3">
            <Etiket ad={t("dusunme")}>
              <select className="girdi" value={taslak.dusunme} onChange={(e) => alan("dusunme", e.target.value)}>
                <option value="">{t("varsayilan")}</option>
                <option value="low">{t("dusuk")}</option>
                <option value="medium">{t("orta")}</option>
                <option value="high">{t("yuksek")}</option>
                <option value="uyarlanir">{t("uyarlanir")}</option>
              </select>
            </Etiket>
            <Etiket ad={t("dilAyar")}>
              <select className="girdi" value={taslak.dil} onChange={(e) => alan("dil", e.target.value)}>
                <option value="">{t("dilOtomatik")}</option>
                <option value="tr">Türkçe</option>
                <option value="en">English</option>
              </select>
            </Etiket>
          </div>
          <div className="grid grid-cols-2 gap-3">
            <Etiket ad={t("maksAdim")}>
              <input className="girdi font-mono" type="number" min={1} value={taslak.maks_adim} onChange={(e) => alan("maks_adim", Number(e.target.value) || 1)} />
            </Etiket>
            <Etiket ad={t("baglam")}>
              <input className="girdi font-mono" type="number" min={2048} step={1024} value={taslak.baglam} onChange={(e) => alan("baglam", Number(e.target.value) || 2048)} />
            </Etiket>
          </div>
          <label className="flex cursor-pointer items-start gap-2.5 rounded-xl border border-kenar bg-derin/60 p-3 transition hover:border-vurgu/40">
            <input type="checkbox" className="mt-0.5 accent-[#00ff41]" checked={taslak.korumali} onChange={(e) => alan("korumali", e.target.checked)} />
            <span className="text-[13px]">
              {t("korumali")}
              <span className="mt-0.5 block text-xs text-soluk">{t("korumaliIpucu")}</span>
            </span>
          </label>
          {taslak.korumali && (
            <Etiket ad={t("imaj")}>
              <input className="girdi font-mono" value={taslak.korumali_imaj} onChange={(e) => alan("korumali_imaj", e.target.value)} />
            </Etiket>
          )}
          <div className="flex justify-end gap-2 pt-1">
            <button type="button" className="dugme" onClick={kapat}>{t("vazgec")}</button>
            <button type="submit" className="dugme-ana">{t("kaydet")}</button>
          </div>
        </form>
      )}
    </Pencere>
  );
}

function Etiket({ ad, ipucu, children }: { ad: string; ipucu?: string; children: ReactNode }) {
  return (
    <label className="block space-y-1.5">
      <span className="font-mono text-[11px] uppercase tracking-[0.12em] text-soluk">{ad}</span>
      {children}
      {ipucu && <span className="block text-xs text-soluk">{ipucu}</span>}
    </label>
  );
}

export function OnayPenceresi({ soru, kapat }: { soru: { baslik: string; ayrinti: string; dugme: string; evet: () => void } | null; kapat: () => void }) {
  const t = useT();
  return (
    <Pencere acik={!!soru} kapat={kapat} baslik={soru?.baslik ?? ""}>
      {soru && (
        <>
          <p className="whitespace-pre-wrap text-[13px] leading-relaxed text-soluk">{soru.ayrinti}</p>
          <div className="mt-5 flex justify-end gap-2">
            <button type="button" className="dugme" onClick={kapat}>{t("vazgec")}</button>
            <button type="button" className="dugme-ana" onClick={() => { soru.evet(); kapat(); }}>{soru.dugme}</button>
          </div>
        </>
      )}
    </Pencere>
  );
}
