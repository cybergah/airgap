import clsx from "clsx";

/** Airgap logosu (docs/logo.svg ile ayni cizim): kalkan ve ortasi kesik kablo. `canli` iken boslukta kivilcim atar. */
export function Kalkan({ boyut = 32, zemin = true, canli = false, className }: { boyut?: number; zemin?: boolean; canli?: boolean; className?: string }) {
  return (
    <svg viewBox="0 0 128 128" width={boyut} height={boyut} className={clsx("shrink-0", className)} aria-hidden="true">
      <defs>
        <linearGradient id="ag-yesil" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#00FF41" />
          <stop offset="1" stopColor="#00B32D" />
        </linearGradient>
        <filter id="ag-parilti" x="-30%" y="-30%" width="160%" height="160%">
          <feGaussianBlur stdDeviation="3" result="b" />
          <feMerge><feMergeNode in="b" /><feMergeNode in="SourceGraphic" /></feMerge>
        </filter>
      </defs>
      {zemin && <rect width="128" height="128" rx="28" fill="#0D1117" />}
      <g filter={canli ? "url(#ag-parilti)" : undefined}>
        <path d="M64 14 L104 28 V62 C104 88 87 106 64 116 C41 106 24 88 24 62 V28 Z" fill="none" stroke="url(#ag-yesil)" strokeWidth="7" strokeLinejoin="round" />
        <path d="M38 66 H56" stroke="#00FF41" strokeWidth="7" strokeLinecap="round" />
        <path d="M72 66 H90" stroke="#00FF41" strokeWidth="7" strokeLinecap="round" />
      </g>
      <circle cx="56" cy="66" r="2.5" fill="#0D1117" />
      <circle cx="72" cy="66" r="2.5" fill="#0D1117" />
      <path d="M60 58 L68 74" stroke="#C9D1D9" strokeWidth="3" strokeLinecap="round" opacity="0.55" className={canli ? "kivilcim" : undefined} />
    </svg>
  );
}

export function Yazi({ className }: { className?: string }) {
  return <span className={clsx("font-mono font-bold tracking-[0.18em] text-parlak", className)}>AIRGAP</span>;
}
