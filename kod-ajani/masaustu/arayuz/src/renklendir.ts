// Shiki ile kod renklendirme. WebAssembly yerine JavaScript duzenli ifade motoru: sayfanin guvenlik kurali
// (CSP) wasm ya da eval'e izin vermiyor. Diller ilk kullanildiklarinda ayri parca olarak yuklenir.
import { createHighlighterCore, type HighlighterCore } from "shiki/core";
import { createJavaScriptRegexEngine } from "shiki/engine/javascript";

const DILLER: Record<string, () => Promise<unknown>> = {
  python: () => import("shiki/langs/python.mjs"),
  javascript: () => import("shiki/langs/javascript.mjs"),
  typescript: () => import("shiki/langs/typescript.mjs"),
  tsx: () => import("shiki/langs/tsx.mjs"),
  jsx: () => import("shiki/langs/jsx.mjs"),
  json: () => import("shiki/langs/json.mjs"),
  bash: () => import("shiki/langs/bash.mjs"),
  powershell: () => import("shiki/langs/powershell.mjs"),
  csharp: () => import("shiki/langs/csharp.mjs"),
  html: () => import("shiki/langs/html.mjs"),
  css: () => import("shiki/langs/css.mjs"),
  markdown: () => import("shiki/langs/markdown.mjs"),
  diff: () => import("shiki/langs/diff.mjs"),
  yaml: () => import("shiki/langs/yaml.mjs"),
  toml: () => import("shiki/langs/toml.mjs"),
  sql: () => import("shiki/langs/sql.mjs"),
  go: () => import("shiki/langs/go.mjs"),
  rust: () => import("shiki/langs/rust.mjs"),
  java: () => import("shiki/langs/java.mjs"),
  c: () => import("shiki/langs/c.mjs"),
  cpp: () => import("shiki/langs/cpp.mjs"),
};

const TAKMA: Record<string, string> = {
  py: "python", js: "javascript", mjs: "javascript", cjs: "javascript", ts: "typescript", sh: "bash", shell: "bash",
  zsh: "bash", console: "bash", ps1: "powershell", ps: "powershell", pwsh: "powershell", cs: "csharp", "c#": "csharp",
  yml: "yaml", md: "markdown", htm: "html", patch: "diff", "c++": "cpp", hpp: "cpp", h: "c", rs: "rust",
};

let cekirdek: Promise<HighlighterCore> | null = null;
const yuklenen = new Set<string>();

function hazirla(): Promise<HighlighterCore> {
  cekirdek ??= createHighlighterCore({
    themes: [import("shiki/themes/github-dark-default.mjs"), import("shiki/themes/github-light-default.mjs")],
    langs: [],
    engine: createJavaScriptRegexEngine(),
  });
  return cekirdek;
}

export function dilAdi(etiket: string | undefined): string | null {
  const d = (etiket ?? "").toLowerCase().trim();
  const ad = TAKMA[d] ?? d;
  return ad in DILLER ? ad : null;
}

export function uzantidanDil(yol: string): string | null {
  const uz = yol.split(".").pop() ?? "";
  return dilAdi(uz);
}

/** Satir satir renklendirilmis parcalar; dil bilinmiyorsa null (duz metin gosterilir). */
export async function renklendir(kod: string, dil: string): Promise<{ icerik: string; renk?: string }[][] | null> {
  const ad = dilAdi(dil);
  if (!ad) return null;
  const h = await hazirla();
  if (!yuklenen.has(ad)) {
    const m = (await DILLER[ad]()) as { default: Parameters<HighlighterCore["loadLanguage"]>[0] };
    await h.loadLanguage(m.default);
    yuklenen.add(ad);
  }
  const koyu = matchMedia("(prefers-color-scheme: dark)").matches;
  const sonuc = h.codeToTokensBase(kod, { lang: ad, theme: koyu ? "github-dark-default" : "github-light-default" });
  return sonuc.map((satir) => satir.map((p) => ({ icerik: p.content, renk: p.color })));
}
