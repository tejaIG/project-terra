import { z } from "zod";

export const CorrelationSchema = z.object({
  commodity: z.string().min(1),
  coefficient: z.number().min(-1).max(1),
});

export const MarketDataSchema = z.object({
  ticker: z.string().min(1),
  price: z.number().finite(),
  volume: z.number().nonnegative(),
  commodityCorrelations: z.array(CorrelationSchema).default([]),
  timestamp: z.string().datetime(),
});

export type Correlation = z.infer<typeof CorrelationSchema>;
export type MarketData = z.infer<typeof MarketDataSchema>;
