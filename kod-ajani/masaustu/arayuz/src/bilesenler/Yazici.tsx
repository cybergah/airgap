import { forwardRef, useImperativeHandle, useMemo, useRef, useState, type ReactNode } from "react";
import clsx from "clsx";
import { FileCode2 } from "lucide-react";
import { useT } from "../dil";

type Ozellikler = {
  deger: string;
  degistir: (v: string) => void;
  gonder: () => void;
  kapali: boolean;
  yerTutucu: string;
  dosyalar: string[] | null;
  dosyaIste: () => void;
  altSatir: ReactNode;
};

export type YaziciRef = { odakla: () => void };

/** "@" ile dosya onerisi olan mesaj kutusu: ok tuslari ile secilir, Enter ya da Tab ile eklenir. */
export const Yazici = forwardRef<YaziciRef, Ozellikler>(function Yazici(
  { deger, degistir, gonder, kapali, yerTutucu, dosyalar, dosyaIste, altSatir },
  ref,
) {
  const alan = useRef<HTMLTextAreaElement>(null);
  const t = useT();
  const [imlec, setImlec] = useState(0);
  const [secili, setSecili] = useState(0);
  const [kapatildi, setKapatildi] = useState(false);
  useImperativeHandle(ref, () => ({ odakla: () => alan.current?.focus() }));

  const sorgu = useMemo(() => /(?:^|\s)@([\w./\\-]*)$/.exec(deger.slice(0, imlec))?.[1] ?? null, [deger, imlec]);

  const oneriler = useMemo(() => {
    if (sorgu === null || !dosyalar) return [];
    const q = sorgu.toLowerCase().replace(/\\/g, "/");
    const puanli = dosyalar
      .map((d) => {
        const k = d.toLowerCase();
        const ad = k.split("/").pop() ?? k;
        if (!q) return { d, p: d.split("/").length };
        if (ad.startsWith(q)) return { d, p: 0 + d.length / 1000 };
        if (ad.includes(q)) return { d, p: 1 + d.length / 1000 };
        if (k.includes(q)) return { d, p: 2 + d.length / 1000 };
        return null;
      })
      .filter((x): x is { d: string; p: number } => x !== null)
      .sort((a, b) => a.p - b.p);
    return puanli.slice(0, 8).map((x) => x.d);
  }, [sorgu, dosyalar]);

  const acik = sorgu !== null && !kapatildi && oneriler.length > 0;

  const ekle = (yol: string) => {
    const once = deger.slice(0, imlec).replace(/@([\w./\\-]*)$/, `@${yol} `);
    const yeni = once + deger.slice(imlec);
    degistir(yeni);
    requestAnimationFrame(() => {
      const a = alan.current;
      if (!a) return;
      a.focus();
      a.setSelectionRange(once.length, once.length);
      setImlec(once.length);
    });
  };

  return (
    <div className="relative">
      {acik && (
        <div className="cam absolute bottom-full left-0 right-0 mb-2 animate-gir overflow-hidden rounded-xl border border-kenar shadow-[0_18px_50px_-20px_rgb(0_0_0/0.9)]" role="listbox">
          <div className="border-b border-kenar-2 px-3 py-1.5 font-mono text-[10.5px] uppercase tracking-[0.16em] text-soluk">{t("dosyaEkle")}</div>
          {oneriler.map((d, i) => (
            <button
              key={d}
              type="button"
              role="option"
              aria-selected={i === secili}
              onMouseDown={(e) => { e.preventDefault(); ekle(d); }}
              onMouseEnter={() => setSecili(i)}
              className={clsx("flex w-full items-center gap-2 px-3 py-1.5 text-left text-[13px]", i === secili ? "bg-vurgu/10 text-parlak" : "text-soluk")}
            >
              <FileCode2 size={13} className={clsx("shrink-0", i === secili && "text-vurgu")} />
              <span className="truncate font-mono">
                <span className="text-metin">{d.split("/").pop()}</span>
                {d.includes("/") && <span className="ml-2 text-[11.5px] text-soluk">{d.slice(0, d.lastIndexOf("/"))}</span>}
              </span>
            </button>
          ))}
        </div>
      )}
      <textarea
        ref={alan}
        rows={1}
        value={deger}
        disabled={kapali}
        onChange={(e) => {
          degistir(e.target.value);
          setImlec(e.target.selectionStart ?? e.target.value.length);
          setSecili(0);
          setKapatildi(false);
          if (e.target.value.includes("@") && dosyalar === null) dosyaIste();
        }}
        onSelect={(e) => setImlec(e.currentTarget.selectionStart ?? 0)}
        onKeyDown={(e) => {
          if (acik) {
            if (e.key === "ArrowDown") { e.preventDefault(); setSecili((s) => (s + 1) % oneriler.length); return; }
            if (e.key === "ArrowUp") { e.preventDefault(); setSecili((s) => (s - 1 + oneriler.length) % oneriler.length); return; }
            if (e.key === "Enter" || e.key === "Tab") { e.preventDefault(); ekle(oneriler[Math.min(secili, oneriler.length - 1)]); return; }
            if (e.key === "Escape") { e.preventDefault(); setKapatildi(true); return; }
          }
          if (e.key === "Enter" && !e.shiftKey && !e.nativeEvent.isComposing) { e.preventDefault(); gonder(); }
        }}
        placeholder={yerTutucu}
        className="block max-h-60 min-h-[52px] w-full resize-none bg-transparent px-4 pb-1 pt-3.5 text-[14.5px] leading-relaxed outline-none [field-sizing:content] placeholder:text-soluk/70"
        aria-label="Mesaj"
      />
      {altSatir}
    </div>
  );
});
