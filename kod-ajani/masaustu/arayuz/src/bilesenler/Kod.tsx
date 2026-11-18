import { useEffect, useState } from "react";
import { Check, Copy } from "lucide-react";
import { renklendir } from "../renklendir";
import { useT } from "../dil";

/** Renklendirilmis kod blogu ve kopyala dugmesi. Parcalar React metni olarak basilir (HTML enjekte edilmez). */
export function KodBlogu({ kod, dil }: { kod: string; dil?: string }) {
  const [parcalar, setParcalar] = useState<{ icerik: string; renk?: string }[][] | null>(null);
  const [kopyalandi, setKopyalandi] = useState(false);
  const t = useT();

  useEffect(() => {
    let iptal = false;
    if (dil) {
      renklendir(kod, dil)
        .then((p) => { if (!iptal) setParcalar(p); })
        .catch(() => { if (!iptal) setParcalar(null); });
    }
    return () => { iptal = true; };
  }, [kod, dil]);

  const kopyala = async () => {
    try {
      await navigator.clipboard.writeText(kod);
      setKopyalandi(true);
      setTimeout(() => setKopyalandi(false), 1500);
    } catch { /* pano kapali */ }
  };

  return (
    <div className="group relative my-3 overflow-hidden rounded-lg border border-kenar-2 bg-kod">
      <div className="flex items-center justify-between border-b border-kenar px-3 py-1.5 text-xs text-soluk">
        <span className="font-mono">{dil || t("metin")}</span>
        <button type="button" onClick={kopyala} className="flex items-center gap-1 rounded px-1.5 py-0.5 transition hover:bg-yuzey-2 hover:text-vurgu" aria-label={t("kopyala")}>
          {kopyalandi ? <Check size={13} /> : <Copy size={13} />}
          {kopyalandi ? t("kopyalandi") : t("kopyala")}
        </button>
      </div>
      <pre className="overflow-x-auto px-3 py-2.5 font-mono text-[12.5px] leading-relaxed">
        <code>
          {parcalar
            ? parcalar.map((satir, i) => (
                <span key={i} className="block min-h-[1lh]">
                  {satir.map((p, j) => (
                    <span key={j} style={p.renk ? { color: p.renk } : undefined}>{p.icerik}</span>
                  ))}
                </span>
              ))
            : kod}
        </code>
      </pre>
    </div>
  );
}
