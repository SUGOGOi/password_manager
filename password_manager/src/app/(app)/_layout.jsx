// src/app/(app)/_layout.jsx
import { Stack } from 'expo-router';

export default function AppLayout() {
    return (
        <Stack
            screenOptions={{
                headerShown: false, // Keeps your custom header layout clean
            }}
        />
    );
}