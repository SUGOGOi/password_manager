// src/app/_layout.jsx
import { Stack, useRouter, useSegments } from 'expo-router';
import { useEffect } from 'react';
import { ActivityIndicator, View } from 'react-native';
import Toast from 'react-native-toast-message';
import { useAuthStore } from '../store/authStore';



export default function RootLayout() {
  // Option A (Safer): Grab the exact state items safely
  const isLoggedIn = useAuthStore((state) => state.isLoggedIn);
  const isLoading = useAuthStore((state) => state.isLoading);
  const checkAuth = useAuthStore((state) => state.checkAuth);

  const segments = useSegments();
  const router = useRouter();

  useEffect(() => {
    // Test if checkAuth actually exists before calling it to prevent crash
    if (typeof checkAuth === 'function') {
      checkAuth();
    } else {
      console.error("🔴 checkAuth is undefined! Check your store export.");
    }
  }, []); // Safe empty dependency array to run once on load

  useEffect(() => {
    if (isLoading) return;

    const inAuthGroup = segments[0] === '(auth)';

    if (!isLoggedIn && !inAuthGroup) {
      router.replace('/(auth)/login');
    } else if (isLoggedIn && inAuthGroup) {
      router.replace('/(app)');
    }
  }, [isLoggedIn, segments, isLoading]);

  if (isLoading) {
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
        <ActivityIndicator size="large" color="#2563eb" />
      </View>
    );
  }

  return (
    <>
      <Stack screenOptions={{ headerShown: false }}>
        <Stack.Screen name="(auth)" />
        <Stack.Screen name="(app)" />
      </Stack>
      <Toast />
    </>
  );
}