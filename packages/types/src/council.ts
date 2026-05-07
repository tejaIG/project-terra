import { z } from "zod";
import { AgentResponseSchema } from "./agents";
import { MarketDataSchema } from "./market";
import { TradeSignalSchema } from "./trades";

export const CouncilRunSchema = z.object({
  runId: z.string().uuid(),
  ticker: z.string().min(1),
  startedAt: z.string().datetime(),
  marketData: MarketDataSchema,
  responses: z.array(AgentResponseSchema).default([]),
  finalSignal: TradeSignalSchema.optional(),
});

export const AgentThoughtEventSchema = z.object({
  kind: z.literal("agent_thought"),
  runId: z.string().uuid(),
  payload: AgentResponseSchema,
});

export const PriceTickEventSchema = z.object({
  kind: z.literal("price_tick"),
  runId: z.string().uuid(),
  payload: MarketDataSchema,
});

export const CouncilEventSchema = z.discriminatedUnion("kind", [
  AgentThoughtEventSchema,
  PriceTickEventSchema,
]);

export type CouncilRun = z.infer<typeof CouncilRunSchema>;
export type AgentThoughtEvent = z.infer<typeof AgentThoughtEventSchema>;
export type PriceTickEvent = z.infer<typeof PriceTickEventSchema>;
export type CouncilEvent = z.infer<typeof CouncilEventSchema>;
