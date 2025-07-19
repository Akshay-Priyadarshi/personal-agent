import { toNextJsHandler } from "better-auth/next-js";
import { betterAuthServer } from "@/lib/auth"; // path to your auth file

export const { POST, GET } = toNextJsHandler(betterAuthServer);
