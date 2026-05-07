"use client";

import { Card, ScrollArea } from "@terra/ui";
import { useAgentStream } from "@/hooks/use-agent-stream";
import { AgentLogRow } from "./agent-log-row";

export function IntelligenceFeed(): React.JSX.Element {
  const rows = useAgentStream();

  return (
    <Card className="h-full">
      <h2 className="mb-3 text-lg font-semibold text-zinc-100">Intelligence Feed</h2>
      <ScrollArea className="h-[70vh]">
        <div className="space-y-2 font-mono text-xs">
          {rows.map((row, idx) => (
            <AgentLogRow key={`${row.createdAt}-${idx}`} row={row} />
          ))}
          {rows.length === 0 && <p className="text-zinc-500">Waiting for council stream...</p>}
        </div>
      </ScrollArea>
    </Card>
  );
}
