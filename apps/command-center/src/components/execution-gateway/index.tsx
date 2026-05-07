"use client";

import { useState } from "react";
import { Card } from "@terra/ui";
import { useAgentStream } from "@/hooks/use-agent-stream";
import { useFinalSignal } from "@/hooks/use-final-signal";
import { ApproveTradeDialog } from "./approve-trade-dialog";

export function ExecutionGateway({ runId }: { runId: string | null }): React.JSX.Element {
  const [approved, setApproved] = useState(false);
  const { analyses } = useAgentStream(runId);
  const finalSignal = useFinalSignal(runId);
  const strategistThought = analyses.find((analysis) => analysis.agentId === "strategist");
  const canApprove = Boolean(runId && finalSignal && strategistThought && strategistThought.confidence >= 0.8);

  return (
    <Card className="h-full">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold text-zinc-100">Execution Gateway</h2>
        {canApprove && runId && finalSignal && strategistThought ? (
          <ApproveTradeDialog
            runId={runId}
            signal={finalSignal}
            rationale={strategistThought.analysis}
            openByDefault
            onApprove={() => setApproved(true)}
          />
        ) : null}
      </div>
      <p className="mt-3 text-sm text-zinc-400">{approved ? "Last action: approved." : "No approval submitted."}</p>
    </Card>
  );
}
