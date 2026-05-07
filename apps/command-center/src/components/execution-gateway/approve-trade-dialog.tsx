"use client";

import { Button, Dialog, DialogContent, DialogTrigger, ShieldAlert } from "@terra/ui";

export function ApproveTradeDialog({
  onApprove,
}: {
  onApprove: () => void;
}): React.JSX.Element {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="destructive">Approve Signal</Button>
      </DialogTrigger>
      <DialogContent>
        <div className="space-y-4">
          <div className="flex items-center gap-2 text-rose-300">
            <ShieldAlert className="h-4 w-4" />
            <p className="font-medium">High-risk action requires HITL approval</p>
          </div>
          <p className="text-sm text-zinc-300">Approve BUY signal for NMDC with capped risk parameters.</p>
          <Button onClick={onApprove}>Confirm Approval</Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}
