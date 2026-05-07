import { z } from "zod";

export const AgentIdSchema = z.enum(["geologist", "quant", "oracle", "strategist"]);
export type AgentId = z.infer<typeof AgentIdSchema>;

export const AgentAnalysisSchema = z.object({
  agentId: AgentIdSchema,
  analysis: z.string().min(1),
  sentimentScore: z.number().min(-1).max(1),
  confidence: z.number().min(0).max(1),
  createdAt: z.string().datetime(),
});

export type AgentAnalysis = z.infer<typeof AgentAnalysisSchema>;
