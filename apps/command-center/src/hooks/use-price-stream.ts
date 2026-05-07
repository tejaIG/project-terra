"use client";

import { useMemo } from "react";
import type { MarketData } from "@terra/types";
import { useCouncilSocket } from "./use-council-socket";

export function usePriceStream(runId: string | null): { ticks: MarketData[]; latest: MarketData | null; status: string } {
  const { events, status } = useCouncilSocket(runId);
  const ticks = useMemo(
    () =>
      events
        .filter((event) => event.kind === "price_tick")
        .map((event) => event.payload)
        .slice(0, 200),
    [events],
  );
  return { ticks, latest: ticks[0] ?? null, status };
}
