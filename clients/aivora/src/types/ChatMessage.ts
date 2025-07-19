import { v4 } from "uuid";
import { z } from "zod";

export const chatMessage = z.object({
	id: z.string().default(() => v4()),
	createdAt: z.string(),
	updatedAt: z.string(),
	content: z.string().min(1, "Message cannot be empty"),
	role: z.enum(["user", "agent", "system"]),
});

export type ChatMessage = z.infer<typeof chatMessage>;

export type ChatMessageRole = ChatMessage["role"];
