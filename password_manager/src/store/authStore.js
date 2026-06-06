import { create } from "zustand";
import * as SecureStore from "expo-secure-store";

export const useAuthStore = create((set) => ({
  isLoggedIn: false,
  userEmail: null,
  isLoading: true, // Used to prevent flashing login screen while checking storage

  // Call this when the app first loads
  checkAuth: async () => {
    try {
      const token = await SecureStore.getItemAsync("userToken");
      const email = await SecureStore.getItemAsync("userEmail");

      if (token && email) {
        set({ isLoggedIn: true, userEmail: email, isLoading: false });
      } else {
        set({ isLoggedIn: false, isLoading: false });
      }
    } catch (error) {
      console.error("Error loading secure store data", error);
      set({ isLoggedIn: false, isLoading: false });
    }
  },

  login: async (email, token) => {
    try {
      // Save data securely on the hardware level
      await SecureStore.setItemAsync("userToken", token);
      await SecureStore.setItemAsync("userEmail", email);

      set({ isLoggedIn: true, userEmail: email });
    } catch (error) {
      console.error("Failed to save auth data", error);
    }
  },

  logout: async () => {
    try {
      // Remove tokens from device storage
      await SecureStore.deleteItemAsync("userToken");
      await SecureStore.deleteItemAsync("userEmail");

      set({ isLoggedIn: false, userEmail: null });
    } catch (error) {
      console.error("Failed to delete auth data", error);
    }
  },
}));
