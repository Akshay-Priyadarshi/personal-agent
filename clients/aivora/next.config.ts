import type { NextConfig } from "next";

const APP_ENV = process.env.APP_ENV || "development";

const nextConfig: NextConfig = {
	/* config options here */
	devIndicators:
		APP_ENV === "development" ? { position: "bottom-left" } : false,
};

export default nextConfig;
