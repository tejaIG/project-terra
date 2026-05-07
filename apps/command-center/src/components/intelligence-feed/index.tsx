"use client";

import { Card, ScrollArea } from "@terra/ui";
import { useAgentStream } from "@/hooks/use-agent-stream";
import { AgentLogRow } from "./agent-log-row";

export function IntelligenceFeed({ runId }: { runId: string | null }): React.JSX.Element {
  const { analyses, status } = useAgentStream(runId);

  return (
    <Card className="h-full">
      <div className="mb-3 flex items-center justify-between">
        <h2 className="text-lg font-semibold text-zinc-100">Intelligence Feed</h2>
        <span className="text-xs text-zinc-500">{status}</span>
      </div>
      <ScrollArea className="h-[70vh]">
        <div className="space-y-2 font-mono text-xs">
          {analyses.map((row, idx) => (
            <AgentLogRow key={`${row.createdAt}-${idx}`} row={row} />
          ))}
          {analyses.length === 0 && <p className="text-zinc-500">Waiting for council stream...</p>}
        </div>
      </ScrollArea>
    </Card>
  );
}
