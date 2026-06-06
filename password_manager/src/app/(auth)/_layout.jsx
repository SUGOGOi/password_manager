// src/app/(auth)/_layout.jsx
import { Stack } from 'expo-router';

export default function AuthLayout() {
    return (
        <Stack
            screenOptions={{
                headerShown: false, // Hides the native header bar for a clean custom UI
                animation: 'fade',  // Smooth transition between login and registration
            }}
        />
    );
}