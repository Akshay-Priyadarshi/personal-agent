import { ChatWindow, Header } from "@/components";

export default function Home() {
	return (
		<div className="px-16 h-screen w-screen flex flex-col overflow-hidden">
			<Header />
			<ChatWindow />
		</div>
	);
}
