"use client";

import { useState } from "react";
import type { TradeSignal } from "@terra/types";
import { Button, Dialog, DialogContent, DialogTrigger, ShieldAlert } from "@terra/ui";
import { supabaseClient } from "@/lib/supabase/client";

export function ApproveTradeDialog({
  runId,
  signal,
  rationale,
  onApprove,
  openByDefault = false,
}: {
  runId: string;
  signal: TradeSignal;
  rationale: string;
  onApprove: () => void;
  openByDefault?: boolean;
}): React.JSX.Element {
  const [submitting, setSubmitting] = useState(false);

  const approve = async () => {
    setSubmitting(true);
    try {
      const token = (await supabaseClient.auth.getSession()).data.session?.access_token;
      await fetch(`${process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"}/trades`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        body: JSON.stringify({ runId, signal }),
      });
      onApprove();
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Dialog defaultOpen={openByDefault}>
      <DialogTrigger asChild>
        <Button variant="destructive">Approve Signal</Button>
      </DialogTrigger>
      <DialogContent>
        <div className="space-y-4">
          <div className="flex items-center gap-2 text-rose-300">
            <ShieldAlert className="h-4 w-4" />
            <p className="font-medium">High-risk action requires HITL approval</p>
          </div>
          <p className="text-sm text-zinc-300">{rationale}</p>
          <div className="text-xs text-zinc-400">
            <p>Stop-loss: {signal.riskParams.stopLossPct}%</p>
            <p>Take-profit: {signal.riskParams.takeProfitPct}%</p>
            <p>Max exposure: {signal.riskParams.maxPositionSizePct}%</p>
          </div>
          <Button onClick={approve} disabled={submitting}>
            {submitting ? "Submitting..." : "Confirm Approval"}
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}
