"use client";

import { useEffect, useRef } from "react";
import { createChart, type ISeriesApi, type LineData, type UTCTimestamp } from "lightweight-charts";
import type { MarketData } from "@terra/types";

export function PriceChart({ ticks }: { ticks: MarketData[] }): React.JSX.Element {
  const ref = useRef<HTMLDivElement | null>(null);
  const seriesRef = useRef<ISeriesApi<"Line"> | null>(null);

  useEffect(() => {
    if (!ref.current) return;
    const chart = createChart(ref.current, {
      height: 260,
      layout: { background: { color: "#09090b" }, textColor: "#d4d4d8" },
      grid: { vertLines: { color: "#27272a" }, horzLines: { color: "#27272a" } },
    });
    const series = chart.addLineSeries({ color: "#34d399" });
    seriesRef.current = series;
    return () => chart.remove();
  }, []);

  useEffect(() => {
    const latest = ticks[0];
    if (!latest || !seriesRef.current) return;
    const point: LineData = {
      time: Math.floor(new Date(latest.timestamp).getTime() / 1000) as UTCTimestamp,
      value: latest.price,
    };
    seriesRef.current.update(point);
  }, [ticks]);

  return <div ref={ref} className="h-[260px] w-full" />;
}
