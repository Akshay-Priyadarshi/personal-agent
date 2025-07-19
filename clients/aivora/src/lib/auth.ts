import { betterAuth } from "better-auth";
import { drizzleAdapter } from "better-auth/adapters/drizzle";
import { jwt } from "better-auth/plugins";
import { account, db, session, user, verification } from "@/database";

export const betterAuthServer = betterAuth({
	emailAndPassword: {
		enabled: true,
	},
	database: drizzleAdapter(db, {
		provider: "pg",
		debugLogs: process.env.NODE_ENV === "development",
		schema: {
			user,
			session,
			account,
			verification,
		},
	}),
	plugins: [jwt()],
});
