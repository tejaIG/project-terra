import { WarRoom } from "@/components/war-room";
import { IntelligenceFeed } from "@/components/intelligence-feed";
import { ExecutionGateway } from "@/components/execution-gateway";

export default function CommandCenterPage(): React.JSX.Element {
  return (
    <main className="grid h-dvh grid-cols-12 grid-rows-6 gap-3 bg-zinc-950 p-3 text-zinc-100">
      <section className="col-span-8 row-span-4">
        <WarRoom />
      </section>
      <section className="col-span-4 row-span-6">
        <IntelligenceFeed />
      </section>
      <section className="col-span-8 row-span-2">
        <ExecutionGateway />
      </section>
    </main>
  );
}
