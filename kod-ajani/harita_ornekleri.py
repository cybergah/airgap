"""Proje haritasini olcmek icin ornek dosyalar: her dosyada bulunmasi gereken tanimlar bilinir.

Harita fonksiyon, sinif, metot, arayuz gibi tanimlari bulmali; cagrilari, kosullari ve
degiskenleri tanim saymamali. 'beklenen' adlar dosyanin gercek tanimlaridir.
"""

ORNEKLER = [
    {"yol": "src/sepet.js", "beklenen": {
        "Sepet", "constructor", "ekle", "toplam", "bos", "olustur", "indirimUygula", "fiyatBicimle", "yukle",
        "varsayilanSepet", "kaydet", "dogrula"},
     "metin": """import { api } from './api.js';

export class Sepet {
  constructor(urunler = []) {
    this.urunler = urunler;
  }

  ekle(urun) {
    if (!urun) {
      throw new Error('urun yok');
    }
    this.urunler.push(urun);
  }

  get toplam() {
    return this.urunler.reduce((t, u) => t + u.fiyat, 0);
  }

  static bos() {
    return new Sepet();
  }

  indirimUygula = (oran) => {
    this.urunler.forEach((u) => { u.fiyat *= 1 - oran; });
  };
}

export function olustur(veri) {
  return new Sepet(veri.urunler);
}

export const fiyatBicimle = (fiyat) => `${fiyat.toFixed(2)} TL`;

export async function yukle(id) {
  const yanit = await api.get(`/sepet/${id}`);
  return olustur(yanit);
}

export default function varsayilanSepet() {
  return Sepet.bos();
}

module.exports.yardimci = {
  kaydet(sepet) {
    return api.post('/sepet', sepet);
  },
  dogrula: function (sepet) {
    return sepet.urunler.length > 0;
  },
};

describe('sepet', () => {
  it('bos baslar', () => {
    expect(Sepet.bos().toplam).toBe(0);
  });
});
"""},
    {"yol": "src/kullanici.ts", "beklenen": {
        "Kullanici", "Rol", "KullaniciServisi", "bul", "kaydet", "sil", "KimlikId", "adGoster", "yetkiliMi"},
     "metin": """export interface Kullanici {
  id: number;
  ad: string;
}

export enum Rol { Admin, Uye }

export type KimlikId = string | number;

export class KullaniciServisi {
  private readonly kayitlar = new Map<number, Kullanici>();

  public async bul(id: number): Promise<Kullanici | undefined> {
    return this.kayitlar.get(id);
  }

  kaydet(k: Kullanici): void {
    this.kayitlar.set(k.id, k);
  }

  protected sil(
    id: number,
    zorla = false,
  ): boolean {
    return this.kayitlar.delete(id);
  }
}

export const adGoster = (k: Kullanici): string => k.ad.toUpperCase();

export function yetkiliMi(k: Kullanici, rol: Rol): boolean {
  for (const r of [rol]) {
    if (r === Rol.Admin) {
      return true;
    }
  }
  return false;
}
"""},
    {"yol": "Servisler/SiparisServisi.cs", "beklenen": {
        "Magaza.Servisler", "ISiparisDeposu", "BulAsync", "Kaydet", "SiparisServisi", "Toplam", "IndirimliToplam",
        "OlusturAsync", "Dogrula", "Siparis", "SiparisDurumu", "Fatura", "Yazdir", "Uzantilar", "KdvEkle"},
     "metin": """using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace Magaza.Servisler
{
    public interface ISiparisDeposu
    {
        Task<Siparis?> BulAsync(int id);
        void Kaydet(Siparis siparis);
    }

    public sealed class SiparisServisi
    {
        private readonly ISiparisDeposu _depo;

        public SiparisServisi(ISiparisDeposu depo)
        {
            _depo = depo ?? throw new ArgumentNullException(nameof(depo));
        }

        public decimal Toplam(IEnumerable<decimal> fiyatlar) => fiyatlar.Sum();

        public decimal IndirimliToplam(IEnumerable<decimal> fiyatlar, decimal oran)
        {
            if (oran < 0)
            {
                throw new ArgumentOutOfRangeException(nameof(oran));
            }
            return Toplam(fiyatlar) * (1 - oran);
        }

        [Obsolete("Yeni surumu kullan")]
        public async Task<Siparis> OlusturAsync(
            int musteriId,
            List<decimal> fiyatlar)
        {
            var siparis = new Siparis(musteriId, Toplam(fiyatlar));
            _depo.Kaydet(siparis);
            return await Task.FromResult(siparis);
        }

        private static bool Dogrula(Siparis s)
        {
            return s.Tutar > 0;
        }
    }

    public record Siparis(int MusteriId, decimal Tutar);

    public enum SiparisDurumu { Yeni, Hazirlaniyor, Gonderildi }

    internal class Fatura
    {
        internal void Yazdir()
        {
            Console.WriteLine("fatura");
        }
    }

    public static class Uzantilar
    {
        public static decimal KdvEkle(this decimal tutar) => tutar * 1.2m;
    }
}
"""},
]
