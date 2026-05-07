import { createTerraClient } from "@terra/database";

export function getServerSupabaseClient() {
  return createTerraClient();
}
