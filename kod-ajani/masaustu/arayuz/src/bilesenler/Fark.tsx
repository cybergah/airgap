import { useMemo, useState } from "react";
import { Columns2, Rows2 } from "lucide-react";
import clsx from "clsx";
import { useT } from "../dil";

type Satir = { tur: "ayni" | "ekle" | "sil" | "konum"; metin: string; eski?: number; yeni?: number };

/** Birlesik (unified) farki satir numarali satirlara cevirir. */
export function farkCoz(fark: string): Satir[] {
  const satirlar: Satir[] = [];
  let eski = 0;
  let yeni = 0;
  for (const s of fark.split("\n")) {
    if (s.startsWith("---") || s.startsWith("+++")) continue;
    const m = /^@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@(.*)$/.exec(s);
    if (m) {
      eski = Number(m[1]);
      yeni = Number(m[2]);
      satirlar.push({ tur: "konum", metin: m[3]?.trim() ?? "" });
    } else if (s.startsWith("+")) satirlar.push({ tur: "ekle", metin: s.slice(1), yeni: yeni++ });
    else if (s.startsWith("-")) satirlar.push({ tur: "sil", metin: s.slice(1), eski: eski++ });
    else if (s.startsWith("\\")) continue;
    else satirlar.push({ tur: "ayni", metin: s.slice(1), eski: eski++, yeni: yeni++ });
  }
  return satirlar;
}

/** Yan yana gorunum icin silinen ve eklenen satirlari eslestirir. */
function eslestir(satirlar: Satir[]): [Satir | null, Satir | null][] {
  const ciftler: [Satir | null, Satir | null][] = [];
  let i = 0;
  while (i < satirlar.length) {
    const s = satirlar[i];
    if (s.tur === "sil") {
      const siller: Satir[] = [];
      const ekler: Satir[] = [];
      while (i < satirlar.length && satirlar[i].tur === "sil") siller.push(satirlar[i++]);
      while (i < satirlar.length && satirlar[i].tur === "ekle") ekler.push(satirlar[i++]);
      for (let j = 0; j < Math.max(siller.length, ekler.length); j++) ciftler.push([siller[j] ?? null, ekler[j] ?? null]);
    } else if (s.tur === "ekle") {
      ciftler.push([null, s]);
      i++;
    } else {
      ciftler.push([s, s]);
      i++;
    }
  }
  return ciftler;
}

const RENK = {
  ekle: "bg-ekle/15",
  sil: "bg-sil/15",
  ayni: "",
  konum: "bg-yuzey-2 text-soluk",
};

const SINIR = 600;

export function Fark({ fark }: { fark: string }) {
  const t = useT();
  const [yanYana, setYanYana] = useState(false);
  const satirlar = useMemo(() => farkCoz(fark), [fark]);
  const eklenen = satirlar.filter((s) => s.tur === "ekle").length;
  const silinen = satirlar.filter((s) => s.tur === "sil").length;
  const gosterilen = satirlar.slice(0, SINIR);

  return (
    <div className="overflow-hidden rounded-lg border border-kenar-2">
      <div className="flex items-center gap-3 border-b border-kenar bg-yuzey-2/60 px-3 py-1.5 text-xs">
        <span className="font-mono text-ekle">+{eklenen}</span>
        <span className="font-mono text-sil">−{silinen}</span>
        <span className="flex-1" />
        <div className="flex rounded-md border border-kenar p-0.5">
          {([false, true] as const).map((y) => (
            <button
              key={String(y)}
              type="button"
              onClick={() => setYanYana(y)}
              className={clsx("flex items-center gap-1 rounded px-1.5 py-0.5", yanYana === y ? "bg-kenar-2 text-parlak" : "text-soluk hover:text-metin")}
            >
              {y ? <Columns2 size={12} /> : <Rows2 size={12} />}
              {y ? t("yanYana") : t("altAlta")}
            </button>
          ))}
        </div>
      </div>
      <div className="max-h-[420px] overflow-auto bg-kod font-mono text-[12.5px] leading-[1.55]">
        {!yanYana ? (
          <table className="w-full border-collapse">
            <tbody>
              {gosterilen.map((s, i) => (
                <tr key={i} className={RENK[s.tur]}>
                  {s.tur === "konum" ? (
                    <td colSpan={3} className="px-3 py-0.5 text-[11.5px]">@@ {s.metin}</td>
                  ) : (
                    <>
                      <td className="w-10 select-none border-r border-kenar/60 px-2 text-right text-soluk/70">{s.eski ?? ""}</td>
                      <td className="w-10 select-none border-r border-kenar/60 px-2 text-right text-soluk/70">{s.yeni ?? ""}</td>
                      <td className="whitespace-pre px-3">
                        <span className={clsx("mr-2 select-none", s.tur === "ekle" && "text-ekle", s.tur === "sil" && "text-sil")}>
                          {s.tur === "ekle" ? "+" : s.tur === "sil" ? "−" : " "}
                        </span>
                        {s.metin}
                      </td>
                    </>
                  )}
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <table className="w-full table-fixed border-collapse">
            <tbody>
              {eslestir(gosterilen).map(([sol, sag], i) =>
                sol?.tur === "konum" ? (
                  <tr key={i} className={RENK.konum}><td colSpan={4} className="px-3 py-0.5 text-[11.5px]">@@ {sol.metin}</td></tr>
                ) : (
                  <tr key={i}>
                    <td className={clsx("w-10 select-none border-r border-kenar/60 px-2 text-right text-soluk/70", sol && RENK[sol.tur === "ayni" ? "ayni" : "sil"])}>{sol?.eski ?? ""}</td>
                    <td className={clsx("overflow-hidden whitespace-pre border-r border-kenar px-3", sol && sol.tur === "sil" && RENK.sil)}>{sol?.metin ?? ""}</td>
                    <td className={clsx("w-10 select-none border-r border-kenar/60 px-2 text-right text-soluk/70", sag && sag.tur === "ekle" && RENK.ekle)}>{sag?.yeni ?? ""}</td>
                    <td className={clsx("overflow-hidden whitespace-pre px-3", sag && sag.tur === "ekle" && RENK.ekle)}>{sag?.metin ?? ""}</td>
                  </tr>
                ),
              )}
            </tbody>
          </table>
        )}
        {satirlar.length > SINIR && <div className="px-3 py-1 text-xs text-soluk">{t("satirDaha", { n: satirlar.length - SINIR })}</div>}
      </div>
    </div>
  );
}
