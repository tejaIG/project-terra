import { z } from "zod";
import { AgentAnalysisSchema } from "./agents";
import { MarketDataSchema } from "./market";
import { TradeSignalSchema } from "./trades";

export const CouncilRunSchema = z.object({
  runId: z.string().uuid(),
  ticker: z.string().min(1),
  startedAt: z.string().datetime(),
  marketData: MarketDataSchema,
  analyses: z.array(AgentAnalysisSchema).default([]),
  finalSignal: TradeSignalSchema.optional(),
});

export const AgentThoughtEventSchema = z.object({
  kind: z.literal("agent_thought"),
  runId: z.string().uuid(),
  payload: AgentAnalysisSchema,
});

export const PriceTickEventSchema = z.object({
  kind: z.literal("price_tick"),
  runId: z.string().uuid(),
  payload: MarketDataSchema,
});

export const RunStartedEventSchema = z.object({
  kind: z.literal("run_started"),
  runId: z.string().uuid(),
  payload: z.object({
    ticker: z.string().min(1),
    startedAt: z.string().datetime(),
  }),
});

export const RunCompletedEventSchema = z.object({
  kind: z.literal("run_completed"),
  runId: z.string().uuid(),
  payload: z.object({
    completedAt: z.string().datetime(),
    finalSignal: TradeSignalSchema.optional(),
  }),
});

export const ErrorEventSchema = z.object({
  kind: z.literal("error"),
  runId: z.string().uuid(),
  payload: z.object({
    message: z.string().min(1),
  }),
});

export const CouncilEventSchema = z.discriminatedUnion("kind", [
  AgentThoughtEventSchema,
  PriceTickEventSchema,
  RunStartedEventSchema,
  RunCompletedEventSchema,
  ErrorEventSchema,
]);

export type CouncilRun = z.infer<typeof CouncilRunSchema>;
export type AgentThoughtEvent = z.infer<typeof AgentThoughtEventSchema>;
export type PriceTickEvent = z.infer<typeof PriceTickEventSchema>;
export type RunStartedEvent = z.infer<typeof RunStartedEventSchema>;
export type RunCompletedEvent = z.infer<typeof RunCompletedEventSchema>;
export type ErrorEvent = z.infer<typeof ErrorEventSchema>;
export type CouncilEvent = z.infer<typeof CouncilEventSchema>;
