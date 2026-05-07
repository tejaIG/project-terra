import { createClient, type SupabaseClient } from "@supabase/supabase-js";
import type { Database } from "./types";

function getEnv(name: string): string {
  const value = process.env[name];
  if (!value) {
    throw new Error(`Missing environment variable: ${name}`);
  }
  return value;
}

export function createTerraClient(): SupabaseClient<Database> {
  return createClient<Database>(getEnv("NEXT_PUBLIC_SUPABASE_URL"), getEnv("NEXT_PUBLIC_SUPABASE_ANON_KEY"));
}
