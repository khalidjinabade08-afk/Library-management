import streamlit as st
import requests
from home_ui import show_dashboard

st.set_page_config(
    page_title="Library Management System", page_icon="📚", layout="wide"
)

base_url = "http://127.0.0.1:5501"
auth_url = f"{base_url}/auth"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "user_data" not in st.session_state:
    st.session_state.user_data = None


def apply_custom_style():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        .stApp {
            background: #0a0f1e;
            color: #e2e8f0;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #080d1a 0%, #0f172a 40%, #111827 100%);
            border-right: 1px solid rgba(59,130,246,0.15);
        }

        [data-testid="stSidebar"] * {
            color: #cbd5e1 !important;
        }

        .library-logo {
            text-align: center;
            padding: 20px 12px 16px;
            margin-bottom: 18px;
            border-radius: 16px;
            background: linear-gradient(135deg, #1d4ed8 0%, #4f46e5 50%, #7c3aed 100%);
            box-shadow: 0 8px 32px rgba(79,70,229,0.45), inset 0 1px 0 rgba(255,255,255,0.12);
            position: relative;
            overflow: hidden;
        }

        .library-logo::before {
            content: '';
            position: absolute;
            top: -40%;
            left: -40%;
            width: 180%;
            height: 180%;
            background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 60%);
            pointer-events: none;
        }

        .library-title {
            font-family: 'Playfair Display', serif;
            font-size: 28px;
            font-weight: 700;
            color: #ffffff !important;
            letter-spacing: -0.5px;
            margin-bottom: 4px;
        }

        .library-subtitle {
            font-size: 11px;
            font-weight: 500;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            color: rgba(255,255,255,0.75) !important;
        }

        .section-header {
            color: #475569 !important;
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin: 18px 0 6px 4px;
            display: block;
        }

        [data-testid="stSidebar"] .stButton > button {
            width: 100%;
            background: transparent;
            color: #94a3b8 !important;
            border: 1px solid transparent;
            border-radius: 10px;
            padding: 10px 14px;
            font-size: 14px;
            font-weight: 500;
            text-align: left;
            transition: all 0.2s ease;
            margin-bottom: 2px;
        }

        [data-testid="stSidebar"] .stButton > button:hover {
            background: linear-gradient(90deg, rgba(79,70,229,0.18), rgba(124,58,237,0.10));
            color: #e2e8f0 !important;
            border-color: rgba(79,70,229,0.35);
            transform: translateX(3px);
            box-shadow: 0 0 0 0;
        }

        [data-testid="stSidebar"] .stButton > button:focus {
            background: linear-gradient(90deg, rgba(79,70,229,0.25), rgba(124,58,237,0.15));
            color: #ffffff !important;
            border-color: rgba(79,70,229,0.5);
            box-shadow: none;
        }

        hr {
            border: none !important;
            height: 1px !important;
            background: linear-gradient(90deg, transparent, rgba(79,70,229,0.3), transparent) !important;
            margin: 12px 0 !important;
        }

        .current-page {
            background: linear-gradient(135deg, rgba(79,70,229,0.15), rgba(124,58,237,0.10));
            border: 1px solid rgba(79,70,229,0.3);
            border-radius: 12px;
            padding: 12px;
            text-align: center;
            margin-top: 18px;
            font-size: 12px;
            color: #a5b4fc !important;
            letter-spacing: 0.3px;
        }

        .main .block-container {
            padding: 1.5rem 2rem 2rem;
            max-width: 1280px;
        }

        h1 {
            font-family: 'Playfair Display', serif;
            font-size: 32px !important;
            font-weight: 700 !important;
            background: linear-gradient(135deg, #e2e8f0, #a5b4fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 4px !important;
        }

        h2, h3 {
            color: #cbd5e1 !important;
            font-weight: 600 !important;
        }

        .glass-card {
            background: linear-gradient(135deg, rgba(15,23,42,0.85), rgba(17,24,39,0.90));
            border: 1px solid rgba(79,70,229,0.2);
            border-radius: 16px;
            padding: 20px 24px;
            margin-bottom: 16px;
            box-shadow: 0 4px 24px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.04);
            backdrop-filter: blur(12px);
        }

        .section-title {
            font-size: 17px;
            font-weight: 700;
            color: #e2e8f0;
            margin-bottom: 14px;
            padding-bottom: 10px;
            border-bottom: 1px solid rgba(79,70,229,0.2);
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .gradient-subheader {
            font-size: 18px;
            font-weight: 700;
            background: linear-gradient(90deg, #818cf8, #c4b5fd);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 20px 0 12px;
            letter-spacing: -0.3px;
        }

        .chart-card {
            background: rgba(15,23,42,0.7);
            border: 1px solid rgba(79,70,229,0.15);
            border-radius: 14px;
            padding: 16px 18px;
            margin-bottom: 12px;
        }

        .category-title {
            font-size: 14px;
            font-weight: 600;
            color: #94a3b8 !important;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-bottom: 10px;
        }

        .main .stButton > button,
        .stForm .stButton > button {
            background: linear-gradient(135deg, #4f46e5, #7c3aed);
            color: #ffffff !important;
            border: none;
            border-radius: 10px;
            padding: 10px 20px;
            font-size: 14px;
            font-weight: 600;
            letter-spacing: 0.3px;
            transition: all 0.2s ease;
            box-shadow: 0 4px 14px rgba(79,70,229,0.35);
        }

        .main .stButton > button:hover,
        .stForm .stButton > button:hover {
            background: linear-gradient(135deg, #4338ca, #6d28d9);
            box-shadow: 0 6px 20px rgba(79,70,229,0.5);
            transform: translateY(-1px);
        }

        .main .stButton > button:active,
        .stForm .stButton > button:active {
            transform: translateY(0);
            box-shadow: 0 2px 8px rgba(79,70,229,0.3);
        }

        [data-testid="stFormSubmitButton"] > button {
            background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 10px 20px !important;
            font-size: 14px !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 14px rgba(79,70,229,0.35) !important;
            transition: all 0.2s ease !important;
        }

        [data-testid="stFormSubmitButton"] > button:hover {
            background: linear-gradient(135deg, #4338ca, #6d28d9) !important;
            box-shadow: 0 6px 20px rgba(79,70,229,0.5) !important;
            transform: translateY(-1px) !important;
        }

        [data-testid="stTextInput"] input,
        [data-testid="stNumberInput"] input,
        [data-testid="stTextArea"] textarea {
            background: rgba(15,23,42,0.8) !important;
            border: 1px solid rgba(79,70,229,0.25) !important;
            border-radius: 10px !important;
            color: #e2e8f0 !important;
            font-size: 14px !important;
            padding: 10px 14px !important;
            transition: border-color 0.2s ease !important;
        }

        [data-testid="stTextInput"] input:focus,
        [data-testid="stNumberInput"] input:focus,
        [data-testid="stTextArea"] textarea:focus {
            border-color: rgba(79,70,229,0.6) !important;
            box-shadow: 0 0 0 3px rgba(79,70,229,0.12) !important;
        }

        [data-testid="stTextInput"] input::placeholder,
        [data-testid="stTextArea"] textarea::placeholder {
            color: #475569 !important;
        }

        [data-testid="stSelectbox"] > div > div {
            background: rgba(15,23,42,0.8) !important;
            border: 1px solid rgba(79,70,229,0.25) !important;
            border-radius: 10px !important;
            color: #e2e8f0 !important;
        }

        [data-testid="stRadio"] label {
            color: #94a3b8 !important;
            font-size: 14px !important;
        }

        [data-testid="stRadio"] label:hover {
            color: #e2e8f0 !important;
        }

        [data-testid="stMetric"] {
            background: linear-gradient(135deg, rgba(15,23,42,0.9), rgba(17,24,39,0.85));
            border: 1px solid rgba(79,70,229,0.2);
            border-radius: 14px;
            padding: 16px 18px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.25);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        [data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(79,70,229,0.2);
            border-color: rgba(79,70,229,0.4);
        }

        [data-testid="stMetricLabel"] {
            color: #64748b !important;
            font-size: 12px !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.8px !important;
        }

        [data-testid="stMetricValue"] {
            color: #e2e8f0 !important;
            font-size: 28px !important;
            font-weight: 700 !important;
        }

        [data-testid="stDataFrame"] {
            border-radius: 12px !important;
            overflow: hidden;
            border: 1px solid rgba(79,70,229,0.2) !important;
        }

        [data-testid="stDataFrame"] iframe {
            border-radius: 12px !important;
        }

        [data-testid="stTabs"] [role="tablist"] {
            background: rgba(15,23,42,0.6);
            border-radius: 12px;
            padding: 4px;
            gap: 2px;
            border: 1px solid rgba(79,70,229,0.15);
        }

        [data-testid="stTabs"] [role="tab"] {
            border-radius: 9px !important;
            color: #64748b !important;
            font-size: 13px !important;
            font-weight: 500 !important;
            padding: 7px 16px !important;
            transition: all 0.2s ease !important;
            border: none !important;
        }

        [data-testid="stTabs"] [role="tab"][aria-selected="true"] {
            background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
            color: #ffffff !important;
            font-weight: 600 !important;
            box-shadow: 0 2px 10px rgba(79,70,229,0.4) !important;
        }

        [data-testid="stTabs"] [role="tab"]:hover:not([aria-selected="true"]) {
            background: rgba(79,70,229,0.1) !important;
            color: #a5b4fc !important;
        }
        
        [data-testid="stAlert"] {
            border-radius: 12px !important;
            border-left-width: 3px !important;
            font-size: 14px !important;
        }

        [data-testid="stDateInput"] input {
            background: rgba(15,23,42,0.8) !important;
            border: 1px solid rgba(79,70,229,0.25) !important;
            border-radius: 10px !important;
            color: #e2e8f0 !important;
        }

        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }

        ::-webkit-scrollbar-track {
            background: rgba(15,23,42,0.4);
        }

        ::-webkit-scrollbar-thumb {
            background: rgba(79,70,229,0.4);
            border-radius: 3px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: rgba(79,70,229,0.65);
        }

        .page-indicator {
            background: rgba(79,70,229,0.12);
            border: 1px solid rgba(79,70,229,0.25);
            border-radius: 8px;
            padding: 8px 16px;
            text-align: center;
            font-size: 14px;
            font-weight: 600;
            color: #a5b4fc;
            display: inline-block;
            width: 100%;
        }

        [data-testid="stForm"] {
            background: rgba(15,23,42,0.5);
            border: 1px solid rgba(79,70,229,0.15);
            border-radius: 14px;
            padding: 16px !important;
        }

        .stCaption {
            color: #475569 !important;
            font-size: 12px !important;
        }

        label, [data-testid="stWidgetLabel"] {
            color: #94a3b8 !important;
            font-size: 13px !important;
            font-weight: 500 !important;
        }

        [data-testid="stNumberInput"] button {
            background: rgba(79,70,229,0.15) !important;
            border: 1px solid rgba(79,70,229,0.2) !important;
            color: #a5b4fc !important;
            border-radius: 6px !important;
        }

        [data-testid="stNumberInput"] button:hover {
            background: rgba(79,70,229,0.3) !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


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
            st.session_state.cookies = response.cookies.get_dict()
            st.session_state.authenticated = True
            st.session_state.user_data = response.json().get("data", {})
            st.success("Login Successful")
            st.rerun()
        else:
            st.error(response.text)
    except Exception as e:
        st.error(f"Connection error: {e}")


def register_user(username, name, password, role):
    payload = {"username": username, "name": name, "password": password, "role": role}
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
        st.error(
            "Cannot connect to the server. Please ensure the backend API is running"
        )
    except Exception as e:
        st.error(f"Connection Error: {e}")


def logout():
    st.session_state.authenticated = False
    st.session_state.user_data = {}
    st.rerun()


def auth_page():
    st.markdown(
        """
        <div class="library-logo">
            <div class="library-title">Library System</div>
            <div class="library-subtitle">Secure Access Portal</div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        with st.form("login_form"):
            st.markdown(
                '<div class="gradient-subheader">Welcome Back</div>',
                unsafe_allow_html=True,
            )
            username = st.text_input(
                "Username", placeholder="Enter Username", key="login_user_key"
            )
            password = st.text_input(
                "Password",
                type="password",
                placeholder="••••••••",
                key="login_pass_key",
            )
            login_btn = st.form_submit_button("Login")

            if login_btn:
                if not username or not password:
                    st.warning("Please fill all fields")
                else:
                    login_user(username, password)

    with tab2:
        with st.form("register_form"):
            st.markdown(
                '<div class="gradient-subheader">Create Account</div>',
                unsafe_allow_html=True,
            )

            name = st.text_input("Full Name")
            username = st.text_input("Username", key="reg_user_key")
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Minimum 6 characters",
                key="reg_pass_key",
            )
            role = st.selectbox(
                "Organizational Role", ["admin", "superadmin"], key="reg_role_key"
            )

            register_btn = st.form_submit_button("Register")

            if register_btn:
                if not name or not username or not password:
                    st.warning("Please fill all fields")
                else:
                    register_user(username, name, password, role)


def dashboard():
    st.markdown("<h1>Library Management System</h1>", unsafe_allow_html=True)
    st.markdown(
        '<div class="gradient-subheader">Dashboard Overview</div>',
        unsafe_allow_html=True,
    )

    user_info = st.session_state.user_data or {}

    st.markdown(
        f"""
        <div class="glass-card">
            <div class="category-title">User Details</div>
            <p style="margin: 0; padding-bottom: 5px;">Welcome, <strong style="color: #ffffff;">{user_info.get('name', 'User')}</strong></p>
            <p style="margin: 0;">Role: <strong style="color: #a5b4fc; text-transform: capitalize;">{user_info.get('role', 'N/A')}</strong></p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    if st.button("Logout", key="logout_btn"):
        logout()


# ----------------- App Execution ----------------- #
apply_custom_style()
init_session()

if not st.session_state.authenticated:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        auth_page()
else:
    show_dashboard()
