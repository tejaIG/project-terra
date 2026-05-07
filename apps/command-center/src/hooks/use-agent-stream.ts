"use client";

import { useMemo } from "react";
import type { AgentAnalysis } from "@terra/types";
import { useCouncilSocket } from "./use-council-socket";

export function useAgentStream(runId: string | null): { analyses: AgentAnalysis[]; status: string } {
  const { events, status } = useCouncilSocket(runId);
  const analyses = useMemo(
    () =>
      events
        .filter((event) => event.kind === "agent_thought")
        .map((event) => event.payload)
        .slice(0, 200),
    [events],
  );
  return { analyses, status };
}
