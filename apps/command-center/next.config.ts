import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  transpilePackages: ["@terra/ui", "@terra/types", "@terra/database"],
};

export default nextConfig;
