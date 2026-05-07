import * as React from "react";
import { cn } from "../lib/utils";

export function Separator({
  className,
  ...props
}: React.HTMLAttributes<HTMLHRElement>): React.JSX.Element {
  return <hr className={cn("border-zinc-800", className)} {...props} />;
}
