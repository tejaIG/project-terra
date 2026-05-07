"use client";

import { useMemo } from "react";
import type { TradeSignal } from "@terra/types";
import { useCouncilSocket } from "./use-council-socket";

export function useFinalSignal(runId: string | null): TradeSignal | null {
  const { events } = useCouncilSocket(runId);
  return useMemo(() => {
    const completed = events.find((event) => event.kind === "run_completed");
    if (!completed || completed.kind !== "run_completed") {
      return null;
    }
    return completed.payload.finalSignal ?? null;
  }, [events]);
}
