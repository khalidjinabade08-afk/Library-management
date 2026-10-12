import streamlit as st
import requests

# Page configuration
st.set_page_config(
    page_title="Library Management System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_URL = "http://127.0.0.1:5501"
AUTH_URL = f"{BASE_URL}/auth"


def apply_simple_style():
    """Injects a modern, aesthetic, and vibrant stylesheet without being overwhelming."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

        html, body, [class*="css"], .stApp {
            font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
            color: #f1f5f9 !important;
        }

        /* Ambient luxury dark background */
        .stApp {
            background-color: #0b0f19 !important;
            background-image: 
                radial-gradient(at 15% 15%, rgba(99, 102, 241, 0.12) 0px, transparent 45%),
                radial-gradient(at 85% 20%, rgba(6, 182, 212, 0.08) 0px, transparent 40%),
                radial-gradient(at 50% 90%, rgba(139, 92, 246, 0.08) 0px, transparent 50%) !important;
            background-attachment: fixed !important;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #0d1322 !important;
            border-right: 1px solid rgba(255, 255, 255, 0.07) !important;
        }

        .brand-header {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 8px 4px 18px 4px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            margin-bottom: 16px;
        }

        .brand-icon {
            width: 44px;
            height: 44px;
            border-radius: 12px;
            background: linear-gradient(135deg, #6366f1 0%, #06b6d4 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
            box-shadow: 0 4px 18px rgba(99, 102, 241, 0.45);
            flex-shrink: 0;
        }

        .brand-text h3 {
            margin: 0 !important;
            font-size: 18px !important;
            font-weight: 800 !important;
            letter-spacing: -0.4px;
            line-height: 1.2 !important;
            background: linear-gradient(135deg, #ffffff 40%, #c7d2fe 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .brand-text p {
            margin: 2px 0 0 0 !important;
            font-size: 11px !important;
            color: #94a3b8 !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            letter-spacing: 0.8px;
        }

        .user-card {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 12px 14px;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            margin-bottom: 18px;
            backdrop-filter: blur(10px);
        }

        .user-card-left {
            display: flex;
            align-items: center;
            gap: 10px;
            overflow: hidden;
        }

        .user-avatar {
            width: 34px;
            height: 34px;
            border-radius: 50%;
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            color: #ffffff;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 14px;
            flex-shrink: 0;
            box-shadow: 0 0 10px rgba(99, 102, 241, 0.4);
        }

        .user-info-name {
            font-size: 13.5px;
            font-weight: 600;
            color: #f8fafc;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .user-info-role {
            font-size: 10.5px;
            color: #a5b4fc;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.6px;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: #10b981;
            box-shadow: 0 0 8px #10b981;
            flex-shrink: 0;
        }

        .nav-header {
            font-size: 11px !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            letter-spacing: 1.2px !important;
            color: #64748b !important;
            margin: 16px 0 8px 6px !important;
        }

        /* Navigation Menu Pills */
        [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] {
            gap: 4px !important;
        }

        [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label > div:first-child {
            display: none !important;
        }

        [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label {
            padding: 10px 14px !important;
            border-radius: 10px !important;
            cursor: pointer !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
            border: 1px solid transparent !important;
            margin-bottom: 2px !important;
            display: flex !important;
            align-items: center !important;
            background: transparent !important;
        }

        [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label p {
            font-size: 13.5px !important;
            font-weight: 500 !important;
            color: #94a3b8 !important;
            margin: 0 !important;
            transition: color 0.15s ease !important;
        }

        [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label:hover {
            background-color: rgba(99, 102, 241, 0.1) !important;
            transform: translateX(4px);
        }

        [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label:hover p {
            color: #f1f5f9 !important;
        }

        [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label:has(input:checked) {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.28) 0%, rgba(6, 182, 212, 0.15) 100%) !important;
            border: 1px solid rgba(99, 102, 241, 0.45) !important;
            box-shadow: 0 4px 16px -2px rgba(99, 102, 241, 0.3) !important;
        }

        [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label:has(input:checked) p {
            color: #ffffff !important;
            font-weight: 700 !important;
        }

        /* Metric Cards */
        [data-testid="stMetric"] {
            background: rgba(17, 24, 39, 0.75) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-top: 3px solid #6366f1 !important;
            border-radius: 14px !important;
            padding: 18px 22px !important;
            box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.4) !important;
            backdrop-filter: blur(12px) !important;
            transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease !important;
        }

        [data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            border-color: rgba(99, 102, 241, 0.4) !important;
            box-shadow: 0 8px 26px -2px rgba(99, 102, 241, 0.25) !important;
        }

        [data-testid="stMetricLabel"] p {
            color: #94a3b8 !important;
            font-size: 13px !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.6px !important;
        }

        [data-testid="stMetricValue"] div {
            color: #ffffff !important;
            font-size: 28px !important;
            font-weight: 800 !important;
            letter-spacing: -0.5px !important;
        }

        /* Tabs Styling */
        [data-testid="stTabs"] [data-baseweb="tab-list"] {
            background: rgba(15, 23, 42, 0.65) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 12px !important;
            padding: 4px 6px !important;
            gap: 6px !important;
            margin-bottom: 22px !important;
        }

        [data-testid="stTabs"] [data-baseweb="tab"] {
            border-radius: 8px !important;
            padding: 8px 18px !important;
            color: #94a3b8 !important;
            font-weight: 600 !important;
            font-size: 13.5px !important;
            border: none !important;
            background: transparent !important;
            transition: all 0.2s ease !important;
        }

        [data-testid="stTabs"] [data-baseweb="tab"]:hover {
            color: #ffffff !important;
            background: rgba(255, 255, 255, 0.04) !important;
        }

        [data-testid="stTabs"] [aria-selected="true"] {
            background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
            color: #ffffff !important;
            font-weight: 700 !important;
            box-shadow: 0 4px 14px rgba(99, 102, 241, 0.4) !important;
        }

        [data-testid="stTabs"] [data-baseweb="tab-border"] {
            display: none !important;
        }

        [data-testid="stTabs"] [data-baseweb="tab-highlight"] {
            display: none !important;
        }

        /* Primary and Secondary Buttons */
        .stButton > button[kind="primary"],
        .stForm .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
            color: #ffffff !important;
            font-weight: 700 !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 10px 20px !important;
            box-shadow: 0 4px 16px rgba(99, 102, 241, 0.35) !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }

        .stButton > button[kind="primary"]:hover,
        .stForm .stButton > button[kind="primary"]:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 22px rgba(99, 102, 241, 0.55) !important;
            filter: brightness(1.1) !important;
        }

        .stButton > button[kind="secondary"],
        .stButton > button {
            background: rgba(30, 41, 59, 0.7) !important;
            color: #e2e8f0 !important;
            font-weight: 600 !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 10px !important;
            padding: 9px 18px !important;
            transition: all 0.2s ease !important;
        }

        .stButton > button:hover {
            background: rgba(51, 65, 85, 0.85) !important;
            border-color: rgba(99, 102, 241, 0.4) !important;
            transform: translateY(-1px) !important;
            color: #ffffff !important;
        }

        /* Inputs, Selectboxes, DateInputs */
        [data-testid="stTextInput"] input,
        [data-testid="stNumberInput"] input,
        [data-testid="stDateInput"] input,
        [data-testid="stTextArea"] textarea {
            background-color: rgba(15, 23, 42, 0.85) !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            border-radius: 10px !important;
            color: #f8fafc !important;
            font-size: 14px !important;
            padding: 10px 14px !important;
            transition: all 0.2s ease !important;
        }

        [data-testid="stTextInput"] input:focus,
        [data-testid="stNumberInput"] input:focus,
        [data-testid="stDateInput"] input:focus,
        [data-testid="stTextArea"] textarea:focus {
            border-color: #6366f1 !important;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.25) !important;
            background-color: rgba(15, 23, 42, 0.95) !important;
        }

        [data-baseweb="select"] > div {
            background-color: rgba(15, 23, 42, 0.85) !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            border-radius: 10px !important;
            color: #f8fafc !important;
        }

        /* Container Border Styling */
        [data-testid="stVerticalBlockBorderWrapper"] > div {
            background: rgba(17, 24, 39, 0.65) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 14px !important;
            backdrop-filter: blur(12px) !important;
            padding: 18px 22px !important;
        }

        /* Headings */
        h1 {
            color: #ffffff !important;
            font-weight: 800 !important;
            letter-spacing: -0.8px !important;
            font-size: 28px !important;
            margin-bottom: 6px !important;
        }

        h2 {
            color: #f8fafc !important;
            font-weight: 700 !important;
            letter-spacing: -0.5px !important;
        }

        h3 {
            color: #e2e8f0 !important;
            font-weight: 600 !important;
            letter-spacing: -0.3px !important;
        }

        /* Badges */
        .badge-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 3px 12px;
            border-radius: 9999px;
            font-size: 12px;
            font-weight: 600;
        }
        .badge-active {
            background: rgba(16, 185, 129, 0.15);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.3);
        }
        .badge-issued {
            background: rgba(99, 102, 241, 0.15);
            color: #a5b4fc;
            border: 1px solid rgba(99, 102, 241, 0.3);
        }
        .badge-expired {
            background: rgba(244, 63, 94, 0.15);
            color: #fb7185;
            border: 1px solid rgba(244, 63, 94, 0.3);
        }

        /* Hide Streamlit default decoration */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True,
    )


def init_session():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user_data" not in st.session_state:
        st.session_state.user_data = None
    if "cookies" not in st.session_state:
        st.session_state.cookies = {}
    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"


def login_user(username, password):
    if not username.strip() or not password:
        st.warning("Please enter your username and password.")
        return

    try:
        response = requests.post(
            f"{AUTH_URL}/login",
            json={"username": username.strip().lower(), "password": password},
            timeout=8,
        )
        try:
            data = response.json()
        except Exception:
            data = {}

        if response.status_code == 200 and data.get("status") == "success":
            st.session_state.cookies = response.cookies.get_dict()
            st.session_state.authenticated = True
            st.session_state.user_data = data.get("data", {})
            st.toast("Login Successful!", icon="🎉")
            st.rerun()
        else:
            err = data.get("message") or response.text or "Invalid username or password"
            st.error(f"Login failed: {err}")
    except requests.exceptions.ConnectionError:
        st.error(
            f"Cannot connect to the backend server at `{BASE_URL}`. "
            "Please ensure `python app.py` is running."
        )
    except Exception as e:
        st.error(f"Login error: {e}")


def register_user(username, name, password, role):
    if not username.strip() or not name.strip() or not password:
        st.warning("Please fill in all registration fields.")
        return

    payload = {
        "username": username.strip().lower(),
        "name": name.strip(),
        "password": password,
        "role": role,
    }

    try:
        response = requests.post(f"{AUTH_URL}/register", json=payload, timeout=8)
        try:
            data = response.json()
        except Exception:
            data = {}

        if response.status_code in [200, 201] and data.get("status") != "error":
            st.success("Registration successful! You can now log in.")
        else:
            err = data.get("message") or response.text or "Registration failed."
            st.error(f"Registration failed: {err}")
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to backend server. Make sure `python app.py` is running.")
    except Exception as e:
        st.error(f"Registration error: {e}")


def logout():
    st.session_state.authenticated = False
    st.session_state.user_data = None
    st.session_state.cookies = {}
    st.session_state.page = "Dashboard"
    st.rerun()


def auth_page():
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    col_l, col_m, col_r = st.columns([1, 1.4, 1])

    with col_m:
        st.markdown(
            """
            <div style="text-align: center; margin-bottom: 24px;">
                <div style="width: 58px; height: 58px; margin: 0 auto 14px; border-radius: 16px; background: linear-gradient(135deg, #6366f1 0%, #06b6d4 100%); display: flex; align-items: center; justify-content: center; font-size: 28px; box-shadow: 0 8px 30px rgba(99, 102, 241, 0.5);">
                    📚
                </div>
                <h1 style="font-size: 28px; font-weight: 800; margin: 0; background: linear-gradient(135deg, #ffffff 40%, #c7d2fe 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Lumina LMS</h1>
                <p style="color: #94a3b8; font-size: 14px; margin-top: 4px; font-weight: 500;">Next-Gen Library Intelligence & Circulation</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.container(border=True):
            tab1, tab2 = st.tabs(["🔐 Sign In", "✨ Create Account"])

            with tab1:
                with st.form("login_form"):
                    st.markdown("<p style='font-size: 15px; font-weight: 700; color: #f8fafc; margin-bottom: 12px;'>Welcome Back</p>", unsafe_allow_html=True)
                    user_inp = st.text_input("Username", placeholder="e.g. admin", key="log_user")
                    pass_inp = st.text_input(
                        "Password", type="password", placeholder="••••••••", key="log_pass"
                    )
                    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
                    submit_btn = st.form_submit_button("Sign In to Portal", use_container_width=True, type="primary")

                    if submit_btn:
                        login_user(user_inp, pass_inp)

            with tab2:
                with st.form("register_form"):
                    st.markdown("<p style='font-size: 15px; font-weight: 700; color: #f8fafc; margin-bottom: 12px;'>Register New Administrator</p>", unsafe_allow_html=True)
                    name_inp = st.text_input("Full Name", placeholder="e.g. Alex Morgan", key="reg_name")
                    user_reg = st.text_input("Username", placeholder="e.g. amorgan", key="reg_user")
                    pass_reg = st.text_input(
                        "Password", type="password", placeholder="Minimum 6 characters", key="reg_pass"
                    )
                    role_reg = st.selectbox(
                        "Administrative Role", ["admin", "superadmin"], key="reg_role"
                    )
                    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
                    reg_btn = st.form_submit_button("Create Account", use_container_width=True, type="primary")

                    if reg_btn:
                        register_user(user_reg, name_inp, pass_reg, role_reg)

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        try:
            r = requests.get(f"{BASE_URL}/swagger", timeout=2)
            if r.status_code in [200, 308, 404]:
                st.markdown(
                    f"<div style='text-align:center;'><span class='badge-pill badge-active'>● Live Backend</span> <span style='font-size:12px; color:#64748b;'>port 5501</span></div>",
                    unsafe_allow_html=True,
                )
        except Exception:
            st.markdown(
                f"<div style='text-align:center;'><span class='badge-pill badge-expired'>● Backend Offline</span> <span style='font-size:12px; color:#64748b;'>Run python app.py</span></div>",
                unsafe_allow_html=True,
            )


# ---------------- EXECUTION ----------------
apply_simple_style()
init_session()

if not st.session_state.authenticated:
    auth_page()
else:
    import importlib
    import home_ui

    importlib.reload(home_ui)
    home_ui.show_dashboard(logout_callback=logout)

