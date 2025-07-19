import { ArrowDown } from "lucide-react";
import {
	Button,
	DropdownMenu,
	DropdownMenuContent,
	DropdownMenuItem,
	DropdownMenuTrigger,
} from "@/components";
import { ThemeSwitcher } from "../ThemeSwitcher";

export const Header = () => {
	return (
		<div className="w-full flex flex-row justify-between items-center my-12">
			<DropdownMenu>
				<DropdownMenuTrigger asChild>
					<div className="relative inline-block rounded-lg">
						<div className="absolute inset-0 rounded-lg border-2 border-primary border-solid animate-pulse" />
						<Button
							variant="outline"
							className="relative flex items-center gap-2 rounded-lg px-4 py-2 transition-all duration-75"
						>
							<h3 className="font-semibold">Aivora</h3>
							<ArrowDown className="size-3 animate-bounce" />
						</Button>
					</div>
				</DropdownMenuTrigger>
				<DropdownMenuContent align="start">
					<DropdownMenuItem>
						<h3>Personal Finance Agent</h3>
					</DropdownMenuItem>
				</DropdownMenuContent>
			</DropdownMenu>
			<div className="flex flex-row items-center gap-4 ">
				<Button>SignUp</Button>
				<Button>Login</Button>
				<ThemeSwitcher />
			</div>
		</div>
	);
};
