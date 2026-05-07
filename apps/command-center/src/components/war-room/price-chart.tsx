"use client";

import { useEffect, useRef } from "react";
import { createChart } from "lightweight-charts";

export function PriceChart(): React.JSX.Element {
  const ref = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (!ref.current) return;
    const chart = createChart(ref.current, {
      height: 260,
      layout: { background: { color: "#09090b" }, textColor: "#d4d4d8" },
      grid: { vertLines: { color: "#27272a" }, horzLines: { color: "#27272a" } },
    });
    const series = chart.addLineSeries({ color: "#34d399" });
    series.setData([
      { time: "2026-01-01", value: 200 },
      { time: "2026-01-02", value: 208 },
      { time: "2026-01-03", value: 205 },
      { time: "2026-01-04", value: 213 },
    ]);
    return () => chart.remove();
  }, []);

  return <div ref={ref} className="h-[260px] w-full" />;
}
