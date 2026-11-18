// Ajan olaylarini ekranda gosterilecek ogelere ceviren saf indirgeyici (reducer). Model ciktisi guvenilmez
// metindir: burada yalniz duz metin tutulur, HTML'e cevirme yalniz guvenli bilesenlerde (react-markdown) yapilir.
import type { Olay } from "./baglanti";
import type { Anahtar } from "./dil";

export type OnayDurumu = "bekliyor" | "e" | "h" | "t" | "kapandi";
export type Onay = { id: number; soru: string; hepIzin: boolean; durum: OnayDurumu };
export type Dosya = { yol: string; durum: string };

export type Oge =
  | { k: "kullanici"; n: number; metin: string }
  | { k: "dusunce"; n: number; metin: string }
  | { k: "ajan"; n: number; metin: string }
  | { k: "arac"; n: number; ad: string; hedef: string }
  | { k: "komut"; n: number; komut: string; onay?: Onay; cikti?: string }
  | { k: "degisiklik"; n: number; yol: string; fark: string; onay?: Onay }
  | { k: "onay"; n: number; onay: Onay }
  | { k: "sonuc"; n: number; ad: string; metin: string }
  | { k: "uyari" | "hata" | "ayrac"; n: number; metin: string; anahtar?: Anahtar }
  | { k: "baglam"; n: number; parcalar: string[] }
  | { k: "geri"; n: number; tip: "tur" | "geri"; dosyalar: Dosya[]; nokta: string; bitti?: boolean };

export type Durum = {
  ogeler: Oge[];
  mesgul: boolean;
  asama: "model" | "onay" | "komut";
  sonCikti: number;
  sayac: number;
};

export const BASLANGIC: Durum = { ogeler: [], mesgul: false, asama: "model", sonCikti: Date.now(), sayac: 0 };

const s = (x: unknown) => (typeof x === "string" ? x : x == null ? "" : String(x));

function dosyalar(x: unknown): Dosya[] {
  return Array.isArray(x) ? x.map((d) => ({ yol: s(d?.yol), durum: s(d?.durum) })) : [];
}

function sonDegistir<T extends Oge>(ogeler: Oge[], k: T["k"], f: (o: T) => T): Oge[] | null {
  const son = ogeler[ogeler.length - 1];
  if (!son || son.k !== k) return null;
  return [...ogeler.slice(0, -1), f(son as T)];
}

function onaylariKapat(ogeler: Oge[]): Oge[] {
  return ogeler.map((o) => {
    if ("onay" in o && o.onay && o.onay.durum === "bekliyor") return { ...o, onay: { ...o.onay, durum: "kapandi" } } as Oge;
    return o;
  });
}

export function indirge(d: Durum, olay: Olay | { tur: "_sifirla" } | { tur: "_onayla"; id: number; yanit: OnayDurumu }): Durum {
  const n = d.sayac + 1;
  const simdi = Date.now();
  const ekle = (o: Oge, ek: Partial<Durum> = {}): Durum => ({ ...d, ...ek, sayac: n, ogeler: [...d.ogeler, o], sonCikti: simdi });
  const o = olay as Olay;
  switch (o.tur) {
    case "_sifirla":
    case "temizle":
      return { ...BASLANGIC, sonCikti: simdi };
    case "onay_yanit": // sunucu gecmisinden: yeniden yuklemede verilen karar gorunsun
    case "_onayla": {
      const id = Number((olay as { id: unknown }).id);
      const yanit = (olay as { yanit: OnayDurumu }).yanit;
      const ogeler = d.ogeler.map((x) =>
        "onay" in x && x.onay && x.onay.id === id ? ({ ...x, onay: { ...x.onay, durum: yanit } } as Oge) : x,
      );
      const komutMu = ogeler.some((x) => x.k === "komut" && x.onay?.id === id);
      return { ...d, ogeler, asama: yanit !== "h" && komutMu ? "komut" : "model", sonCikti: simdi };
    }
    case "kullanici":
      return ekle({ k: "kullanici", n, metin: s(o.metin) }, { mesgul: true, asama: "model" });
    case "dusunce": {
      const yeni = sonDegistir<Extract<Oge, { k: "dusunce" }>>(d.ogeler, "dusunce", (x) => ({ ...x, metin: x.metin + s(o.metin) }));
      return yeni ? { ...d, ogeler: yeni, sonCikti: simdi } : ekle({ k: "dusunce", n, metin: s(o.metin) });
    }
    case "icerik": {
      const yeni = sonDegistir<Extract<Oge, { k: "ajan" }>>(d.ogeler, "ajan", (x) => ({ ...x, metin: x.metin + s(o.metin) }));
      return yeni ? { ...d, ogeler: yeni, sonCikti: simdi } : ekle({ k: "ajan", n, metin: s(o.metin) });
    }
    case "ara_not": {
      // Arac cagrisindan onceki not cogu kez Ingilizce ic sestir: sohbet balonu degil, dusunceye katilir.
      const son = d.ogeler[d.ogeler.length - 1];
      if (!son || son.k !== "ajan") return d;
      const onceki = d.ogeler[d.ogeler.length - 2];
      if (onceki && onceki.k === "dusunce") {
        return { ...d, ogeler: [...d.ogeler.slice(0, -2), { ...onceki, metin: onceki.metin + "\n" + son.metin }] };
      }
      return { ...d, ogeler: [...d.ogeler.slice(0, -1), { k: "dusunce", n: son.n, metin: son.metin }] };
    }
    case "arac": {
      const arg = (o.arg ?? {}) as Record<string, unknown>;
      return ekle({ k: "arac", n, ad: s(o.ad), hedef: s(arg.path ?? arg.pattern ?? arg.query ?? "") });
    }
    case "komut":
      return ekle({ k: "komut", n, komut: s(o.komut) }, { asama: "komut" });
    case "degisiklik":
      return ekle({ k: "degisiklik", n, yol: s(o.yol), fark: s(o.fark) });
    case "onay": {
      const onay: Onay = { id: Number(o.id), soru: s(o.soru), hepIzin: o.hep_izin !== false, durum: "bekliyor" };
      // Ajan komut/degisiklik ile onay sorusu arasina uyari yazabilir ("komut ayristirilamadi"): onlar atlanir.
      let i = d.ogeler.length - 1;
      while (i >= 0 && d.ogeler[i].k === "uyari") i--;
      const hedef = d.ogeler[i];
      if (hedef && (hedef.k === "komut" || hedef.k === "degisiklik") && !hedef.onay) {
        const ogeler = [...d.ogeler];
        ogeler[i] = { ...hedef, onay };
        return { ...d, ogeler, asama: "onay", sonCikti: simdi };
      }
      return ekle({ k: "onay", n, onay }, { asama: "onay" });
    }
    case "sonuc": {
      const son = d.ogeler[d.ogeler.length - 1];
      if (s(o.ad) === "run_command" && son && son.k === "komut" && son.cikti === undefined) {
        return { ...d, ogeler: [...d.ogeler.slice(0, -1), { ...son, cikti: s(o.metin) }], asama: "model", sonCikti: simdi };
      }
      return ekle({ k: "sonuc", n, ad: s(o.ad), metin: s(o.metin) }, { asama: "model" });
    }
    case "uyari":
    case "hata":
    case "ayrac":
      return ekle({ k: o.tur, n, metin: s(o.metin) });
    case "surec_bitti":
      return { ...d, ogeler: onaylariKapat([...d.ogeler, { k: "hata", n, metin: s(o.metin) }]), mesgul: false, sayac: n, sonCikti: simdi };
    case "baglam_eklendi": {
      const parcalar: string[] = [];
      if (o.dosya) parcalar.push(s(o.dosya));
      if (Array.isArray(o.anilan)) o.anilan.forEach((a) => parcalar.push("@" + s(a)));
      return parcalar.length ? ekle({ k: "baglam", n, parcalar }) : d;
    }
    case "tur_bitti": {
      let ogeler = onaylariKapat(d.ogeler);
      const ds = dosyalar(o.dosyalar);
      if (o.nokta && ds.length) {
        ogeler = [...ogeler, { k: "geri", n, tip: "tur", dosyalar: ds, nokta: s(o.nokta) }];
      }
      return { ...d, ogeler, mesgul: false, sayac: n, sonCikti: simdi };
    }
    case "geri_alindi": {
      const nokta = s(o.nokta);
      let ogeler = d.ogeler.map((x) => (x.k === "geri" && x.nokta === nokta ? { ...x, bitti: true } : x));
      const ds = dosyalar(o.dosyalar);
      ogeler = ds.length
        ? [...ogeler, { k: "geri", n, tip: "geri", dosyalar: ds, nokta: s(o.guvenlik) }]
        : [...ogeler, { k: "uyari", n, metin: "", anahtar: "geriAlinacakYok" }];
      return { ...d, ogeler, sayac: n };
    }
    case "geri_alinamadi":
      return ekle({ k: "hata", n, metin: "", anahtar: "geriAlinamadi" });
    default:
      return d;
  }
}
