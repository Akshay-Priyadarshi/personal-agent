"use client";

import { useEffect, useRef, useState } from "react";
import { v4 } from "uuid";
import type { ChatMessage as ChatMessageType } from "@/types";
import { ChatInput } from "./ChatInput";
import { ChatMessage } from "./ChatMessage";

export const ChatWindow = () => {
	const [messages, setMessages] = useState<ChatMessageType[]>([
		{
			id: "1",
			role: "system",
			content:
				"You are a personal finance agent. Help the user with their financial queries.",
			createdAt: new Date().toISOString(),
			updatedAt: new Date().toISOString(),
		},
		{
			id: "2",
			role: "user",
			content: "How can I save more money?",
			createdAt: new Date().toISOString(),
			updatedAt: new Date().toISOString(),
		},
		{
			id: "3",
			role: "agent",
			content:
				"You can save more money by budgeting and cutting unnecessary expenses.",
			createdAt: new Date().toISOString(),
			updatedAt: new Date().toISOString(),
		},
	]);

	const addUserMessage = (content: string): void => {
		const newUserMessage: ChatMessageType = {
			id: String(v4()),
			role: "user",
			content,
			createdAt: new Date().toISOString(),
			updatedAt: new Date().toISOString(),
		};
		setMessages((prevMessages) => [...prevMessages, newUserMessage]);
	};

	// Ref for the last message
	const lastMessageRef = useRef<HTMLDivElement | null>(null);

	useEffect(() => {
		if (lastMessageRef.current && messages.length > 0) {
			lastMessageRef.current.scrollIntoView({ behavior: "smooth" });
		}
	}, [messages]);

	return (
		<div className="flex-1 w-full gap-6 flex flex-col overflow-hidden relative shadow-2xl">
			{messages.length === 0 && <h3 className="text-2xl">🚀 Are you Ready?</h3>}
			<section className="w-full flex flex-col gap-8 overflow-y-scroll hidden-scrollbar flex-1">
				{messages.map((message: ChatMessageType, index: number) => {
					return (
						<ChatMessage
							ref={index === messages.length - 1 ? lastMessageRef : undefined}
							key={message.id}
							message={message}
						/>
					);
				})}
			</section>
			<ChatInput
				addUserMessage={addUserMessage}
				className="sticky w-full min-h-fit bottom-0 z-50"
			/>
		</div>
	);
};
