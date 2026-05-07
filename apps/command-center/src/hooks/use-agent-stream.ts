"use client";

import { useEffect, useState } from "react";
import type { AgentResponse } from "@terra/types";
import { useWebSocketConfig } from "@/providers/websocket-provider";

export function useAgentStream(): AgentResponse[] {
  const { url } = useWebSocketConfig();
  const [rows, setRows] = useState<AgentResponse[]>([]);

  useEffect(() => {
    const socket = new WebSocket(url);
    socket.onmessage = (event) => {
      try {
        const parsed = JSON.parse(event.data) as AgentResponse;
        if (parsed?.agentId) {
          setRows((prev) => [parsed, ...prev].slice(0, 200));
        }
      } catch {
        // ignore malformed payloads in early scaffold stage
      }
    };
    return () => socket.close();
  }, [url]);

  return rows;
}
