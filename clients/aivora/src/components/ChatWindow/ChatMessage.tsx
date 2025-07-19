"use client";

import { useCopyToClipboard } from "@uidotdev/usehooks";
import {
	Bot,
	Clipboard,
	type LucideProps,
	MonitorCog,
	User,
} from "lucide-react";
import { MotionConfig, motion, useInView } from "motion/react"; // fix: correct framer-motion import
import {
	type ForwardRefExoticComponent,
	forwardRef,
	type RefAttributes,
	type RefObject,
	useRef,
} from "react";
import { cn } from "@/lib/utils";
import type { ChatMessageRole, ChatMessage as ChatMessageType } from "@/types";

type ChatMessageProps = {
	message: ChatMessageType;
};

export const ChatMessage = forwardRef<HTMLDivElement, ChatMessageProps>(
	({ message }, ref) => {
		const localRef = useRef(null);
		const actualRef = (ref as RefObject<HTMLDivElement>) ?? localRef;

		const isInView = useInView(actualRef, {
			margin: "0px 0px -20% 0px",
			once: true,
		});

		const [_, copyToClipboard] = useCopyToClipboard();

		const getMessageClasses = (role: ChatMessageRole) => {
			switch (role) {
				case "user":
					return "self-end";
				case "agent":
					return "self-start";
				default:
					return "self-center";
			}
		};

		const roleIcons: Record<
			ChatMessageRole,
			ForwardRefExoticComponent<
				Omit<LucideProps, "ref"> & RefAttributes<SVGSVGElement>
			>
		> = {
			user: User,
			agent: Bot,
			system: MonitorCog,
		};

		return (
			<MotionConfig transition={{ duration: 0.75, ease: "easeOut" }}>
				<motion.div
					variants={{
						hidden: { opacity: 0, y: 20 },
						visible: { opacity: 1, y: 0 },
					}}
					initial="hidden"
					animate={isInView ? "visible" : "hidden"}
					ref={actualRef}
					key={message.id}
					className={cn(
						getMessageClasses(message.role),
						"w-3/4 border-2 border-border rounded-2xl p-3 text-sm z-10",
					)}
				>
					<div className="flex flex-col gap-4">
						<div className="flex flex-row items-center justify-between">
							<div className="flex flex-row items-center gap-2">
								{(() => {
									const Icon = roleIcons[message.role];
									return Icon ? (
										<Icon className="size-4 inline-block text-primary" />
									) : null;
								})()}
								<span className="font-bold capitalize">{message.role}</span>
							</div>
							<div>
								<Clipboard
									className="size-4 cursor-pointer"
									onClick={() => copyToClipboard(message.content)}
								/>
							</div>
						</div>
						<p>{message.content}</p>
					</div>
				</motion.div>
			</MotionConfig>
		);
	},
);
