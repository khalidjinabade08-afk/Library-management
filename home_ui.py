import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def show_dashboard():
    base_url = "http://127.0.0.1:5501"
    book_url = f"{base_url}/book"
    member_url = f"{base_url}/member"

    st.set_page_config(page_title="Bookary Library", page_icon="📚", layout="wide")

    # ---------------- CUSTOM CSS ----------------
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

    if "page" not in st.session_state:
        st.session_state.page = "Overview"

    with st.sidebar:

        st.markdown(
            """
        <div class="library-logo">
            <div class="library-title">📖 Bookary</div>
            <div class="library-subtitle">
                Library Management System
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="section-header">MAIN MENU</div>', unsafe_allow_html=True
        )

        if st.button("🏠 Overview", use_container_width=True):
            st.session_state.page = "Overview"

        if st.button("📚 Books", use_container_width=True):
            st.session_state.page = "Books"

        if st.button("🔄 Library Activities", use_container_width=True):
            st.session_state.page = "Transaction"

        if st.button("👥 Members", use_container_width=True):
            st.session_state.page = "Member"

        st.divider()

        st.markdown(
            '<div class="section-header">MANAGEMENT</div>', unsafe_allow_html=True
        )

        if st.button("🎫 Membership", use_container_width=True):
            st.session_state.page = "Management"

        if st.button("➕ Add Books", use_container_width=True):
            st.session_state.page = "Add Book"

        if st.button("💰 Fines", use_container_width=True):
            st.session_state.page = "Fines"

        st.divider()

        st.markdown(
            '<div class="section-header">SETTINGS & OTHERS</div>',
            unsafe_allow_html=True,
        )

        if st.button("⚙️ Settings", use_container_width=True):
            st.session_state.page = "Setting"

        if st.button("👤 Profile", use_container_width=True):
            st.session_state.page = "Profile"

    page = st.session_state.page

    st.title(page)
    st.write(f"Welcome to the **{page}** page.")

    # --- Overview / Dashboard ---
    if page == "Overview":
        st.markdown(
            "<h3 style='color:#cbd5e1; font-family: Inter, sans-serif; font-weight:600; margin-bottom:16px;'>Dashboard Overview</h3>",
            unsafe_allow_html=True,
        )

        # --- TABS CREATION ---
        tab1, tab2, tab3 = st.tabs(
            ["Books Summary", "member & membership summary", "Transaction summary"]
        )

        with tab1:
            st.subheader("Books Summary")

            try:
                response = requests.get(
                    f"{base_url}/book/show", params={"page": 1, "per_page": 1000}
                )
                if response.status_code == 200:
                    data = response.json().get("message", {})
                    books = data.get("title", [])

                    if books:
                        df = pd.DataFrame(books)
                        category_counts = pd.Series(dtype=int)

                        if "category" in df.columns and "quantity" in df.columns:
                            df["category"] = df["category"].fillna("Unknown")
                            category_counts = (
                                df.groupby("category")["quantity"].sum().sort_index()
                            )

                        total_books_count = data.get("total records", len(df))

                        if "status" in df.columns:
                            available_books_count = len(df[df["status"] == "Available"])
                        elif "borrowed" in df.columns:
                            available_books_count = total_books_count - data.get(
                                "borrowed", 0
                            )
                        else:
                            api_available = data.get("available books", 0)
                            available_books_count = (
                                api_available
                                if api_available <= total_books_count
                                else total_books_count
                            )

                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total Books", total_books_count)
                        with col2:
                            st.metric("Available Books", available_books_count)
                        with col3:
                            st.metric("Total Categories", len(category_counts))

                        st.divider()

                        st.subheader("Book Distribution by Category")

                        if not category_counts.empty:
                            left_spacer, center_col, right_spacer = st.columns(
                                [1, 2, 1]
                            )

                            with center_col:
                                fig, ax = plt.subplots(figsize=(6, 4), facecolor="none")

                                colors = [
                                    "#3b82f6",
                                    "#8b5cf6",
                                    "#60a5fa",
                                    "#a78bfa",
                                    "#2563eb",
                                    "#7c3aed",
                                    "#1d4ed8",
                                    "#6d28d9",
                                ]

                                ax.pie(
                                    category_counts,
                                    labels=category_counts.index,
                                    autopct="%1.1f%%",
                                    startangle=140,
                                    colors=colors[: len(category_counts)],
                                    radius=0.95,
                                    labeldistance=1.15,
                                    pctdistance=0.65,
                                    textprops={
                                        "color": "white",
                                        "fontsize": 10,
                                        "weight": "bold",
                                    },
                                    wedgeprops={
                                        "edgecolor": "#0f172a",
                                        "linewidth": 2,
                                    },
                                )
                                ax.axis("equal")

                                st.pyplot(fig, use_container_width=True)
                        else:
                            st.info("No category data found in the records.")
                    else:
                        st.warning("No books available in the library yet.")
                else:
                    st.error(
                        f"Failed to load books. Status Code: {response.status_code}\nResponse: {response.text}"
                    )
            except Exception as e:
                st.error(f"Error generating books summary: {e}")

        with tab2:
            st.subheader("Member & Membership Summary")

            try:
                member_res = requests.get(
                    f"{member_url}/show", params={"page": 1, "per_page": 1000}
                )
                membership_res = requests.get(
                    f"{member_url}/membership/show",
                    params={"page": 1, "per_page": 1000},
                )

                total_members = 0
                members_data = []

                if member_res.status_code == 200:
                    mem_json = member_res.json()
                    total_members = mem_json.get("total no", 0)
                    members_data = mem_json.get("Members", [])

                if membership_res.status_code == 200:
                    res_json = membership_res.json()
                    data = res_json.get("data", res_json)
                    memberships = data.get("memberships", [])

                    if memberships:
                        df_m = pd.DataFrame(memberships)
                        active_count = (
                            (df_m["status"] == "active").sum()
                            if "status" in df_m.columns
                            else 0
                        )
                        expired_count = (
                            (df_m["status"] == "expired").sum()
                            if "status" in df_m.columns
                            else 0
                        )
                        type_counts = (
                            df_m["membership_type"].value_counts()
                            if "membership_type" in df_m.columns
                            else pd.Series(dtype=int)
                        )

                        col1, col2 = st.columns([1, 2])

                        with col1:
                            st.metric("Total Members", total_members)
                            st.metric("Active Memberships", int(active_count))
                            st.metric("Expired Memberships", int(expired_count))

                        with col2:
                            st.markdown(
                                '<div class="chart-card">', unsafe_allow_html=True
                            )
                            st.markdown(
                                "<p class='category-title'>Membership Plans Distribution</p>",
                                unsafe_allow_html=True,
                            )
                            if not type_counts.empty:
                                fig, ax = plt.subplots(figsize=(3, 2), facecolor="none")

                                ax.pie(
                                    type_counts,
                                    labels=type_counts.index,
                                    autopct="%1.1f%%",
                                    startangle=140,
                                    colors=colors[: len(type_counts)],
                                    radius=0.8,
                                    labeldistance=1.2,
                                    textprops={"color": "#cbd5e1", "fontsize": 5},
                                    wedgeprops={"edgecolor": "black", "linewidth": 1.5},
                                )

                                ax.axis("equal")
                                plt.tight_layout()

                                st.pyplot(fig, use_container_width=True)
                            else:
                                st.info("No membership type data found to chart.")
                            st.markdown("</div>", unsafe_allow_html=True)
                    else:
                        st.metric("Total Members", total_members)
                        st.info("No active memberships in the system yet.")
                else:
                    st.error(
                        f"Failed to load memberships. Status Code: {membership_res.status_code}"
                    )

                st.divider()

                st.markdown('<div class="chart-card">', unsafe_allow_html=True)
                st.markdown(
                    "<p class='category-title'>Members Added Monthly</p>",
                    unsafe_allow_html=True,
                )

                if members_data:
                    df_members = pd.DataFrame(members_data)

                    if (
                        "created_at" in df_members.columns
                        and not df_members["created_at"].isnull().all()
                    ):
                        df_members["created_at"] = pd.to_datetime(
                            df_members["created_at"], errors="coerce"
                        )
                        df_members["Month"] = df_members["created_at"].dt.strftime(
                            "%Y-%m"
                        )

                        monthly_data = df_members.groupby("Month").size().sort_index()

                        if not monthly_data.empty:
                            fig2, ax2 = plt.subplots(figsize=(10, 4), facecolor="none")

                            bars = ax2.bar(
                                monthly_data.index,
                                monthly_data.values,
                                color="#00AAA6",
                                width=0.5,
                            )

                            ax2.tick_params(axis="x", colors="#94a3b8", rotation=45)
                            ax2.tick_params(axis="y", colors="#94a3b8")
                            ax2.set_ylabel(
                                "New Members", color="#94a3b8", fontweight="bold"
                            )

                            for spine in ["top", "right"]:
                                ax2.spines[spine].set_visible(False)
                            ax2.spines["bottom"].set_color("#1e293b")
                            ax2.spines["left"].set_color("#1e293b")

                            st.pyplot(fig2)
                        else:
                            st.info(
                                "Not enough date information to plot monthly trends."
                            )
                    else:
                        st.warning(
                            "Date information is missing. Make sure you updated the Flask backend to send 'created_at'."
                        )
                else:
                    st.info("No members available to chart.")

                st.markdown("</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Error generating summary: {e}")

        with tab3:
            st.subheader("Transaction Summary")

            try:
                trans_res = requests.get(
                    f"{base_url}/transaction/show", params={"page": 1, "per_page": 1000}
                )

                if trans_res.status_code == 200:
                    res_json = trans_res.json()
                    data = res_json.get("data", {})
                    transactions = data.get("transaction", [])

                    if transactions:
                        df_t = pd.DataFrame(transactions)

                        if "status" in df_t.columns:
                            df_t["status_clean"] = (
                                df_t["status"].astype(str).str.strip().str.lower()
                            )
                        else:
                            df_t["status_clean"] = ""

                        total_trans = len(df_t)
                        issued_count = (df_t["status_clean"] == "issued").sum()
                        returned_count = (
                            df_t["status_clean"]
                            .str.contains("returned", na=False)
                            .sum()
                        )

                        if "fine_amount" in df_t.columns:
                            df_t["fine_amount"] = pd.to_numeric(
                                df_t["fine_amount"], errors="coerce"
                            ).fillna(0)
                            total_fines = df_t["fine_amount"].sum()
                        else:
                            total_fines = 0.0

                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Total Transactions", total_trans)
                        with col2:
                            st.metric("Currently Issued", int(issued_count))
                        with col3:
                            st.metric("Books Returned", int(returned_count))
                        with col4:
                            st.metric("Total Fines Collected", f"₹ {total_fines:,.2f}")

                        st.divider()

                        col1, col2 = st.columns([1, 2])

                        with col1:
                            st.markdown(
                                '<div class="chart-card">', unsafe_allow_html=True
                            )
                            st.markdown(
                                "<p class='category-title'>Transaction Status</p>",
                                unsafe_allow_html=True,
                            )

                            status_counts = (
                                df_t["status"].value_counts()
                                if "status" in df_t.columns
                                else pd.Series(dtype=int)
                            )

                            if not status_counts.empty:
                                fig, ax = plt.subplots(figsize=(5, 5), facecolor="none")

                                ax.plot(
                                    status_counts.index.str.title(),
                                    status_counts.values,
                                    color="#00AAA6",
                                    marker="o",
                                    linestyle="-",
                                    linewidth=2,
                                    markersize=8,
                                )

                                ax.tick_params(axis="x", colors="#94a3b8")
                                ax.tick_params(axis="y", colors="#94a3b8")
                                ax.set_ylabel(
                                    "Total Count",
                                    color="#94a3b8",
                                    fontweight="bold",
                                )

                                # Clean up the chart borders (spines)
                                for spine in ["top", "right"]:
                                    ax.spines[spine].set_visible(False)
                                ax.spines["bottom"].set_color("#1e293b")
                                ax.spines["left"].set_color("#1e293b")

                                ax.set_ylim(bottom=0)

                                st.pyplot(fig)
                            else:
                                st.info("No status data available to chart.")

                            st.markdown("</div>", unsafe_allow_html=True)

                        with col2:
                            st.markdown(
                                '<div class="chart-card">', unsafe_allow_html=True
                            )
                            st.markdown(
                                "<p class='category-title'>Books Issued Monthly</p>",
                                unsafe_allow_html=True,
                            )

                            if (
                                "issue_date" in df_t.columns
                                and not df_t["issue_date"].isnull().all()
                            ):
                                df_t["issue_date_dt"] = pd.to_datetime(
                                    df_t["issue_date"], errors="coerce"
                                )
                                df_t["Month"] = df_t["issue_date_dt"].dt.strftime(
                                    "%Y-%m"
                                )

                                monthly_issues = (
                                    df_t.groupby("Month").size().sort_index()
                                )

                                if not monthly_issues.empty:
                                    fig2, ax2 = plt.subplots(
                                        figsize=(8, 4), facecolor="none"
                                    )

                                    ax2.bar(
                                        monthly_issues.index,
                                        monthly_issues.values,
                                        color="#077A7D",
                                        width=0.5,
                                    )

                                    ax2.tick_params(
                                        axis="x", colors="#94a3b8", rotation=45
                                    )
                                    ax2.tick_params(axis="y", colors="#94a3b8")
                                    ax2.set_ylabel(
                                        "Total Books Issued",
                                        color="#94a3b8",
                                        fontweight="bold",
                                    )

                                    for spine in ["top", "right"]:
                                        ax2.spines[spine].set_visible(False)
                                    ax2.spines["bottom"].set_color("#1e293b")
                                    ax2.spines["left"].set_color("#1e293b")

                                    st.pyplot(fig2)
                                else:
                                    st.info(
                                        "Not enough date information to plot monthly trends."
                                    )
                            else:
                                st.info("No issue dates recorded yet.")

                            st.markdown("</div>", unsafe_allow_html=True)

                        st.divider()
                        st.markdown(
                            "<p class='category-title'>Recent Activities</p>",
                            unsafe_allow_html=True,
                        )

                        if "id" in df_t.columns:
                            df_recent = (
                                df_t.sort_values(by="id", ascending=False)
                                .head(5)
                                .copy()
                            )

                            for col in ["issue_date", "due_date", "return_date"]:
                                if col in df_recent.columns:
                                    df_recent[col] = (
                                        pd.to_datetime(df_recent[col], errors="coerce")
                                        .dt.strftime("%Y-%m-%d")
                                        .fillna("-")
                                    )

                            df_recent = df_recent.rename(
                                columns={
                                    "id": "Transaction ID",
                                    "member_id": "Member ID",
                                    "book_id": "Book ID",
                                    "issue_date": "Issue Date",
                                    "due_date": "Due Date",
                                    "return_date": "Return Date",
                                    "fine_amount": "Fine (₹)",
                                    "status": "Status",
                                }
                            )

                            drop_cols = ["Month", "status_clean", "issue_date_dt"]
                            df_recent = df_recent.drop(
                                columns=[
                                    c for c in drop_cols if c in df_recent.columns
                                ],
                                errors="ignore",
                            )

                            # Render a clean, scrollable table
                            st.dataframe(
                                df_recent, use_container_width=True, hide_index=True
                            )
                        else:
                            st.info("Could not load recent activities data.")

                    else:
                        st.info("No transactions recorded in the library yet.")

                else:
                    st.error(
                        f"Failed to load transactions. Status Code: {trans_res.status_code}"
                    )

            except Exception as e:
                st.error(f"Error generating transaction summary: {e}")
    # --- Books Page ---
    elif page == "Books":

        st.markdown(
            """
        <div class="glass-card">
            <div class="section-title">📚 Book Management</div>
            <p style="color:#737373;">
                Manage your library books, search records, update information and remove books.
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )
        tab1, tab2, tab3, tab4 = st.tabs(
            ["View Books", "search book", "Update Book", "Delete Book"]
        )

        # Tab 1: View Books
        with tab1:
            if "book_page" not in st.session_state:
                st.session_state.book_page = 1

            st.markdown(
                """
                <div class="glass-card">
                    <div class="section-title">Browse Books</div>
                """,
                unsafe_allow_html=True,
            )

            col1, col2 = st.columns([1, 3])

            with col1:
                per_page = st.selectbox(
                    "Books Per Page",
                    options=[4, 8, 12, 16],
                    index=0,
                    key="book_per_page",
                )

            st.markdown("</div>", unsafe_allow_html=True)

            params = {"page": st.session_state.book_page, "per_page": per_page}

            data = {}

            try:
                response = requests.get(f"{book_url}/show", params=params)

                st.markdown(
                    """
                    <div class="glass-card">
                        <div class="section-title">Book Records</div>
                    """,
                    unsafe_allow_html=True,
                )

                if response.status_code == 200:
                    result = response.json()

                    data = result.get("message", {})
                    books = data.get("title", [])

                    if books:
                        df = pd.DataFrame(books)

                        st.dataframe(df, use_container_width=True, hide_index=True)

                        col1, col2, col3 = st.columns(3)

                        with col1:
                            st.metric("Total Books", data.get("total records", 0))

                        with col2:
                            st.metric("Available Books", data.get("available books", 0))

                        with col3:
                            st.metric("Current Page", data.get("current page", 1))

                    else:
                        st.warning("No books found.")
                        data = {}

                else:
                    st.error(
                        f"Failed to fetch books. Status Code: {response.status_code}"
                    )
                    data = {}

            except Exception as e:
                st.error(f"Backend connection error: {e}")
                data = {}

            st.markdown("</div>", unsafe_allow_html=True)

            prev_col, center_col, next_col = st.columns([1, 2, 1])

            with prev_col:
                if st.button("⬅ Previous", key="book_prev", use_container_width=True):
                    if st.session_state.book_page > 1:
                        st.session_state.book_page -= 1
                        st.rerun()

            with center_col:
                st.markdown(
                    f"""
                    <div style="
                        text-align:center;
                        font-size:20px;
                        font-weight:600;
                        padding-top:8px;">
                        Page {st.session_state.book_page}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with next_col:
                if st.button("Next ➝", key="book_next", use_container_width=True):
                    total_pages = data.get("total pages", 1)

                    if st.session_state.book_page < total_pages:
                        st.session_state.book_page += 1
                        st.rerun()

        # Tab 2: Search Book
        with tab2:
            st.subheader("Search Book")

            search_by = st.radio("Search By", ["Book ID", "Title"], horizontal=True)

            params = {}

            if search_by == "Book ID":
                book_id = st.number_input("Book ID", min_value=1, step=1)

                params["id"] = book_id

            else:
                title = st.text_input("Book Title")

                params["title"] = title

            if st.button(
                "Search Book",
                use_container_width=True,
            ):
                try:
                    response = requests.get(f"{book_url}/search", params=params)

                    result = response.json()

                    if response.status_code == 200:

                        books = result.get("data", [])

                        if books:
                            st.success(result.get("message", "Book found"))

                            df = pd.DataFrame(books)

                            st.dataframe(df, use_container_width=True, hide_index=True)
                        else:
                            st.warning("No books found.")

                    else:
                        st.error(result.get("message", "Book not found"))

                except Exception as e:
                    st.error(f"Backend connection error: {e}")

        # Tab 3: Update Book
        with tab3:
            st.subheader("Update Book")

            if "up_book_title" not in st.session_state:
                st.session_state.up_book_title = ""

            if "up_book_author" not in st.session_state:
                st.session_state.up_book_author = ""

            if "up_book_category" not in st.session_state:
                st.session_state.up_book_category = ""

            if "up_book_quantity" not in st.session_state:
                st.session_state.up_book_quantity = 0

            if "up_book_year" not in st.session_state:
                st.session_state.up_book_year = 2000

            book_id = st.number_input(
                "Book ID", min_value=1, step=1, key="update_book_id"
            )

            if st.button(
                "Load Book",
                key="load_book_btn",
                use_container_width=True,
            ):
                try:
                    response = requests.get(
                        f"{book_url}/search", params={"id": book_id}
                    )

                    if response.status_code == 200:
                        result = response.json()

                        if result.get("data"):
                            book = result["data"][0]

                            st.session_state.up_book_title = book.get("title", "")
                            st.session_state.up_book_author = book.get("author", "")
                            st.session_state.up_book_category = book.get("category", "")
                            st.session_state.up_book_quantity = book.get("quantity", 0)
                            st.session_state.up_book_year = book.get(
                                "publishes_year", 2000
                            )

                            st.success("Book loaded successfully!")
                            st.rerun()
                        else:
                            st.error("Book not found.")

                    else:
                        st.error("Book not found.")

                except Exception as e:
                    st.error(f"Failed to fetch book: {e}")

            title = st.text_input("Title", key="up_book_title")

            author = st.text_input("Author", key="up_book_author")

            category = st.text_input("Category", key="up_book_category")

            quantity = st.number_input("Quantity", min_value=0, key="up_book_quantity")

            publishes_year = st.number_input(
                "Published Year", min_value=1000, max_value=9999, key="up_book_year"
            )

            if st.button(
                "Update Book",
                key="submit_update_book",
                use_container_width=True,
            ):
                payload = {
                    "title": title,
                    "author": author,
                    "category": category,
                    "quantity": quantity,
                    "publishes_year": publishes_year,
                }

                try:
                    response = requests.put(
                        f"{book_url}/update/{book_id}", json=payload
                    )

                    result = response.json()

                    if response.status_code == 200:
                        st.success(result.get("message", "Book updated successfully!"))

                        st.write("### Updated Book Information")
                        st.write(f"**Book ID:** {book_id}")
                        st.write(f"**Title:** {title}")
                        st.write(f"**Author:** {author}")
                        st.write(f"**Category:** {category}")
                        st.write(f"**Quantity:** {quantity}")
                        st.write(f"**Published Year:** {publishes_year}")

                    else:
                        st.error(result.get("message", "Failed to update book."))

                except Exception as e:
                    st.error(f"Update error: {e}")

        # Tab 4: Delete Book
        with tab4:
            st.subheader("Delete Book")

            delete_id = st.number_input(
                "Book ID", min_value=1, step=1, key="delete_book"
            )

            if st.button("Load Book", key="load_delete_book"):
                response = requests.get(f"{book_url}/search", params={"id": delete_id})

                data = response.json()

                if response.status_code == 200:
                    book = data.get("data")

                    if isinstance(book, list):
                        book = book[0] if book else {}

                    st.session_state["delete_book_info"] = book

                else:
                    st.error(data.get("message", "Book not found"))

            if "delete_book_info" in st.session_state:
                book = st.session_state["delete_book_info"]

                st.warning("Book Information")

                st.write(f"**ID:** {book.get('id', '')}")
                st.write(f"**Title:** {book.get('title', '')}")
                st.write(f"**Author:** {book.get('author', '')}")
                st.write(f"**Category:** {book.get('category', '')}")
                st.write(f"**Quantity:** {book.get('quantity', '')}")
                st.write(
                    f"**Available Quantity:** {book.get('Book available quantity', '')}"
                )
                st.write(f"**Published Year:** {book.get('publishes year', '')}")
                st.write(f"**Created At:** {book.get('created at', '')}")

                st.write("Remove Book Record")

            if st.button(
                "Delete Book",
                key="confirm_delete_book",
                use_container_width=True,
            ):
                try:
                    headers = {
                        "Authorization": f"Bearer {st.session_state.get('token', '')}"
                    }

                    response = requests.delete(
                        f"{book_url}/delete/{delete_id}", headers=headers
                    )

                    data = response.json()

                    if response.status_code == 200:
                        st.success(data.get("message", "Book deleted successfully."))

                        del st.session_state["delete_book_info"]

                    else:
                        st.error(
                            data.get("message", "Book not found or deletion failed.")
                        )

                except Exception as e:
                    st.error(f"Deletion error: {e}")

    elif page == "Transaction":

        tab1, tab2, tab3 = st.tabs(["issue book", "return book", "show transaction"])

        # Tab 1: issue Book
        with tab1:
            st.subheader("Issue Book")

            member_id = st.number_input(
                "Member ID", min_value=1, step=1, key="issue_member_id"
            )
            book_id = st.number_input("Book ID", min_value=1, key="Issue_book_id")

            if st.button(
                "Issue Book",
                key="issue_book_btn",
                use_container_width=True,
            ):
                payload = {"member_id": int(member_id), "book_id": int(book_id)}
                try:
                    response = requests.post(
                        f"{base_url}/transaction/issue", json=payload
                    )

                    result = response.json()

                    if result.get("status") == "success":
                        st.success(result.get("message"))

                        data = result.get("data", {})

                        df = pd.DataFrame(
                            [
                                {
                                    "Transaction ID": data.get("transaction id"),
                                    "Member ID": data.get("member id"),
                                    "Book ID": data.get("book id"),
                                    "Issue Date": data.get("issue date"),
                                    "Due Date": data.get("due date"),
                                    "Status": data.get("status"),
                                }
                            ]
                        )

                        st.dataframe(df, use_container_width=True, hide_index=True)
                    else:
                        st.error(result.get("message"))
                except Exception as e:
                    st.error(f"Error: {e}")

        # Tab 2: Return Book
        with tab2:
            st.markdown(
                """
                <div class = 'glass-card'>
                    <div class='section-title'>Return Book</div>
                """,
                unsafe_allow_html=True,
            )

            transaction_id = st.number_input(
                "Transaction ID",
                min_value=1,
                step=1,
                key="return_transaction_id",
            )

            if st.button(
                "Return Book",
                key="return_book_btn",
                use_container_width=True,
            ):
                payload = {"transaction_id": int(transaction_id)}

                try:
                    response = requests.post(
                        f"{base_url}/transaction/return", json=payload
                    )

                    result = response.json()

                    if result.get("status") == "success":
                        st.success(result.get("message"))

                        data = result.get("data", {})

                        df = pd.DataFrame(
                            [
                                {
                                    "Transaction ID": data.get("transaction id"),
                                    "Book ID": data.get("book id"),
                                    "Member ID": data.get("member id"),
                                    "Return Date": data.get("return date"),
                                    "Fine Amount": data.get("fine amount"),
                                    "Status": data.get("status"),
                                }
                            ]
                        )

                        st.dataframe(df, use_container_width=True, hide_index=True)
                    else:
                        st.error(result.get("message"))
                except Exception as e:
                    st.error(f"Error: {e}")

        # Tab 3: Show Transaction
        with tab3:
            st.subheader("Show Transaction")

            if "transaction_page" not in st.session_state:
                st.session_state.transaction_page = 1

            per_page = 4

            try:
                response = requests.get(
                    f"{base_url}/transaction/show",
                    params={
                        "page": st.session_state.transaction_page,
                        "per_page": per_page,
                    },
                )

                result = response.json() or {}

                if result.get("status") == "success":

                    data = result.get("data") or {}

                    transactions = data.get("transaction") or []

                    if transactions:

                        df = pd.DataFrame(transactions)

                        df = df.rename(
                            columns={
                                "id": "ID",
                                "member_id": "Member ID",
                                "book_id": "Book ID",
                                "issue_date": "Issue Date",
                                "due_date": "Due Date",
                                "return_date": "Return Date",
                                "fine_date": "Fine Amount",
                                "fine_amount": "Fine Amount",
                                "status": "Status",
                            }
                        )

                        st.dataframe(
                            df,
                            use_container_width=True,
                            hide_index=True,
                        )

                        col1, col2, col3 = st.columns([1, 2, 1])

                        with col1:
                            if st.button("⬅ Previous", key="prev_transaction"):
                                if st.session_state.transaction_page > 1:
                                    st.session_state.transaction_page -= 1
                                    st.rerun()

                        with col2:
                            st.markdown(
                                f"""
                                <div class="page-indicator">
                                Page {data.get('current_page')} of {data.get('total_pages')}
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                        with col3:
                            if st.button("Next ➡", key="next_transaction"):
                                if st.session_state.transaction_page < data.get(
                                    "total_pages", 1
                                ):
                                    st.session_state.transaction_page += 1
                                    st.rerun()

                        st.caption(f"Total Records: {data.get('total_records', 0)}")

                    else:
                        st.info("No transactions found.")

                else:
                    st.error(result.get("message"))

            except Exception as e:
                st.error(f"Error: {e}")
    # --- Members Page ---
    elif page == "Member":
        st.title("Member")

        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            [
                "View Members",
                "Add Member",
                "Search Member",
                "Update Member",
                "Delete Member",
            ]
        )

        # Tab 1: View Members
        with tab1:
            if "member_page" not in st.session_state:
                st.session_state.member_page = 1

            st.markdown(
                """
                <div class="glass-card">
                    <div class="section-title">Browse Members</div>
                """,
                unsafe_allow_html=True,
            )

            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                per_page = st.selectbox(
                    "Members Per Page", options=[4, 8, 12, 16], index=0
                )

            st.markdown("</div>", unsafe_allow_html=True)

            params = {"page": st.session_state.member_page, "per_page": per_page}

            try:
                response = requests.get(f"{member_url}/show", params=params)
                st.markdown(
                    """
                    <div class="glass-card">
                        <div class="section-title">Member Records</div>
                    """,
                    unsafe_allow_html=True,
                )

                if response.status_code == 200:
                    raw_data = response.json()
                    if "Members" in raw_data:
                        members = raw_data["Members"]
                        if members:
                            df = pd.DataFrame(members)
                            st.dataframe(df, use_container_width=True, hide_index=True)

                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Total Members", raw_data.get("total no", 0))
                            with col2:
                                st.metric("Total Pages", raw_data.get("total page", 0))
                            with col3:
                                st.metric(
                                    "Current Page", raw_data.get("current page", 0)
                                )
                        else:
                            st.warning("No members found.")
                            raw_data = {}
                    else:
                        st.error("Members data not found in API response.")
                        raw_data = {}
                else:
                    st.error(
                        f"Failed to fetch members. Status Code: {response.status_code}"
                    )
                    raw_data = {}
            except Exception as e:
                st.error(f"Backend connection error: {e}")
                raw_data = {}

            st.markdown("</div>", unsafe_allow_html=True)

            prev_col, center_col, next_col = st.columns([1, 2, 1])
            with prev_col:
                if st.button("⬅ Previous", use_container_width=True):
                    if st.session_state.member_page > 1:
                        st.session_state.member_page -= 1
                        st.rerun()

            with center_col:
                st.markdown(
                    f'<div class="page-indicator">Page {st.session_state.member_page}</div>',
                    unsafe_allow_html=True,
                )

            with next_col:
                if st.button("Next ➝", use_container_width=True):
                    total_pages = raw_data.get("total page", 1)
                    if st.session_state.member_page < total_pages:
                        st.session_state.member_page += 1
                        st.rerun()

        # Tab 2: Add Member
        with tab2:
            st.markdown(
                """
                <div class="glass-card">
                    <div class="section-title">Add New Member</div>
                """,
                unsafe_allow_html=True,
            )

            with st.form("add_member_form"):
                name = st.text_input("Member Name")
                phone_no = st.text_input("Phone Number")
                address = st.text_area("Address")

                submit_member = st.form_submit_button("Create Member")

            if submit_member:
                payload = {
                    "name": name,
                    "phone_no": phone_no,
                    "address": address,
                }

                try:
                    response = requests.post(f"{member_url}/create", json=payload)

                    result = response.json()

                    if response.status_code in [200, 201]:
                        st.success("Member created successfully")

                        if "message" in result:
                            st.write(result["message"])

                    else:
                        st.error("Failed to create member")
                        st.write(result)

                except Exception as e:
                    st.error(f"Backend connection error: {e}")

            st.markdown("</div>", unsafe_allow_html=True)

        # Tab 3: Search Member
        with tab3:
            st.subheader("Search Member")
            search_by = st.radio(
                "Search by", ["Member ID", "Member Name"], horizontal=True
            )

            if search_by == "Member ID":
                member_id = st.number_input(
                    "Member ID", min_value=1, key="search_member_id"
                )
                if st.button(
                    "Search",
                    key="search_id_btn",
                    use_container_width=True,
                ):
                    try:
                        response = requests.get(
                            f"{member_url}/search", params={"id": member_id}
                        )
                        data = response.json()
                        if response.status_code == 200:
                            st.success("Member Found")
                            if "data" in data and data["data"]:
                                df = pd.DataFrame(data["data"])
                                st.dataframe(df, use_container_width=True)
                            else:
                                st.write(data)
                        else:
                            st.error(data.get("message", "Member not found"))
                    except Exception as e:
                        st.error(f"Search failed: {e}")
            else:
                member_name = st.text_input("Member Name", key="search_member_name")
                if st.button(
                    "Search",
                    key="search_name_btn",
                    use_container_width=True,
                ):
                    try:
                        response = requests.get(
                            f"{member_url}/search", params={"name": member_name}
                        )
                        data = response.json()
                        if response.status_code == 200:
                            st.success("Member Found")
                            if "data" in data and data["data"]:
                                df = pd.DataFrame(data["data"])
                                st.dataframe(df, use_container_width=True)
                            else:
                                st.write(data)
                        else:
                            st.error(data.get("message", "Member not found"))
                    except Exception as e:
                        st.error(f"Search failed: {e}")

        # Tab 4: Update Member
        with tab4:
            st.subheader("Update Member")

            if "up_name_input" not in st.session_state:
                st.session_state.up_name_input = ""
            if "up_phone_input" not in st.session_state:
                st.session_state.up_phone_input = ""
            if "up_address_input" not in st.session_state:
                st.session_state.up_address_input = ""

            update_id = st.number_input(
                "Member ID", min_value=1, key="update_member_id"
            )

            if st.button(
                "Load Member",
                key="load_member_btn",
                use_container_width=True,
            ):
                try:
                    response = requests.get(
                        f"{member_url}/search", params={"id": update_id}
                    )
                    if response.status_code == 200:
                        result = response.json()
                        if result.get("data"):
                            member = result["data"][0]

                            st.session_state.up_name_input = member.get("name", "")
                            st.session_state.up_phone_input = member.get(
                                "phone", ""
                            ) or member.get("phone_no", "")
                            st.session_state.up_address_input = member.get(
                                "address", ""
                            )

                            st.success(
                                "Member loaded successfully! Fields updated below."
                            )
                            st.rerun()
                        else:
                            st.error("Member details missing from backend data array.")
                    else:
                        st.error("Member not found.")
                except Exception as e:
                    st.error(f"Failed to fetch resource: {e}")

            up_name = st.text_input("Name", key="up_name_input")
            up_phone = st.text_input("Phone Number", key="up_phone_input")
            up_address = st.text_input("Address", key="up_address_input")

            if st.button(
                "Update Member",
                key="submit_update_btn",
                use_container_width=True,
            ):
                if not up_name:
                    st.warning("Please load a member or enter a name first.")
                else:
                    payload = {
                        "name": up_name,
                        "phone no": up_phone,
                        "address": up_address,
                    }
                    try:
                        response = requests.put(
                            f"{member_url}/update/{update_id}", json=payload
                        )
                        data = response.json()
                        if response.status_code == 200:
                            st.success(data.get("message", "Updated successfully!"))
                            st.write("### Updated Member Information")
                            st.write(f"**Member ID:** {update_id}")
                            st.write(f"**Name:** {up_name}")
                            st.write(f"**Phone Number:** {up_phone}")
                            st.write(f"**Address:** {up_address}")
                        else:
                            st.error(
                                data.get("message", "Failed to update member profiles.")
                            )
                    except Exception as e:
                        st.error(f"Update network pipeline error: {e}")

        # Tab 5: Delete Member
        with tab5:
            st.subheader("Delete Member")
            delete_id = st.number_input(
                "Member ID", min_value=1, step=1, key="delete_member"
            )

            if st.button("Load Member", key="load_delete_member"):
                response = requests.get(
                    f"{member_url}/search", params={"id": delete_id}
                )
                data = response.json()
                if response.status_code == 200:
                    member = data.get("data")

                    if isinstance(member, list):
                        member = member[0] if member else {}

                    st.session_state["delete_member_info"] = member

                else:
                    st.error(data.get("message", "member not found"))

            if "delete_member_info" in st.session_state:
                member = st.session_state["delete_member_info"]

                st.warning("Member Information")

                st.write(f"**ID:** {member.get('id', '')}")
                st.write(f"**Name:** {member.get('name', '')}")
                st.write(f"**Phone Number:** {member.get('phone_no', '')}")
                st.write(f"**Address:** {member.get('address', '')}")
                st.write("Remove Member Profile")

            if st.button(
                "Delete Member",
                key="confirm_delete_btn",
                use_container_width=True,
            ):
                try:
                    headers = {
                        "Authorization": f"Bearer {st.session_state.get('token','')}"
                    }
                    response = requests.delete(
                        f"{member_url}/delete/{delete_id}", headers=headers
                    )
                    data = response.json()

                    if response.status_code == 200:
                        st.success(data.get("message", "Member deleted successfully."))
                        del st.session_state["delete_member_info"]
                    else:
                        st.error(
                            data.get(
                                "message", "Member not found or deletion restricted."
                            )
                        )
                except Exception as e:
                    st.error(f"Deletion payload error: {e}")

    elif page == "Management":
        st.header("Membership Management")
        tab1, tab2, tab3 = st.tabs(
            ["Add Membership", "search membership", "Membership List"]
        )

        with tab1:
            st.subheader("Add Membership")

            member_id = st.number_input(
                "Member ID", min_value=1, step=1, key="membership_member_id"
            )

            membership_type = st.selectbox(
                "Membership Type",
                ["1 week", "1 month", "6 month", "1 year"],
                key="membership_type",
            )

            if st.button(
                "Add Membership",
                key="add_membership_btn",
                use_container_width=True,
            ):

                payload = {
                    "member_id": int(member_id),
                    "membership_type": membership_type,
                }

                try:
                    response = requests.post(
                        f"{base_url}/member/membership", json=payload
                    )

                    result = response.json()

                    if "error" in result:
                        st.error(result["error"])

                    elif result.get("message") == "member not found":
                        st.error("Member not found")

                    elif result.get("message") == "invalid membership type":
                        st.error("Invalid membership type")

                    else:
                        st.success(result.get("message"))

                        df = pd.DataFrame(
                            [
                                {
                                    "Member Name": result.get("member_name"),
                                    "Membership Type": membership_type,
                                    "Expiry Date": result.get("expiry_date"),
                                }
                            ]
                        )

                        st.dataframe(df, use_container_width=True, hide_index=True)

                except Exception as e:
                    st.error(f"Error: {e}")

        with tab2:
            st.subheader("Search Membership")

            membership_type = st.selectbox(
                "Membership Type",
                ["1 week", "1 month", "6 month", "1 year"],
                key="search_membership_type",
            )

            if st.button(
                "Search Membership",
                key="search_membership_btn",
                use_container_width=True,
            ):
                try:
                    response = requests.get(
                        f"{member_url}/membership/search",
                        params={
                            "membership_type": membership_type,
                            "page": 1,
                            "per_page": 4,
                        },
                    )

                    result = response.json()

                    if (
                        response.status_code == 200
                        and result.get("status") == "success"
                    ):

                        st.success("Membership Found")

                        data = result.get("data", {})
                        memberships = data.get("membership", [])

                        if memberships:

                            df = pd.DataFrame(memberships)

                            df = df.rename(
                                columns={
                                    "member id": "Member ID",
                                    "member name": "Member Name",
                                    "phone no": "Phone No",
                                    "address": "Address",
                                    "membership type": "Membership Type",
                                    "start date": "Start Date",
                                    "end date": "End Date",
                                }
                            )

                            st.dataframe(
                                df,
                                use_container_width=True,
                                hide_index=True,
                            )

                            st.caption(
                                f"Page {data.get('current page', 1)} "
                                f"of {data.get('total page', 1)} | "
                                f"Total Records: {data.get('total no', 0)}"
                            )

                        else:
                            st.warning("No memberships found.")

                    else:
                        st.error(result.get("message", "Membership not found"))

                except Exception as e:
                    st.error(f"Search failed: {e}")

        with tab3:
            if "membership_page" not in st.session_state:
                st.session_state.membership_page = 1

            st.markdown(
                """
                <div class="glass-card">
                    <div class="section-title">Browse Memberships</div>
                """,
                unsafe_allow_html=True,
            )

            col1, col2, col3 = st.columns([1, 1, 2])

            with col1:
                per_page = st.selectbox(
                    "Memberships Per Page",
                    options=[4, 8, 12, 16],
                    index=0,
                    key="membership_per_page",
                )

            st.markdown("</div>", unsafe_allow_html=True)

            params = {
                "page": st.session_state.membership_page,
                "per_page": per_page,
            }

            try:
                response = requests.get(
                    f"{member_url}/membership/show",
                    params=params,
                )

                st.markdown(
                    """
                    <div class="glass-card">
                        <div class="section-title">Membership Records</div>
                    """,
                    unsafe_allow_html=True,
                )

                if response.status_code == 200:

                    result = response.json()

                    if result.get("status") == "success":

                        data = result.get("data", {})

                        memberships = data.get("memberships", [])

                        if memberships:

                            df = pd.DataFrame(memberships)

                            df = df.rename(
                                columns={
                                    "member_id": "Member ID",
                                    "member_name": "Member Name",
                                    "phone_no": "Phone No",
                                    "address": "Address",
                                    "membership_type": "Membership Type",
                                    "start_date": "Start Date",
                                    "end_date": "End Date",
                                }
                            )

                            st.dataframe(
                                df,
                                use_container_width=True,
                                hide_index=True,
                            )

                            col1, col2, col3 = st.columns(3)

                            with col1:
                                st.metric(
                                    "Total Memberships",
                                    data.get("total_records", 0),
                                )

                            with col2:
                                st.metric(
                                    "Total Pages",
                                    data.get("total_pages", 0),
                                )

                            with col3:
                                st.metric(
                                    "Current Page",
                                    data.get("current_page", 0),
                                )

                        else:
                            st.warning("No memberships found.")
                            data = {}

                    else:
                        st.error(result.get("message", "Memberships not found."))
                        data = {}

                else:
                    st.error(
                        f"Failed to fetch memberships. Status Code: {response.status_code}"
                    )
                    data = {}

            except Exception as e:
                st.error(f"Backend connection error: {e}")
                data = {}

            st.markdown("</div>", unsafe_allow_html=True)

            prev_col, center_col, next_col = st.columns([1, 2, 1])

            with prev_col:
                if st.button(
                    "⬅ Previous",
                    key="membership_prev",
                    use_container_width=True,
                ):
                    if st.session_state.membership_page > 1:
                        st.session_state.membership_page -= 1
                        st.rerun()

            with center_col:
                st.markdown(
                    f"""
                    <div class="page-indicator">
                        Page {st.session_state.membership_page}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with next_col:
                if st.button(
                    "Next ➝",
                    key="membership_next",
                    use_container_width=True,
                ):
                    total_pages = data.get("total_pages", 1)

                    if st.session_state.membership_page < total_pages:
                        st.session_state.membership_page += 1
                        st.rerun()

    # tab 2: add book
    elif page == "Add Book":
        st.markdown(
            """
                <div class="glass-card">
                    <div class="section-title">Fill The Information</div>
                """,
            unsafe_allow_html=True,
        )

        with st.form("add_book_form"):
            title = st.text_input("Book Title")
            author = st.text_input("Author")
            category = st.text_input("Category")
            quantity = st.number_input("Quantity", min_value=1, step=1)
            publishes_year = st.number_input(
                "Published Year", min_value=1000, max_value=9999, step=1
            )

            created_at = st.date_input("Created Date")

            submit_book = st.form_submit_button("Add Book")

        if submit_book:
            payload = {
                "title": title,
                "author": author,
                "category": category,
                "quantity": quantity,
                "publishes_year": publishes_year,
                "created_at": created_at.strftime("%Y-%m-%d"),
            }

            try:
                response = requests.post(f"{book_url}/create", json=payload)

                result = response.json()

                if response.status_code in [200, 201]:
                    st.success("Book added successfully")

                    if "message" in result:
                        st.write(result["message"])

                else:
                    st.error("Failed to add book")
                    st.write(result)

            except Exception as e:
                st.error(f"Backend connection error: {e}")

        st.markdown("</div>", unsafe_allow_html=True)

    elif page == "Fines":
        if "fine_page" not in st.session_state:
            st.session_state.fine_page = 1

        st.markdown(
            """
                <div class="glass-card">
                    <div class="section-title">Fine Records</div>
                """,
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns([1, 1, 2])

        with col1:
            per_page = st.selectbox(
                "Records Per Page",
                options=[4, 8, 12, 16],
                index=0,
                key="fine_per_page",
            )

        st.markdown("</div>", unsafe_allow_html=True)

        params = {
            "page": st.session_state.fine_page,
            "per_page": per_page,
        }

        try:
            response = requests.get(
                f"{base_url}/transaction/fines",
                params=params,
            )

            st.markdown(
                """
                    <div class="glass-card">
                        <div class="section-title">Fine Details</div>
                    """,
                unsafe_allow_html=True,
            )

            if response.status_code == 200:

                result = response.json()

                if result.get("status") == "success":

                    data = result.get("data", {})

                    fines = data.get("fines", [])

                    if fines:

                        df = pd.DataFrame(fines)

                        df = df.rename(
                            columns={
                                "transaction_id": "Transaction ID",
                                "member_id": "Member ID",
                                "member_name": "Member Name",
                                "phone_no": "Phone No",
                                "book_id": "Book ID",
                                "return_date": "Return Date",
                                "fine_amount": "Fine Amount (₹)",
                            }
                        )

                        st.dataframe(
                            df,
                            use_container_width=True,
                            hide_index=True,
                        )

                        col1, col2, col3, col4 = st.columns(4)

                        with col1:
                            st.metric(
                                "Total Records",
                                data.get("total_records", 0),
                            )

                        with col2:
                            st.metric(
                                "Total Pages",
                                data.get("total_pages", 0),
                            )

                        with col3:
                            st.metric(
                                "Current Page",
                                data.get("current_page", 0),
                            )

                        with col4:
                            st.metric(
                                "Total Fine",
                                f"₹{data.get('total_fine_collected', 0)}",
                            )

                    else:
                        st.warning("No fine records found.")
                        data = {}

                else:
                    st.error(result.get("message", "Fine records not found."))
                    data = {}

            else:
                st.error(
                    f"Failed to fetch fine records. Status Code: {response.status_code}"
                )
                data = {}

        except Exception as e:
            st.error(f"Backend connection error: {e}")
            data = {}

        st.markdown("</div>", unsafe_allow_html=True)

        prev_col, center_col, next_col = st.columns([1, 2, 1])

        with prev_col:
            if st.button(
                "⬅ Previous",
                key="fine_prev",
                use_container_width=True,
            ):
                if st.session_state.fine_page > 1:
                    st.session_state.fine_page -= 1
                    st.rerun()

        with center_col:
            st.markdown(
                f"""
                    <div class="page-indicator">
                        Page {st.session_state.fine_page}
                    </div>
                    """,
                unsafe_allow_html=True,
            )

        with next_col:
            if st.button(
                "Next ➝",
                key="fine_next",
                use_container_width=True,
            ):
                total_pages = data.get("total_pages", 1)

                if st.session_state.fine_page < total_pages:
                    st.session_state.fine_page += 1
                    st.rerun()

    elif page == "Setting":
        tab1, tab2 = st.tabs(["change password", "delete Admin & superadmin"])
        with tab1:
            st.markdown(
                """
                <div class="glass-card">
                    <div class="section-title">Change Password</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            username = st.text_input(
                "Username",
                key="change_username",
            )

            old_password = st.text_input(
                "Old Password",
                type="password",
                key="old_password",
            )

            new_password = st.text_input(
                "New Password",
                type="password",
                key="new_password",
            )

            confirm_password = st.text_input(
                "Confirm New Password",
                type="password",
                key="confirm_password",
            )

            if st.button(
                "Change Password",
                key="change_password_btn",
                use_container_width=True,
            ):

                if not username.strip():
                    st.warning("Please enter username.")

                elif not old_password:
                    st.warning("Please enter old password.")

                elif not new_password:
                    st.warning("Please enter new password.")

                elif new_password != confirm_password:
                    st.error("New password and confirm password do not match.")

                else:

                    payload = {
                        "username": username.strip(),
                        "old_password": old_password,
                        "new_password": new_password,
                    }

                    try:
                        response = requests.put(
                            f"{base_url}/auth/change_password",
                            json=payload,
                        )

                        result = response.json()

                        if response.status_code == 200:

                            st.success(
                                result.get(
                                    "message",
                                    "Password changed successfully",
                                )
                            )

                        else:
                            st.error(
                                result.get(
                                    "message",
                                    "Failed to change password",
                                )
                            )

                    except Exception as e:
                        st.error(f"Error: {e}")

        with tab2:
            st.markdown(
                """
                <div class="glass-card">
                    <div class="section-title">Delete User</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            user_id = st.number_input(
                "User ID",
                min_value=1,
                step=1,
                key="delete_user_id",
            )

            if st.button(
                "Delete User",
                key="delete_user_btn",
                use_container_width=True,
            ):

                try:
                    response = requests.delete(f"{base_url}/auth/delete/{int(user_id)}")

                    result = response.json()

                    if response.status_code == 200:
                        st.success(result.get("message", "User deleted successfully"))

                    else:

                        st.error(result.get("message", "Failed to delete user"))

                except Exception as e:
                    st.error(f"Error: {e}")

    elif page == "Profile":

        st.markdown(
            """
            <div class="glass-card">
                <div class="section-title">👤 User Profile</div>
                <p style="color:#94a3b8; margin:0;">
                    View your account details and role information.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        try:
            response = requests.get(
                f"{base_url}/auth/profile", cookies=st.session_state.get("cookies", {})
            )

            if response.status_code == 200:

                user = response.json()["data"]
                st.markdown(
                    f"""
                    <div class="glass-card">
                        <div class="gradient-subheader" style="margin-top: 0; font-size: 24px;">{user['name']}</div>
                        <hr style="margin: 16px 0 !important;">
                        <div style="margin-top: 16px; display: flex; flex-direction: column; gap: 12px;">
                            <p style="margin: 0; font-size: 15px;">
                                <strong style="color: #cbd5e1;">ID:</strong> 
                                <span style="color: #94a3b8;">{user['id']}</span>
                            </p>
                            <p style="margin: 0; font-size: 15px;">
                                <strong style="color: #cbd5e1;">Username:</strong> 
                                <span style="color: #94a3b8;">{user['username']}</span>
                            </p>
                            <p style="margin: 0; font-size: 15px;">
                                <strong style="color: #cbd5e1;">Role:</strong> 
                                <span style="color: #a5b4fc; text-transform: capitalize; font-weight: 500;">{user['role']}</span>
                            </p>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.markdown("<br>", unsafe_allow_html=True)
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button(
                        "Logout",
                        key="profile_logout_btn",
                        use_container_width=True,
                    ):
                        st.session_state.authenticated = False
                        if "user_data" in st.session_state:
                            st.session_state.user_data = None
                        if "page" in st.session_state:
                            st.session_state.page = "Overview"
                        st.rerun()

            else:
                st.error("Unable to fetch profile")

        except Exception as e:
            st.error(str(e))
