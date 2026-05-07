"use client";

import { useState } from "react";
import { Card } from "@terra/ui";
import { ApproveTradeDialog } from "./approve-trade-dialog";

export function ExecutionGateway(): React.JSX.Element {
  const [approved, setApproved] = useState(false);

  return (
    <Card className="h-full">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold text-zinc-100">Execution Gateway</h2>
        <ApproveTradeDialog onApprove={() => setApproved(true)} />
      </div>
      <p className="mt-3 text-sm text-zinc-400">{approved ? "Last action: approved." : "No approval submitted."}</p>
    </Card>
  );
}
