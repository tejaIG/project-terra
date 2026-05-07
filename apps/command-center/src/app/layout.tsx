import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { WebSocketProvider } from "@/providers/websocket-provider";
import { ThemeProvider } from "@/providers/theme-provider";
import "./globals.css";

const geistSans = Geist({ subsets: ["latin"], variable: "--font-geist-sans" });
const geistMono = Geist_Mono({ subsets: ["latin"], variable: "--font-geist-mono" });

export const metadata: Metadata = {
  title: "Project Terra Command Center",
  description: "War Room for AI-driven mining equity intelligence.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>): React.JSX.Element {
  return (
    <html lang="en" className="dark">
      <body className={`${geistSans.variable} ${geistMono.variable} bg-zinc-950 text-zinc-100`}>
        <ThemeProvider>
          <WebSocketProvider>{children}</WebSocketProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
