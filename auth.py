import os
import streamlit as st
import json

# Mendapatkan path absolut ke direktori skrip
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
USER_DATA_PATH = os.path.join(SCRIPT_DIR, "G:/analisis_sentiment/user_data.json")

# Load user data from local storage
def load_user_data():
    try:
        with open(USER_DATA_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        st.warning("File user_data.json tidak ditemukan. Pembuatan file baru.")
        return {}

# Save user data to local storage
def save_user_data(user_data):
    with open(USER_DATA_PATH, "w") as f:
        json.dump(user_data, f)

# Fungsi untuk melakukan login
def perform_login(username, password):
    # Load existing user data
    user_data = load_user_data()

    if username not in user_data:
        st.error("Username tidak ditemukan.")
    elif user_data[username]["password"] != password:
        st.error("Password salah.")
    else:
        st.session_state.is_logged_in = True
        st.session_state.username = username
        st.success(f"Selamat datang, {username}!")
        st.experimental_rerun()  # Redirect to home page

# Fungsi untuk halaman login
def login():
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        perform_login(username, password)

# Fungsi untuk halaman registrasi
def register():
    # Load existing user data
    user_data = load_user_data()

    new_username = st.text_input("Masukkan Username:")
    new_password = st.text_input("Masukkan Password:", type="password")
    confirm_password = st.text_input("Konfirmasi Password:", type="password")

    if st.button("Registrasi"):
        if new_password != confirm_password:
            st.error("Password yang Anda masukkan tidak cocok.")
        elif new_username in user_data:
            st.error("Username sudah digunakan. Silakan pilih yang lain.")
        else:
            # Simpan data pengguna
            user_data[new_username] = {"password": new_password}
            save_user_data(user_data)
            st.success("Registrasi berhasil!")
            st.session_state.is_logged_in = True  # Set is_logged_in to True after successful registration
            st.session_state.username = new_username  # Set the username
            st.experimental_rerun()  # Redirect to home page
