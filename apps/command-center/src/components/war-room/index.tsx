import { Card, Badge } from "@terra/ui";
import type { MarketData } from "@terra/types";
import { PriceChart } from "./price-chart";
import { CommodityOverlay } from "./commodity-overlay";

export function WarRoom({ ticks, latest }: { ticks: MarketData[]; latest: MarketData | null }): React.JSX.Element {
  return (
    <Card className="h-full">
      <div className="mb-3 flex items-center justify-between">
        <h2 className="text-lg font-semibold text-zinc-100">War Room</h2>
        <Badge className="border-emerald-400/30 text-emerald-300">Live</Badge>
      </div>
      <PriceChart ticks={ticks} />
      <CommodityOverlay latest={latest} />
    </Card>
  );
}
