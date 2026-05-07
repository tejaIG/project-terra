import type { MarketData } from "@terra/types";

export function CommodityOverlay({ latest }: { latest: MarketData | null }): React.JSX.Element {
  const correlations = latest?.commodityCorrelations ?? [];
  return (
    <div className="mt-3 grid grid-cols-3 gap-2 text-xs text-zinc-300">
      {correlations.map((entry) => (
        <div
          key={entry.commodity}
          className={`rounded border p-2 ${entry.coefficient >= 0 ? "border-emerald-900/40 text-emerald-200" : "border-rose-900/40 text-rose-200"}`}
        >
          {entry.commodity}: {entry.coefficient > 0 ? "+" : ""}
          {entry.coefficient.toFixed(2)}
        </div>
      ))}
      {correlations.length === 0 && <div className="rounded border border-zinc-800 p-2">Awaiting correlation stream...</div>}
    </div>
  );
}
