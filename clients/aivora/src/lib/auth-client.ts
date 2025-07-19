import { jwt } from "better-auth/plugins";
import { createAuthClient } from "better-auth/react";
export const betterAuthClient = createAuthClient({
	/** The base URL of the server (optional if you're using the same domain) */
	baseURL: "http://localhost:3000",
	plugins: [jwt()],
});
