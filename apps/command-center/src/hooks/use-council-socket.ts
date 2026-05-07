"use client";

import { useEffect, useMemo, useState } from "react";
import type { CouncilEvent } from "@terra/types";
import { CouncilEventSchema } from "@terra/types";
import { useWebSocketConfig } from "@/providers/websocket-provider";

export type SocketStatus = "idle" | "connecting" | "open" | "closed" | "error";

type Subscriber = (event: CouncilEvent) => void;

interface SocketState {
  socket: WebSocket | null;
  status: SocketStatus;
  events: CouncilEvent[];
  attempts: number;
  subscribers: Set<Subscriber>;
}

const sockets = new Map<string, SocketState>();

function getOrCreateState(runId: string): SocketState {
  const existing = sockets.get(runId);
  if (existing) return existing;
  const created: SocketState = {
    socket: null,
    status: "idle",
    events: [],
    attempts: 0,
    subscribers: new Set<Subscriber>(),
  };
  sockets.set(runId, created);
  return created;
}

export function useCouncilSocket(runId: string | null): { events: CouncilEvent[]; status: SocketStatus } {
  const { baseUrl } = useWebSocketConfig();
  const [status, setStatus] = useState<SocketStatus>(runId ? "connecting" : "idle");
  const [events, setEvents] = useState<CouncilEvent[]>([]);

  useEffect(() => {
    if (!runId) {
      setStatus("idle");
      setEvents([]);
      return;
    }

    const state = getOrCreateState(runId);
    const subscriber: Subscriber = (event) => {
      setEvents((prev) => [event, ...prev].slice(0, 400));
    };
    state.subscribers.add(subscriber);
    setStatus(state.status);

    const connect = () => {
      state.status = "connecting";
      setStatus("connecting");
      const ws = new WebSocket(`${baseUrl}/ws/council/${runId}`);
      state.socket = ws;
      ws.onopen = () => {
        state.status = "open";
        state.attempts = 0;
        setStatus("open");
      };
      ws.onmessage = (message) => {
        const parsed = CouncilEventSchema.safeParse(JSON.parse(message.data));
        if (!parsed.success) return;
        state.events = [parsed.data, ...state.events].slice(0, 400);
        state.subscribers.forEach((handler) => handler(parsed.data));
      };
      ws.onclose = () => {
        state.status = "closed";
        setStatus("closed");
        if (state.attempts < 5) {
          state.attempts += 1;
          const timeoutMs = Math.min(1000 * 2 ** state.attempts, 15000);
          setTimeout(connect, timeoutMs);
        }
      };
      ws.onerror = () => {
        state.status = "error";
        setStatus("error");
      };
    };

    if (!state.socket || state.socket.readyState === WebSocket.CLOSED) {
      connect();
    }
    setEvents(state.events);

    return () => {
      state.subscribers.delete(subscriber);
      if (state.subscribers.size === 0 && state.socket) {
        state.socket.close();
        state.socket = null;
      }
    };
  }, [baseUrl, runId]);

  return useMemo(() => ({ events, status }), [events, status]);
}
