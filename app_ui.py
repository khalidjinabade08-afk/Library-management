import streamlit as st
import base64
import requests 
import pandas as pd
import os

login_URL = "http://127.0.0.1:5501/Admin"

base_url = "http://127.0.0.1:5501"

st.set_page_config(page_title="library management system", layout="wide")


def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

path_img = r"K:\Program Files\Library management\images\IMG_20260601_174954.jpg"

if os.path.isfile(path_img):
    bin_str = get_base64(path_img)
    st.markdown(
        f"""
        <style>
        .stApp {{
            flex: 1;
            background-image: url('data:image/jpeg;base64,{bin_str}'); 
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        [data-testid="stHeader]{{
        background: rgb(0,0,0,0);
        }}
        
        [data-testid='stToolbar']{{
        right: 2perm
        }}
    </style>
""", unsafe_allow_html=True
    )

def init_session():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user_data" not in st.session_state:
        st.session_state.user_data = None

def login_user(name, username, password, role):
    try:
        response = requests.post(
            f"{login_URL}/login", json={"name":name, "username":username, "password":password, "role":role }
        )
        if response.status_code == 200:
            st.session_state.authenticated = True
            st.session_state.user_data = response.json().get("data",{})
            st.rerun()
        else:
            st.error("Invalid credentials")
    except Exception as e:
        st.error(f"connectionn error:{e}")


init_session()

tab1, tab2 = st.tabs(["Login", "Register"])

with tab1:
    with st.form("login_form", clear_on_submit=False):
            st.markdown(
                '<div class="form-heading">Welcome Back</div>', unsafe_allow_html=True
            )

            email = st.text_input("Email Address", placeholder="name@company.com")
            password = st.text_input(
                "Password", type="password", placeholder="••••••••"
            )
            submit = st.form_submit_button("Sign In")

            if submit:
                login_user(email, password)

    with tab2:
        with st.form("reg_form", clear_on_submit=False):
            st.markdown(
                '<div class="form-heading">Create Account</div>', unsafe_allow_html=True
            )

            u_name = st.text_input("Full Name", placeholder="user")
            u_email = st.text_input(
                "Work Email Address", placeholder="name@company.com"
            )
            u_pass = st.text_input(
                "Password", type="password", placeholder="Minimum 6 characters"
            )
            u_role = st.selectbox(
                "Organizational Role", ["admin", "superadmin"]
            )
            submit_reg = st.form_submit_button("Create Account")

            if submit_reg:
                login_user(u_name, u_username, u_password, u_role)
                st.success("Registered!")

if not st.session_state.authenticated:
    cols = st.columns([1, 2, 1])
    with cols[1]:
        auth_page()
else:
    # main_dashboard() 
    pass