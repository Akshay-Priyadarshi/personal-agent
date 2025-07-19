"use client";

import { useForm } from "@tanstack/react-form";
import { z } from "zod";
import { Button, Input } from "@/components/ui";
import { betterAuthClient } from "@/lib/auth-client";

const signupFormSchema = z.object({
	email: z.email(),
	password: z.string(),
	fullName: z.string().min(1, "Full name is required"),
});

const defaultValues: z.infer<typeof signupFormSchema> = {
	email: "",
	password: "",
	fullName: "",
};

const SignupForm = () => {
	const form = useForm({
		defaultValues: defaultValues,
		onSubmit: async ({ value }) => {
			console.log("Form submitted with values:", value);
			const { data, error } = await betterAuthClient.signUp.email({
				email: value.email,
				password: value.password,
				name: value.fullName,
				callbackURL: "/dashboard",
			});
			console.log("Signup response:", data, error);
		},
	});

	return (
		<form
			className="w-screen flex flex-col space-y-4 p-4 border-gray-50 border rounded-xl"
			onSubmit={(e) => {
				e.preventDefault();
				form.handleSubmit(e);
			}}
		>
			<h1 className="text-2xl font-bold">Register Here</h1>
			<label htmlFor="email">Email</label>
			<form.Field name="email">
				{(field) => (
					<Input
						id="email"
						name="email"
						type="email"
						placeholder="Email"
						value={field.state.value}
						onChange={(e) => field.handleChange(e.target.value)}
					/>
				)}
			</form.Field>

			<label htmlFor="password">Password</label>
			<form.Field name="password">
				{(field) => (
					<Input
						id="password"
						name="password"
						type="password"
						placeholder="Password"
						value={field.state.value}
						onChange={(e) => field.handleChange(e.target.value)}
					/>
				)}
			</form.Field>

			<label htmlFor="fullName">Full Name</label>
			<form.Field name="fullName">
				{(field) => (
					<Input
						id="fullName"
						name="fullName"
						type="text"
						placeholder="Full Name"
						value={field.state.value}
						onChange={(e) => field.handleChange(e.target.value)}
					/>
				)}
			</form.Field>
			<Button type="submit" variant={"default"}>
				SignUp
			</Button>
			<p className="text-muted-foreground">
				Already have an account?{" "}
				<a href="/login" className="hover:underline">
					Login
				</a>
			</p>
		</form>
	);
};

export default SignupForm;
