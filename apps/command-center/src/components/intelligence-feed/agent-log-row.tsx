import type { AgentAnalysis } from "@terra/types";
import { Badge } from "@terra/ui";

const badgeClassMap: Record<AgentAnalysis["agentId"], string> = {
  geologist: "border-amber-500/40 text-amber-300",
  quant: "border-cyan-500/40 text-cyan-300",
  oracle: "border-violet-500/40 text-violet-300",
  strategist: "border-emerald-500/40 text-emerald-300",
};

export function AgentLogRow({ row }: { row: AgentAnalysis }): React.JSX.Element {
  const sentimentClass =
    row.sentimentScore < -0.2 ? "border-rose-900/50 bg-rose-950/20" : row.sentimentScore > 0.2 ? "border-emerald-900/50 bg-emerald-950/20" : "border-zinc-800";
  return (
    <div className={`rounded border p-2 text-zinc-300 ${sentimentClass}`}>
      <div className="mb-1">
        <Badge className={badgeClassMap[row.agentId]}>{row.agentId}</Badge>
      </div>
      <p>{row.analysis}</p>
    </div>
  );
}
