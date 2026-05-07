"use client";

import { createContext, useContext, useMemo } from "react";

interface WebSocketContextValue {
  baseUrl: string;
}

const WebSocketContext = createContext<WebSocketContextValue | null>(null);

export function WebSocketProvider({
  children,
}: {
  children: React.ReactNode;
}): React.JSX.Element {
  const value = useMemo(
    () => ({ baseUrl: process.env.NEXT_PUBLIC_WS_URL ?? "ws://localhost:8000" }),
    [],
  );

  return <WebSocketContext.Provider value={value}>{children}</WebSocketContext.Provider>;
}

export function useWebSocketConfig(): WebSocketContextValue {
  const context = useContext(WebSocketContext);
  if (!context) {
    throw new Error("useWebSocketConfig must be used inside WebSocketProvider");
  }
  return context;
}
