// app/(auth)/login.tsx
import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet } from 'react-native';
import { useRouter } from 'expo-router';
import Toast from 'react-native-toast-message';
import { useAuthStore } from '../../store/authStore';


export default function LoginScreen() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const login = useAuthStore((state) => state.login);
    const router = useRouter();


    // Inside app/(auth)/login.jsx

    const handleEmailLogin = async () => {
        if (!email || !password) {
            Toast.show({ type: 'error', text1: 'Error', text2: 'Please fill all fields' });
            return;
        }

        // Simulation: Replace this later with your fetch python backend call
        const mockTokenFromBackend = "my_secure_generated_api_token_123";

        // Call updated store action which now saves to device storage
        await login(email, mockTokenFromBackend);

        Toast.show({ type: 'success', text1: 'Welcome back!' });
    };

    const handleGoogleLogin = () => {
        // Simulate Google Login
        login('google-user@gmail.com');
        Toast.show({ type: 'success', text1: 'Logged in with Google' });
    };

    return (
        <View style={styles.container}>
            <Text style={styles.title}>Password Manager</Text>

            <TextInput
                style={styles.input}
                placeholder="Email"
                value={email}
                onChangeText={setEmail}
                autoCapitalize="none"
                keyboardType="email-address"
            />
            <TextInput
                style={styles.input}
                placeholder="Password"
                secureTextEntry
                value={password}
                onChangeText={setPassword}
            />

            <TouchableOpacity style={styles.button} onPress={handleEmailLogin}>
                <Text style={styles.buttonText}>Login</Text>
            </TouchableOpacity>

            <TouchableOpacity style={[styles.button, styles.googleButton]} onPress={handleGoogleLogin}>
                <Text style={styles.googleButtonText}>Continue with Google</Text>
            </TouchableOpacity>

            <TouchableOpacity onPress={() => router.push('/(auth)/register')}>
                <Text style={styles.linkText}>Don't have an account? Register</Text>
            </TouchableOpacity>
        </View>
    );
}

// Simple styling standard fallback style sheet for clean demonstration
const styles = StyleSheet.create({
    container: { flex: 1, justifyContent: 'center', padding: 24, backgroundColor: '#f9fafb' },
    title: { fontSize: 28, fontWeight: 'bold', marginBottom: 32, textAlign: 'center', color: '#111827' },
    input: { backgroundColor: '#fff', padding: 16, borderRadius: 8, marginBottom: 16, borderWidth: 1, borderColor: '#e5e7eb' },
    button: { backgroundColor: '#2563eb', padding: 16, borderRadius: 8, alignItems: 'center', marginBottom: 12 },
    buttonText: { color: '#fff', fontWeight: 'bold', fontSize: 16 },
    googleButton: { backgroundColor: '#fff', borderWidth: 1, borderColor: '#d1d5db' },
    googleButtonText: { color: '#374151', fontWeight: 'bold', fontSize: 16 },
    linkText: { color: '#2563eb', textAlign: 'center', marginTop: 16 },
});