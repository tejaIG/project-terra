"use client";

import { useMemo } from "react";
import type { MarketData } from "@terra/types";

export function usePriceStream(): MarketData[] {
  return useMemo(
    () => [
      {
        ticker: "NMDC",
        price: 244.2,
        volume: 120000,
        commodityCorrelations: [{ commodity: "iron_ore", coefficient: 0.71 }],
        timestamp: new Date().toISOString(),
      },
    ],
    [],
  );
}
