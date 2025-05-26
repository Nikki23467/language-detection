import streamlit as st
import hashlib
import json
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("MY_API_KEY")
if not API_KEY:
    st.error("❗ API key not found. Please set MY_API_KEY in your .env file.")
    st.stop()

# Gemini API details
MODEL = "gemini-2.0-flash"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

# User data file
USER_DATA_FILE = "users.json"

def load_users():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_DATA_FILE, "w") as f:
        json.dump(users, f)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    users = load_users()
    if username in users:
        return False, "🚫 Username already exists."
    users[username] = hash_password(password)
    save_users(users)
    return True, "✅ Registration successful! Please login."

def authenticate_user(username, password):
    users = load_users()
    return username in users and users[username] == hash_password(password)

def show_login():
    with st.container():
        st.markdown("## 🔐 Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login", use_container_width=True):
            if authenticate_user(username, password):
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.success(f"🎉 Welcome back, **{username}**!")
                st.stop()  # stops current run, triggers rerun
            else:
                st.error("❌ Invalid username or password")

def show_register():
    with st.container():
        st.markdown("## 📝 Register")
        username = st.text_input("Choose a username", key="reg_username")
        password = st.text_input("Choose a password", type="password", key="reg_password")
        password_confirm = st.text_input("Confirm password", type="password", key="reg_password_confirm")
        if st.button("Register", use_container_width=True):
            if password != password_confirm:
                st.error("❗Passwords do not match")
            elif not username.strip() or not password.strip():
                st.error("❗Username and password cannot be empty")
            else:
                success, msg = register_user(username.strip(), password)
                if success:
                    st.success(msg)
                else:
                    st.error(msg)

def show_language_detector():
    st.markdown("### 🌍 Language Detection")
    st.write("Enter text and detect its language.")
    user_input = st.text_area("✏️ Enter text here:", height=150)
    if st.button("🔍 Detect Language", use_container_width=True):
        if user_input.strip():
            with st.spinner("⏳ Detecting language..."):
                data = {
                    "contents": [
                        {
                            "parts": [
                                {
                                    "text": f"What language is this sentence written in?\n\n\"{user_input}\""
                                }
                            ]
                        }
                    ]
                }
                response = requests.post(API_URL, headers={"Content-Type": "application/json"}, json=data)
                if response.status_code == 200:
                    result = response.json()
                    output_text = result["candidates"][0]["content"]["parts"][0]["text"]
                    st.success("✅ Language Detected:")
                    st.markdown(f"**{output_text.strip()}**")
                else:
                    st.error(f"❌ API Error: {response.status_code} - {response.text}")
        else:
            st.warning("⚠️ Please enter some text.")

def main():
    # Must be the very first Streamlit command!
    st.set_page_config(page_title="Language Detector", page_icon="🌐", layout="centered")

    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🌐 Language Detector App</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Secure login system | Implemented using GEMINI AI</p>", unsafe_allow_html=True)
    st.divider()

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['username'] = ""

    with st.sidebar:
        st.markdown("### 🔑 Authentication")
        st.info("⚠️ Note: You may need to click the **Login** or **Logout** button twice for it to take effect.")
        if st.session_state['logged_in']:
            st.success(f"👋 Welcome, {st.session_state['username']}!")
            if st.button("🚪 Logout"):
                st.session_state['logged_in'] = False
                st.session_state['username'] = ""
                st.stop()
        else:
            choice = st.radio("Choose action:", ["Login", "Register"])
            st.info("🛡️ Your credentials are stored securely.")

    if st.session_state['logged_in']:
        show_language_detector()
    else:
        if choice == "Login":
            show_login()
        else:
            show_register()

    st.markdown("""
        <hr style="margin-top: 3rem;">
        <div style='text-align: center; font-size: 0.9rem; color: gray;'>
            © 2025 All rights reserved | Developed by using<strong style='color:#4CAF50;'> GEMINI AI</strong>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
