"use client";

import { useEffect, useState } from "react";
import { WarRoom } from "@/components/war-room";
import { IntelligenceFeed } from "@/components/intelligence-feed";
import { ExecutionGateway } from "@/components/execution-gateway";
import { usePriceStream } from "@/hooks/use-price-stream";

export function CommandCenterShell(): React.JSX.Element {
  const [runId, setRunId] = useState<string | null>(null);
  const { ticks, latest } = usePriceStream(runId);

  useEffect(() => {
    let mounted = true;
    const createRun = async () => {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"}/runs`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ticker: "NMDC" }),
      });
      const body = (await response.json()) as { runId: string };
      if (mounted) {
        setRunId(body.runId);
      }
    };
    void createRun();
    return () => {
      mounted = false;
    };
  }, []);

  return (
    <main className="grid h-dvh grid-cols-12 grid-rows-6 gap-3 bg-zinc-950 p-3 text-zinc-100">
      <section className="col-span-8 row-span-4">
        <WarRoom ticks={ticks} latest={latest} />
      </section>
      <section className="col-span-4 row-span-6">
        <IntelligenceFeed runId={runId} />
      </section>
      <section className="col-span-8 row-span-2">
        <ExecutionGateway runId={runId} />
      </section>
    </main>
  );
}
