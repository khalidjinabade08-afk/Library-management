import streamlit as st
import requests

base_url = "http://127.0.0.1:5501"
auth_url = f"{base_url}/auth"
st.set_page_config(page_title="Library Management System", layout="wide")

def init_session():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user_data" not in st.session_state:
        st.session_state.user_data = None

def login_user(username, password):
    try:
        response = requests.post(
            f"{auth_url}/login", json={"username": username, "password": password}
        )
        if response.status_code == 200:
            st.session_state.authenticated = True
            st.session_state.user_data = response.json().get("data", {})
            st.success("Login Successful")
            st.rerun()
        else:
            st.error(response.text)
    except Exception as e:
        st.error(f"Connection error: {e}")

def register_user(username, name, password, role):
    payload = {
        "username": username,
        "name": name,
        "password": password,
        "role":role
    }
    try:
        response = requests.post(f"{auth_url}/register", json=payload)
        
        if response.status_code in [200, 201]:
            st.success("Registration Successful! Please Login.")
        else:
            try:
                st.error(response.json().get("message", "Registration failed"))
            except Exception:
                st.error(response.text)
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to the server. Please ensure the backend API is running")
    except Exception as e:
        st.error(f"Connection Error: {e}")

def logout():
    st.session_state.authenticated = False
    st.session_state.user_data = {}
    st.rerun()

def auth_page():
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        with st.form("login_form"):
            st.subheader("Login")
            username = st.text_input("Username", placeholder="Enter Username", key="login_user_key")
            password = st.text_input(
                "Password", type="password", placeholder="••••••••", key="login_pass_key"
            )
            login_btn = st.form_submit_button("Login")

            if login_btn:
                if not username or not password:
                    st.warning("Please fill all fields")
                else:
                    login_user(username, password)

    with tab2:
        with st.form("register_form"):
            st.subheader("Create Account")

            name = st.text_input("Full Name")
            username = st.text_input("Username", key="reg_user_key")
            password = st.text_input(
                "Password", type="password", placeholder="Minimum 6 characters", key="reg_pass_key"
            )
            role = st.selectbox("Organizational Role",["admin","superadmin"],key="reg_role_key")

            register_btn = st.form_submit_button("Register")

            if register_btn:
                if not name or not username or not password:
                    st.warning("Please fill all fields")
                else:
                    register_user(username, name, password,role)

def dashboard():
    st.title("Library Management System")

    user_info = st.session_state.user_data or {}
    
    st.write(f"Welcome, **{user_info.get('name', 'User')}**")
    st.write(f"Role: **{user_info.get('role', '')}**")

    if st.button("Logout", key="logout_btn"):
        logout()

init_session()

if not st.session_state.authenticated:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        auth_page()
else:
    dashboard()