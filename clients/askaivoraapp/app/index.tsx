import { Text } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

export default function Index() {
	return (
		<SafeAreaView className="h-[100%] bg-purple-800 flex justify-center items-center">
			<Text className="text-4xl text-gray-50">Hello World!</Text>
		</SafeAreaView>
	);
}
