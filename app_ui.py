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

def login_user(name,username, password, role):
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