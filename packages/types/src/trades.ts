import { z } from "zod";

export const TradeActionSchema = z.enum(["BUY", "SELL"]);
export type TradeAction = z.infer<typeof TradeActionSchema>;

export const RiskParamsSchema = z.object({
  stopLossPct: z.number().positive(),
  takeProfitPct: z.number().positive(),
  maxPositionSizePct: z.number().positive(),
});

export const TradeSignalSchema = z.object({
  ticker: z.string().min(1),
  action: TradeActionSchema,
  rationale: z.string().min(1),
  riskParams: RiskParamsSchema,
});

export type RiskParams = z.infer<typeof RiskParamsSchema>;
export type TradeSignal = z.infer<typeof TradeSignalSchema>;
