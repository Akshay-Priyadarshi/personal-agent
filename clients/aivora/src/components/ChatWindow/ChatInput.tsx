"use client";

import type { ClassValue } from "clsx";
import { Send } from "lucide-react";
import { useState } from "react";
import { default as Textarea } from "react-textarea-autosize";
import { cn } from "@/lib/utils";
import { Button } from "../ui";

type ChatInputProps = {
	addUserMessage: (content: string) => void;
	className?: ClassValue;
};

export const ChatInput = ({ addUserMessage, className }: ChatInputProps) => {
	const [userQuery, setUserQuery] = useState("");
	const handleSend = () => {
		if (userQuery.trim() !== "") {
			addUserMessage(userQuery);
			setUserQuery("");
		}
	};
	return (
		<div
			className={cn(
				"w-full z-20 border-input rounded-2xl border-2 p-2",
				className,
			)}
		>
			<Textarea
				autoFocus
				className="w-full min-h-24 max-h-48 bg-transparent dark:bg-transparent h-4/5 text-sm border-0 focus-visible:outline-0 focus-visible:ring-0 focus-visible:border-0 resize-none overflow-scroll custom-scrollbar"
				placeholder="What's on your mind?"
				onChange={(e) => setUserQuery(e.target.value)}
				value={userQuery}
				onKeyDown={(e) => {
					if (e.key === "Enter" && !e.shiftKey) {
						e.preventDefault();
						handleSend();
					}
				}}
			/>
			<div className="flex flex-row justify-between">
				<div></div>
				<Button
					className="cursor-pointer bg-transparent hover:bg-transparent"
					onClick={handleSend}
				>
					<Send className="size-4 text-primary" />
				</Button>
			</div>
		</div>
	);
};
