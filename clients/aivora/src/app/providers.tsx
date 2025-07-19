"use client";

import type { ReactNode } from "react";
import { ThemeProvider } from "@/components";

export function Providers({ children }: { children: ReactNode }) {
	return (
		<ThemeProvider
			attribute="class"
			defaultTheme="system"
			enableSystem
			disableTransitionOnChange
			storageKey="next-theme"
			enableColorScheme={true}
		>
			{children}
		</ThemeProvider>
	);
}
