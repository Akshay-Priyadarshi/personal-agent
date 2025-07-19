import "dotenv/config";
import { drizzle } from "drizzle-orm/node-postgres";

if (!process.env.DATABASE_URL) {
	throw new Error("DATABASE_URL is not set in the environment variables.");
}

console.log("Connecting to database with URL:", process.env.DATABASE_URL);

export const db = drizzle({
	connection: { connectionString: process.env.DATABASE_URL },
});
