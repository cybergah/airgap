import { memo } from "react";
import ReactMarkdown, { type Components } from "react-markdown";
import remarkGfm from "remark-gfm";
import { KodBlogu } from "./Kod";
import { gonder } from "../baglanti";

// react-markdown ham HTML'i islemez (rehype-raw yok): model metnindeki <script> vb. duz metin kalir.
const BILESENLER: Components = {
  code({ className, children, ...geri }) {
    const dil = /language-([\w#+-]+)/.exec(className ?? "")?.[1];
    const metin = String(children ?? "");
    if (dil || metin.includes("\n")) return <KodBlogu kod={metin.replace(/\n$/, "")} dil={dil} />;
    return <code className="rounded border border-kenar-2 bg-derin px-1.5 py-0.5 font-mono text-[0.86em] text-[#7ee787]" {...geri}>{children}</code>;
  },
  pre: ({ children }) => <>{children}</>,
  a({ href, children }) {
    // Uygulama penceresi baska sayfaya gitmesin: baglanti varsayilan tarayicida acilir (yalniz http/https).
    return (
      <a
        href={href}
        className="text-vurgu underline decoration-vurgu/40 underline-offset-2 transition hover:decoration-vurgu"
        onClick={(e) => {
          e.preventDefault();
          if (href && /^https?:\/\//i.test(href)) void gonder({ tur: "bag_ac", adres: href });
        }}
      >
        {children}
      </a>
    );
  },
  table: ({ children }) => <div className="my-3 overflow-x-auto"><table className="w-full border-collapse text-sm">{children}</table></div>,
  th: ({ children }) => <th className="border border-kenar bg-yuzey-2 px-2.5 py-1.5 text-left font-semibold">{children}</th>,
  td: ({ children }) => <td className="border border-kenar px-2.5 py-1.5">{children}</td>,
  img: ({ alt }) => <span className="text-soluk">[{alt}]</span>, // dis kaynak yuklenmez
};

export const Markdown = memo(function Markdown({ metin }: { metin: string }) {
  return (
    <div className="yazi">
      <ReactMarkdown remarkPlugins={[remarkGfm]} components={BILESENLER} skipHtml>
        {metin}
      </ReactMarkdown>
    </div>
  );
});
