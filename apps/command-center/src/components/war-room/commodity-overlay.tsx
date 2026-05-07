export function CommodityOverlay(): React.JSX.Element {
  return (
    <div className="mt-3 grid grid-cols-3 gap-2 text-xs text-zinc-300">
      <div className="rounded border border-zinc-800 p-2">Coal Corr: +0.63</div>
      <div className="rounded border border-zinc-800 p-2">Iron Ore Corr: +0.71</div>
      <div className="rounded border border-zinc-800 p-2">Zinc Corr: +0.42</div>
    </div>
  );
}
