// app/(app)/index.tsx
import React, { useState } from 'react';
import { View, Text, FlatList, TextInput, TouchableOpacity, StyleSheet, Modal } from 'react-native';
import { useAuthStore } from '../../store/authStore';
import { Eye, EyeOff, LogOut, Plus, Trash2 } from 'lucide-react-native';
import Toast from 'react-native-toast-message';

// Dummy initial structural data
const INITIAL_DATA = [
    { id: '1', site: 'Google', user: 'sumsum@gmail.com', pass: 'secret123' },
    { id: '2', site: 'GitHub', user: 'sumsumgogoi', pass: 'gitpass456' },
];

export default function Dashboard() {
    const logout = useAuthStore((state) => state.logout);
    const userEmail = useAuthStore((state) => state.userEmail);
    const [passwords, setPasswords] = useState(INITIAL_DATA);
    const [visiblePasswords, setVisiblePasswords] = useState({});

    // Modal states for adding a new password
    const [modalVisible, setModalVisible] = useState(false);
    const [newSite, setNewSite] = useState('');
    const [newUser, setNewUser] = useState('');
    const [newPass, setNewPass] = useState('');

    const toggleVisibility = (id) => {
        setVisiblePasswords(prev => ({ ...prev, [id]: !prev[id] }));
    };

    const handleAddPassword = () => {
        if (!newSite || !newUser || !newPass) {
            Toast.show({ type: 'error', text1: 'Error', text2: 'All fields are required' });
            return;
        }
        const newItem = { id: Date.now().toString(), site: newSite, user: newUser, pass: newPass };
        setPasswords([newItem, ...passwords]);
        setModalVisible(false);
        setNewSite(''); setNewUser(''); setNewPass('');
        Toast.show({ type: 'success', text1: 'Saved!', text2: 'Credentials added successfully.' });
    };

    const handleDelete = (id) => {
        setPasswords(passwords.filter(item => item.id !== id));
        Toast.show({ type: 'info', text1: 'Deleted successfully' });
    };

    return (
        <View style={styles.container}>
            {/* Header section */}
            <View style={styles.header}>
                <View>
                    <Text style={styles.welcomeText}>Vault</Text>
                    <Text style={styles.userText}>{userEmail}</Text>
                </View>
                <TouchableOpacity onPress={logout} style={styles.logoutButton}>
                    <LogOut color="#ef4444" size={20} />
                </TouchableOpacity>
            </View>

            {/* Passwords List */}
            <FlatList
                data={passwords}
                keyExtractor={(item) => item.id}
                renderItem={({ item }) => (
                    <View style={styles.card}>
                        <View style={{ flex: 1 }}>
                            <Text style={styles.siteText}>{item.site}</Text>
                            <Text style={styles.usernameText}>User: {item.user}</Text>
                            <Text style={styles.passwordText}>
                                Password: {visiblePasswords[item.id] ? item.pass : '••••••••'}
                            </Text>
                        </View>
                        <View style={styles.actionGroup}>
                            <TouchableOpacity onPress={() => toggleVisibility(item.id)} style={styles.iconBtn}>
                                {visiblePasswords[item.id] ? <EyeOff color="#6b7280" size={20} /> : <Eye color="#6b7280" size={20} />}
                            </TouchableOpacity>
                            <TouchableOpacity onPress={() => handleDelete(item.id)} style={styles.iconBtn}>
                                <Trash2 color="#ef4444" size={20} />
                            </TouchableOpacity>
                        </View>
                    </View>
                )}
            />

            {/* Floating Action Button to Add Password */}
            <TouchableOpacity style={styles.fab} onPress={() => setModalVisible(true)}>
                <Plus color="#fff" size={24} />
            </TouchableOpacity>

            {/* Simple Add Credentials Modal Box */}
            <Modal visible={modalVisible} animationType="slide" transparent>
                <View style={styles.modalOverlay}>
                    <View style={styles.modalContent}>
                        <Text style={styles.modalTitle}>Add New Password</Text>
                        <TextInput style={styles.input} placeholder="Site/App Name (e.g. Netflix)" value={newSite} onChangeText={setNewSite} />
                        <TextInput style={styles.input} placeholder="Username / Email" value={newUser} onChangeText={setNewUser} autoCapitalize="none" />
                        <TextInput style={styles.input} placeholder="Password" secureTextEntry value={newPass} onChangeText={setNewPass} />

                        <View style={styles.modalActions}>
                            <TouchableOpacity style={[styles.modalBtn, styles.cancelBtn]} onPress={() => setModalVisible(false)}>
                                <Text style={styles.cancelBtnText}>Cancel</Text>
                            </TouchableOpacity>
                            <TouchableOpacity style={[styles.modalBtn, styles.saveBtn]} onPress={handleAddPassword}>
                                <Text style={styles.saveBtnText}>Save</Text>
                            </TouchableOpacity>
                        </View>
                    </View>
                </View>
            </Modal>
        </View>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, backgroundColor: '#f3f4f6', paddingTop: 60, paddingHorizontal: 16 },
    header: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 },
    welcomeText: { fontSize: 24, fontWeight: 'bold', color: '#111827' },
    userText: { fontSize: 14, color: '#6b7280' },
    logoutButton: { padding: 8, backgroundColor: '#fee2e2', borderRadius: 8 },
    card: { backgroundColor: '#fff', padding: 16, borderRadius: 12, marginBottom: 12, flexDirection: 'row', alignItems: 'center', shadowColor: '#000', shadowOffset: { width: 0, height: 1 }, shadowOpacity: 0.1, shadowRadius: 2, elevation: 2 },
    siteText: { fontSize: 18, fontWeight: 'bold', color: '#1f2937', marginBottom: 4 },
    usernameText: { fontSize: 14, color: '#4b5563' },
    passwordText: { fontSize: 14, color: '#9ca3af', marginTop: 2 },
    actionGroup: { flexDirection: 'row', gap: 12 },
    iconBtn: { padding: 8 },
    fab: { position: 'absolute', bottom: 24, right: 24, backgroundColor: '#2563eb', width: 56, height: 56, borderRadius: 28, justifyContent: 'center', alignItems: 'center', elevation: 4 },
    modalOverlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.5)', justifyContent: 'center', padding: 20 },
    modalContent: { backgroundColor: '#fff', padding: 24, borderRadius: 16 },
    modalTitle: { fontSize: 20, fontWeight: 'bold', marginBottom: 16 },
    input: { backgroundColor: '#f9fafb', padding: 14, borderRadius: 8, marginBottom: 12, borderWidth: 1, borderColor: '#e5e7eb' },
    modalActions: { flexDirection: 'row', justifyContent: 'flex-end', gap: 12, marginTop: 12 },
    modalBtn: { paddingVertical: 12, paddingHorizontal: 20, borderRadius: 8 },
    cancelBtn: { backgroundColor: '#f3f4f6' },
    cancelBtnText: { color: '#4b5563', fontWeight: 'bold' },
    saveBtn: { backgroundColor: '#2563eb' },
    saveBtnText: { color: '#fff', fontWeight: 'bold' },
});