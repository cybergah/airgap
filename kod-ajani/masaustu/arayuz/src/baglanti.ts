// Sunucuyla bag: ajandan gelen olaylar /olaylar akisindan (EventSource), panelden gidenler POST /komut ile.
// Her istek sayfaya gomulu rastgele anahtari tasir; sunucu anahtarsiz istegi reddeder.

export type Olay = { tur: string; [alan: string]: unknown };

const anahtar =
  document.querySelector<HTMLMetaElement>('meta[name="kod-ajani-anahtar"]')?.content ??
  new URLSearchParams(location.search).get("t") ??
  "";

export async function gonder(komut: Record<string, unknown>): Promise<boolean> {
  try {
    const y = await fetch(`/komut?t=${encodeURIComponent(anahtar)}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(komut),
    });
    return y.ok;
  } catch {
    return false;
  }
}

/** Olay akisina baglanir; her (yeniden) baglanista once `sifirla`, sonra sunucu gecmisi bastan yollar. */
export function dinle(olay: (o: Olay) => void, sifirla: () => void, baglanti: (acik: boolean) => void): () => void {
  const akis = new EventSource(`/olaylar?t=${encodeURIComponent(anahtar)}`);
  akis.onopen = () => {
    baglanti(true);
    sifirla();
    void gonder({ tur: "acildi" });
  };
  akis.onmessage = (e) => {
    try {
      const o = JSON.parse(e.data) as Olay;
      if (o && typeof o.tur === "string") olay(o);
    } catch {
      /* bozuk satir */
    }
  };
  akis.onerror = () => baglanti(false);
  return () => akis.close();
}
