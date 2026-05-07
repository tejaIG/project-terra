import type { AgentResponse } from "@terra/types";

export function AgentLogRow({ row }: { row: AgentResponse }): React.JSX.Element {
  return (
    <div className="rounded border border-zinc-800 p-2 text-zinc-300">
      [{row.agentId}] {row.analysis}
    </div>
  );
}
