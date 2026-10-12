import streamlit as st
import requests
import pandas as pd
from datetime import date, timedelta
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

GRAPH_COLORS = [
    "#6366f1",  # Electric Indigo
    "#06b6d4",  # Cyan
    "#a855f7",  # Violet
    "#10b981",  # Emerald
    "#f43f5e",  # Rose
    "#f59e0b",  # Amber
    "#38bdf8",  # Sky Blue
    "#ec4899",  # Pink
    "#8b5cf6",  # Purple
    "#14b8a6",  # Teal
]


def get_graph_colors(n):
    """Safely return n colors, cycling through the palette if n > len(GRAPH_COLORS)."""
    if n <= 0:
        return []
    return (GRAPH_COLORS * (n // len(GRAPH_COLORS) + 1))[:n]


BASE_URL = "http://127.0.0.1:5501"
BOOK_URL = f"{BASE_URL}/book"
MEMBER_URL = f"{BASE_URL}/member"
TRANS_URL = f"{BASE_URL}/transaction"
AUTH_URL = f"{BASE_URL}/auth"


def api_call(method, url, **kwargs):
    """Centralized, resilient API request handler."""
    cookies = st.session_state.get("cookies", {})
    kwargs.setdefault("cookies", cookies)
    kwargs.setdefault("timeout", 8)
    try:
        res = requests.request(method, url, **kwargs)
        try:
            payload = res.json()
        except Exception:
            payload = {"status": "error", "message": res.text or f"HTTP {res.status_code}"}
        return res.status_code, payload
    except requests.exceptions.ConnectionError:
        return 0, {
            "status": "error",
            "message": "Cannot reach backend server. Please verify Flask backend (`python app.py`) is running.",
        }
    except Exception as e:
        return 500, {"status": "error", "message": str(e)}


def show_dashboard(logout_callback=None):
    """Aesthetic, modern, and reliable dashboard."""

    user_info = st.session_state.get("user_data") or {}
    user_name = user_info.get("name") or user_info.get("username") or "Admin"
    user_role = (user_info.get("role") or "admin").upper()

    # ----------------- SIDEBAR ----------------- #
    with st.sidebar:
        st.markdown(
            f"""
            <div class="brand-header">
                <div class="brand-icon">📚</div>
                <div class="brand-text">
                    <h3>Library management</h3>
                    <p>Library Intelligence</p>
                </div>
            </div>

            <div class="user-card">
                <div class="user-card-left">
                    <div class="user-avatar">{user_name[0].upper()}</div>
                    <div>
                        <div class="user-info-name">{user_name}</div>
                        <div class="user-info-role">{user_role}</div>
                    </div>
                </div>
                <div class="status-dot" title="Active"></div>
            </div>

            <div class="nav-header">MAIN MENU</div>
            """,
            unsafe_allow_html=True,
        )

        nav_map = {
            "📊 Dashboard": "Dashboard",
            "📚 Book Catalog": "Books",
            "🔄 Circulation & Loans": "Circulation",
            "👥 Members Directory": "Members",
            "🎫 Memberships": "Memberships",
            "➕ Add New Book": "Add Book",
            "💰 Overdue Fines": "Fines",
            "⚙️ Settings": "Settings",
            "👤 Profile": "Profile",
        }

        selected_nav = st.radio(
            "Navigation Menu",
            list(nav_map.keys()),
            label_visibility="collapsed",
            key="main_navigation",
        )

        st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

        if st.button("🚪 Sign Out", key="sidebar_logout_btn", use_container_width=True):
            if logout_callback:
                logout_callback()
            else:
                st.session_state.authenticated = False
                st.session_state.user_data = None
                st.session_state.cookies = {}
                st.rerun()

    page = nav_map.get(selected_nav, "Dashboard")

    # ========================================================
    # 1. DASHBOARD OVERVIEW
    # ========================================================
    if page == "Dashboard":
        st.markdown(
            """
            <div style="margin-bottom: 20px;">
                <h1 style="margin: 0; font-size: 26px;">📊 Dashboard Overview</h1>
                <p style="color: #94a3b8; font-size: 13.5px; margin-top: 4px;">Real-time circulation metrics, member analytics, and catalog distributions</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # --- 3 TABS AS IN ORIGINAL APPLICATION ---
        tab1, tab2, tab3 = st.tabs(
            ["📚 Books Summary", "👥 Member & Membership Summary", "🔄 Transaction Summary"]
        )

        # ========================================================
        # TAB 1: BOOKS SUMMARY (Original Category Pie Chart)
        # ========================================================
        with tab1:
            try:
                stat, response_json = api_call("GET", f"{BOOK_URL}/show", params={"page": 1, "per_page": 1000})
                if stat == 200 and response_json.get("status") == "success":
                    data = response_json.get("data", {})
                    books = data.get("title", [])

                    if books:
                        df = pd.DataFrame(books)

                        # Clean numeric fields to prevent string-sum or NaN errors
                        if "quantity" in df.columns:
                            df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(1)
                        if "available_quantity" in df.columns:
                            df["available_quantity"] = pd.to_numeric(df["available_quantity"], errors="coerce").fillna(0)

                        # Normalize categories (strip whitespace and title case)
                        if "category" in df.columns:
                            df["category"] = df["category"].fillna("Unknown").astype(str).str.strip().str.title()
                            category_counts = df.groupby("category")["quantity"].sum().sort_index()
                        else:
                            category_counts = pd.Series(dtype=int)

                        total_books_count = int(data.get("total records", len(df)))

                        if "status" in df.columns:
                            available_books_count = int(len(df[df["status"] == "Available"]))
                        elif "available_quantity" in df.columns:
                            available_books_count = int(df["available_quantity"].sum())
                        else:
                            available_books_count = int(data.get("available books", total_books_count))

                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total Books", total_books_count)
                        with col2:
                            st.metric("Available Books", available_books_count)
                        with col3:
                            st.metric("Total Categories", len(category_counts))

                        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

                        with st.container(border=True):
                            st.markdown(
                                """
                                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
                                    <span style="font-size: 13px; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.8px;">Book Distribution by Category</span>
                                    <span class="badge-pill badge-issued">Catalog Composition</span>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                            if not category_counts.empty:
                                left_spacer, center_col, right_spacer = st.columns([1, 2.2, 1])
                                with center_col:
                                    fig, ax = plt.subplots(figsize=(6, 4), facecolor="none")
                                    colors = get_graph_colors(len(category_counts))
                                    wedges, texts, autotexts = ax.pie(
                                        category_counts,
                                        labels=category_counts.index,
                                        autopct="%1.1f%%",
                                        startangle=140,
                                        colors=colors,
                                        radius=0.95,
                                        labeldistance=1.15,
                                        pctdistance=0.65,
                                        wedgeprops={"edgecolor": "#0b0f19", "linewidth": 2},
                                    )
                                    for t in texts:
                                        t.set_color("#cbd5e1")
                                        t.set_fontsize(9)
                                        t.set_fontweight("600")
                                    for at in autotexts:
                                        at.set_color("#ffffff")
                                        at.set_fontsize(9)
                                        at.set_fontweight("bold")

                                    ax.axis("equal")
                                    plt.tight_layout()
                                    st.pyplot(fig, use_container_width=True)
                                    plt.close(fig)
                            else:
                                st.info("No category data found in the records.")
                    else:
                        st.warning("No books available in the library yet.")
                else:
                    st.error(f"Failed to load books: {response_json.get('message', 'Backend response error')}")
            except Exception as e:
                st.error(f"Error generating books summary: {e}")

        # ========================================================
        # TAB 2: MEMBER & MEMBERSHIP SUMMARY (Original 2 Graphs)
        # ========================================================
        with tab2:
            try:
                s_mem, member_res = api_call("GET", f"{MEMBER_URL}/show", params={"page": 1, "per_page": 1000})
                s_mship, membership_res = api_call(
                    "GET", f"{MEMBER_URL}/membership/show", params={"page": 1, "per_page": 1000}
                )

                if s_mem != 200 or member_res.get("status") != "success":
                    st.warning(f"Could not load members: {member_res.get('message', 'Backend error')}")

                mem_data = member_res.get("data", {}) if member_res.get("status") == "success" else {}
                members_data = mem_data.get("Members", [])
                total_members = int(mem_data.get("total no", len(members_data)))

                mship_data = membership_res.get("data", {}) if membership_res.get("status") == "success" else {}
                memberships = mship_data.get("memberships", [])

                if memberships:
                    df_m = pd.DataFrame(memberships)
                    if "status" in df_m.columns:
                        status_series = df_m["status"].astype(str).str.strip().str.lower()
                        active_count = int((status_series == "active").sum())
                        expired_count = int((status_series == "expired").sum())
                    else:
                        active_count = 0
                        expired_count = 0

                    # Normalize membership type to avoid fragmented duplicate slices
                    if "membership_type" in df_m.columns:
                        df_m["membership_type_norm"] = (
                            df_m["membership_type"].astype(str).str.strip().str.title()
                        )
                        type_counts = df_m["membership_type_norm"].value_counts().sort_index()
                    else:
                        type_counts = pd.Series(dtype=int)

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Members", total_members)
                    with col2:
                        st.metric("Active Memberships", active_count)
                    with col3:
                        st.metric("Expired Memberships", expired_count)

                    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

                    with st.container(border=True):
                        st.markdown(
                            """
                            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
                                <span style="font-size: 13px; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.8px;">Membership Plans Distribution</span>
                                <span class="badge-pill badge-active">Plan Ratio</span>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                        if not type_counts.empty:
                            c_left, c_chart, c_right = st.columns([1, 2, 1])
                            with c_chart:
                                fig, ax = plt.subplots(figsize=(4, 3), facecolor="none")
                                colors = get_graph_colors(len(type_counts))
                                wedges, texts, autotexts = ax.pie(
                                    type_counts,
                                    labels=type_counts.index,
                                    autopct="%1.1f%%",
                                    startangle=140,
                                    colors=colors,
                                    radius=0.85,
                                    labeldistance=1.2,
                                    wedgeprops={"edgecolor": "#0b0f19", "linewidth": 1.5},
                                )
                                for t in texts:
                                    t.set_color("#cbd5e1")
                                    t.set_fontsize(9)
                                    t.set_fontweight("600")
                                for at in autotexts:
                                    at.set_color("#ffffff")
                                    at.set_fontsize(9)
                                    at.set_fontweight("bold")

                                ax.axis("equal")
                                plt.tight_layout()
                                st.pyplot(fig, use_container_width=True)
                                plt.close(fig)
                        else:
                            st.info("No membership type data found to chart.")
                else:
                    st.metric("Total Members", total_members)
                    if s_mship == 200:
                        st.info("No active memberships in the system yet.")
                    else:
                        st.error(f"Failed to load memberships: {membership_res.get('message', 'Server error')}")

                st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

                # Graph 2: Members Added Monthly
                with st.container(border=True):
                    st.markdown(
                        """
                        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
                            <span style="font-size: 13px; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.8px;">Members Added Monthly</span>
                            <span class="badge-pill badge-issued">Growth Velocity</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    if members_data:
                        df_members = pd.DataFrame(members_data)
                        if "created_at" in df_members.columns:
                            df_members["created_at_dt"] = pd.to_datetime(df_members["created_at"], errors="coerce")
                            df_valid_m = df_members.dropna(subset=["created_at_dt"]).copy()

                            if not df_valid_m.empty:
                                df_valid_m["Month"] = df_valid_m["created_at_dt"].dt.strftime("%Y-%m")
                                monthly_data = df_valid_m.groupby("Month").size().sort_index()

                                if not monthly_data.empty:
                                    fig2, ax2 = plt.subplots(figsize=(10, 3.8), facecolor="none")
                                    ax2.bar(
                                        monthly_data.index,
                                        monthly_data.values,
                                        color="#06b6d4",
                                        width=0.45,
                                    )
                                    ax2.set_axisbelow(True)
                                    ax2.grid(axis="y", linestyle="--", alpha=0.15, color="#64748b")
                                    ax2.tick_params(axis="x", colors="#94a3b8", rotation=45, labelsize=9)
                                    ax2.tick_params(axis="y", colors="#94a3b8", labelsize=9)
                                    ax2.set_ylabel("New Members", color="#94a3b8", fontweight="bold", fontsize=10)
                                    ax2.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
                                    for spine in ["top", "right"]:
                                        ax2.spines[spine].set_visible(False)
                                    ax2.spines["bottom"].set_color("#1e293b")
                                    ax2.spines["left"].set_color("#1e293b")
                                    plt.tight_layout()
                                    st.pyplot(fig2, use_container_width=True)
                                    plt.close(fig2)
                                else:
                                    st.info("Not enough date information to plot monthly trends.")
                            else:
                                st.info("Member joining date records not available.")
                        else:
                            st.info("Date information is missing from member records.")
                    else:
                        st.info("No members available to chart.")
            except Exception as e:
                st.error(f"Error generating member summary: {e}")

        # ========================================================
        # TAB 3: TRANSACTION SUMMARY (Original 2 Graphs + Table)
        # ========================================================
        with tab3:
            try:
                stat_t, trans_res = api_call("GET", f"{TRANS_URL}/show", params={"page": 1, "per_page": 1000})
                if stat_t == 200 and trans_res.get("status") == "success":
                    t_data = trans_res.get("data", {})
                    transactions = t_data.get("transaction", [])

                    if transactions:
                        df_t = pd.DataFrame(transactions)
                        if "status" in df_t.columns:
                            df_t["status_clean"] = df_t["status"].astype(str).str.strip().str.lower()
                        else:
                            df_t["status_clean"] = ""

                        total_trans = len(df_t)
                        issued_count = int((df_t["status_clean"] == "issued").sum())
                        returned_count = int(df_t["status_clean"].str.contains("returned", na=False).sum())

                        if "fine_amount" in df_t.columns:
                            df_t["fine_amount"] = pd.to_numeric(df_t["fine_amount"], errors="coerce").fillna(0)
                            total_fines = float(df_t["fine_amount"].sum())
                        else:
                            total_fines = 0.0

                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Total Transactions", total_trans)
                        with col2:
                            st.metric("Currently Issued", issued_count)
                        with col3:
                            st.metric("Books Returned", returned_count)
                        with col4:
                            st.metric("Total Fines Collected", f"₹ {total_fines:,.2f}")

                        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

                        col1, col2 = st.columns([1, 1.4])
                        with col1:
                            with st.container(border=True):
                                st.markdown(
                                    """
                                    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
                                        <span style="font-size: 13px; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.8px;">Transaction Status</span>
                                        <span class="badge-pill badge-active">Flow</span>
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )
                                if "status" in df_t.columns:
                                    df_t["status_title"] = df_t["status"].astype(str).str.strip().str.title()
                                    status_counts = df_t["status_title"].value_counts().sort_index()
                                else:
                                    status_counts = pd.Series(dtype=int)

                                if not status_counts.empty:
                                    fig, ax = plt.subplots(figsize=(5, 3.8), facecolor="none")
                                    ax.plot(
                                        status_counts.index,
                                        status_counts.values,
                                        color="#06b6d4",
                                        marker="o",
                                        linestyle="-",
                                        linewidth=2.5,
                                        markersize=8,
                                        markeredgecolor="#0b0f19",
                                        markeredgewidth=2,
                                    )
                                    ax.set_axisbelow(True)
                                    ax.grid(axis="y", linestyle="--", alpha=0.15, color="#64748b")
                                    ax.tick_params(axis="x", colors="#94a3b8", labelsize=9)
                                    ax.tick_params(axis="y", colors="#94a3b8", labelsize=9)
                                    ax.set_ylabel("Total Count", color="#94a3b8", fontweight="bold", fontsize=10)
                                    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
                                    ax.set_ylim(bottom=0)
                                    for spine in ["top", "right"]:
                                        ax.spines[spine].set_visible(False)
                                    ax.spines["bottom"].set_color("#1e293b")
                                    ax.spines["left"].set_color("#1e293b")
                                    plt.tight_layout()
                                    st.pyplot(fig, use_container_width=True)
                                    plt.close(fig)
                                else:
                                    st.info("No status data available to chart.")

                        with col2:
                            with st.container(border=True):
                                st.markdown(
                                    """
                                    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
                                        <span style="font-size: 13px; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.8px;">Books Issued Monthly</span>
                                        <span class="badge-pill badge-issued">Checkouts</span>
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )
                                if "issue_date" in df_t.columns:
                                    df_t["issue_date_dt"] = pd.to_datetime(df_t["issue_date"], errors="coerce")
                                    df_valid_t = df_t.dropna(subset=["issue_date_dt"]).copy()

                                    if not df_valid_t.empty:
                                        df_valid_t["Month"] = df_valid_t["issue_date_dt"].dt.strftime("%Y-%m")
                                        monthly_issues = df_valid_t.groupby("Month").size().sort_index()

                                        if not monthly_issues.empty:
                                            fig2, ax2 = plt.subplots(figsize=(7, 3.8), facecolor="none")
                                            ax2.bar(
                                                monthly_issues.index,
                                                monthly_issues.values,
                                                color="#6366f1",
                                                width=0.45,
                                            )
                                            ax2.set_axisbelow(True)
                                            ax2.grid(axis="y", linestyle="--", alpha=0.15, color="#64748b")
                                            ax2.tick_params(axis="x", colors="#94a3b8", rotation=45, labelsize=9)
                                            ax2.tick_params(axis="y", colors="#94a3b8", labelsize=9)
                                            ax2.set_ylabel("Total Books Issued", color="#94a3b8", fontweight="bold", fontsize=10)
                                            ax2.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
                                            for spine in ["top", "right"]:
                                                ax2.spines[spine].set_visible(False)
                                            ax2.spines["bottom"].set_color("#1e293b")
                                            ax2.spines["left"].set_color("#1e293b")
                                            plt.tight_layout()
                                            st.pyplot(fig2, use_container_width=True)
                                            plt.close(fig2)
                                        else:
                                            st.info("Not enough date information to plot monthly trends.")
                                    else:
                                        st.info("No valid issue dates recorded yet.")
                                else:
                                    st.info("No issue dates recorded yet.")

                        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

                        with st.container(border=True):
                            st.markdown(
                                """
                                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
                                    <span style="font-size: 13px; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.8px;">Recent Circulation Activities</span>
                                    <span class="badge-pill badge-active">Live Feed</span>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                            if "id" in df_t.columns:
                                df_recent = df_t.sort_values(by="id", ascending=False).head(6).copy()
                                for col in ["issue_date", "due_date", "return_date"]:
                                    if col in df_recent.columns:
                                        df_recent[col] = (
                                            pd.to_datetime(df_recent[col], errors="coerce")
                                            .dt.strftime("%Y-%m-%d")
                                            .fillna("-")
                                        )

                                if "fine_amount" in df_recent.columns:
                                    df_recent["fine_amount"] = df_recent["fine_amount"].apply(
                                        lambda x: f"₹ {x:,.2f}" if pd.notnull(x) else "₹ 0.00"
                                    )

                                df_recent = df_recent.rename(
                                    columns={
                                        "id": "Transaction ID",
                                        "member_id": "Member ID",
                                        "book_id": "Book ID",
                                        "issue_date": "Issue Date",
                                        "due_date": "Due Date",
                                        "return_date": "Return Date",
                                        "fine_amount": "Fine",
                                        "status": "Status",
                                    }
                                )
                                drop_cols = ["Month", "status_clean", "status_title", "issue_date_dt"]
                                df_recent = df_recent.drop(
                                    columns=[c for c in drop_cols if c in df_recent.columns],
                                    errors="ignore",
                                )
                                st.dataframe(df_recent, use_container_width=True, hide_index=True)
                            else:
                                st.info("Could not load recent activities.")
                    else:
                        st.info("No transactions recorded in the library yet.")
                else:
                    st.error(f"Failed to load transactions: {trans_res.get('message', 'Server error')}")
            except Exception as e:
                st.error(f"Error generating transaction summary: {e}")

    # ========================================================
    # 2. BOOK CATALOG
    # ========================================================
    elif page == "Books":
        st.markdown(
            """
            <div style="margin-bottom: 20px;">
                <h1 style="margin: 0; font-size: 26px;">📚 Book Catalog</h1>
                <p style="color: #94a3b8; font-size: 13.5px; margin-top: 4px;">Explore, filter, update, and manage your library inventory</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        tab1, tab2, tab3, tab4 = st.tabs(["📖 Browse All", "🔍 Search Book", "✏️ Update Book", "🗑️ Delete Book"])

        # Tab 1: Browse
        with tab1:
            if "b_page" not in st.session_state:
                st.session_state.b_page = 1

            with st.container(border=True):
                col_a, col_b = st.columns([1, 2.5])
                with col_a:
                    b_size = st.selectbox("Display per page", [6, 12, 24], index=1, key="b_size_sel")
                with col_b:
                    filter_kw = st.text_input("Quick filter by title or author", placeholder="Type to filter...", key="b_filter_kw")

                stat, res = api_call(
                    "GET", f"{BOOK_URL}/show", params={"page": st.session_state.b_page, "per_page": b_size}
                )

                if stat == 200 and res.get("status") == "success":
                    data = res.get("data", {})
                    books = data.get("title", [])
                    total_pages = max(1, data.get("total pages", 1))

                    if books:
                        df = pd.DataFrame(books)
                        if filter_kw:
                            df = df[
                                df["title"].str.contains(filter_kw, case=False, na=False)
                                | df["author"].str.contains(filter_kw, case=False, na=False)
                            ]

                        st.dataframe(
                            df,
                            use_container_width=True,
                            hide_index=True,
                            column_config={
                                "id": st.column_config.NumberColumn("ID", format="#%d"),
                                "title": st.column_config.TextColumn("Title", width="large"),
                                "author": st.column_config.TextColumn("Author"),
                                "category": st.column_config.TextColumn("Category"),
                                "quantity": st.column_config.NumberColumn("Total Copies"),
                                "available_quantity": st.column_config.NumberColumn("Available"),
                                "publishes_year": st.column_config.NumberColumn("Year", format="%d"),
                                "created_at": st.column_config.DateColumn("Added Date"),
                            },
                        )

                        # Clean modern pagination
                        p1, p2, p3 = st.columns([1, 2, 1])
                        with p1:
                            if st.button("⬅ Previous", key="prev_b_btn", disabled=st.session_state.b_page <= 1):
                                st.session_state.b_page -= 1
                                st.rerun()
                        with p2:
                            st.markdown(
                                f"<div style='text-align:center; padding-top:8px; color:#94a3b8; font-size:13px;'>Page <b style='color:#f8fafc;'>{st.session_state.b_page}</b> of <b style='color:#f8fafc;'>{total_pages}</b></div>",
                                unsafe_allow_html=True,
                            )
                        with p3:
                            if st.button("Next ➡", key="next_b_btn", disabled=st.session_state.b_page >= total_pages):
                                st.session_state.b_page += 1
                                st.rerun()
                    else:
                        st.info("No books found.")
                else:
                    st.error(res.get("message", "Failed to fetch books."))

        # Tab 2: Search
        with tab2:
            with st.container(border=True):
                st.markdown("<p style='font-size:15px; font-weight:700; color:#f8fafc; margin-bottom:12px;'>Search Catalog</p>", unsafe_allow_html=True)
                search_by = st.radio("Search query type:", ["Book ID", "Title Keywords"], horizontal=True, key="search_b_by")

                if search_by == "Book ID":
                    bid = st.number_input("Book ID", min_value=1, step=1, key="search_bid")
                    params = {"id": int(bid)}
                else:
                    btitle = st.text_input("Title keywords", placeholder="e.g. Python, Algorithms", key="search_btitle")
                    params = {"title": btitle.strip()}

                if st.button("Search Book", key="btn_exec_search_book", type="primary"):
                    if search_by == "Title Keywords" and not params.get("title"):
                        st.warning("Please enter a title keyword to search.")
                    else:
                        stat, res = api_call("GET", f"{BOOK_URL}/search", params=params)
                        if stat == 200 and res.get("status") == "success":
                            found = res.get("data", [])
                            if found:
                                st.success(f"Found {len(found)} matching record(s):")
                                st.dataframe(pd.DataFrame(found), use_container_width=True, hide_index=True)
                            else:
                                st.warning("No matching books found in catalog.")
                        else:
                            st.error(res.get("message", "Book not found."))

        # Tab 3: Update
        with tab3:
            with st.container(border=True):
                st.markdown("<p style='font-size:15px; font-weight:700; color:#f8fafc; margin-bottom:12px;'>Modify Book Details</p>", unsafe_allow_html=True)
                c_id, c_btn = st.columns([2, 1])
                with c_id:
                    edit_id = st.number_input("Enter Book ID to load", min_value=1, step=1, key="load_edit_bid")
                with c_btn:
                    st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)
                    load_act = st.button("Load Details", key="load_b_edit_btn")

                if load_act:
                    stat, res = api_call("GET", f"{BOOK_URL}/search", params={"id": int(edit_id)})
                    if stat == 200 and res.get("data"):
                        b = res["data"][0]
                        st.session_state["edit_book"] = b
                        st.toast("Book details loaded!", icon="✅")
                    else:
                        st.error("Book not found.")

                if "edit_book" in st.session_state:
                    b = st.session_state["edit_book"]
                    st.divider()
                    with st.form("form_edit_book"):
                        col_e1, col_e2 = st.columns(2)
                        with col_e1:
                            utitle = st.text_input("Title", value=b.get("title", ""))
                            uauthor = st.text_input("Author", value=b.get("author", ""))
                            ucat = st.text_input("Category", value=b.get("category", ""))
                        with col_e2:
                            uqty = st.number_input("Total Quantity", min_value=0, value=int(b.get("quantity", 1)))
                            uyear = st.number_input(
                                "Published Year",
                                min_value=1000,
                                max_value=2100,
                                value=int(b.get("publishes_year") or b.get("publishes year") or 2020),
                            )

                        save_btn = st.form_submit_button("Save Changes", type="primary", use_container_width=True)
                        if save_btn:
                            payload = {
                                "title": utitle.strip(),
                                "author": uauthor.strip(),
                                "category": ucat.strip(),
                                "quantity": int(uqty),
                                "publishes_year": int(uyear),
                            }
                            stat, res = api_call("PUT", f"{BOOK_URL}/update/{int(edit_id)}", json=payload)
                            if stat == 200 and res.get("status") == "success":
                                st.success("Book updated successfully!")
                                st.session_state.pop("edit_book", None)
                            else:
                                st.error(res.get("message", "Update failed."))

        # Tab 4: Delete
        with tab4:
            with st.container(border=True):
                st.markdown("<p style='font-size:15px; font-weight:700; color:#f8fafc; margin-bottom:12px;'>Remove Book From Catalog</p>", unsafe_allow_html=True)
                c_del_id, c_del_btn = st.columns([2, 1])
                with c_del_id:
                    del_id = st.number_input("Book ID to delete", min_value=1, step=1, key="del_bid_input")
                with c_del_btn:
                    st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)
                    chk_act = st.button("Inspect Book", key="chk_del_b")

                if chk_act:
                    stat, res = api_call("GET", f"{BOOK_URL}/search", params={"id": int(del_id)})
                    if stat == 200 and res.get("data"):
                        st.session_state["to_del_b"] = res["data"][0]
                    else:
                        st.error("Book not found.")

                if "to_del_b" in st.session_state:
                    tb = st.session_state["to_del_b"]
                    st.divider()
                    st.warning(f"Are you sure you want to permanently delete **{tb.get('title')}** by {tb.get('author')}?")

                    if st.button("Confirm Permanent Deletion", type="primary", key="confirm_del_b_btn"):
                        stat, res = api_call("DELETE", f"{BOOK_URL}/delete/{int(del_id)}")
                        if stat == 200 and res.get("status") == "success":
                            st.success("Book deleted successfully.")
                            st.session_state.pop("to_del_b", None)
                        else:
                            st.error(res.get("message", "Failed to delete book."))

    # ========================================================
    # 3. CIRCULATION (TRANSACTIONS)
    # ========================================================
    elif page == "Circulation":
        st.markdown(
            """
            <div style="margin-bottom: 20px;">
                <h1 style="margin: 0; font-size: 26px;">🔄 Circulation & Loans</h1>
                <p style="color: #94a3b8; font-size: 13.5px; margin-top: 4px;">Handle book issues, returns, and real-time loan tracking</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        t1, t2, t3 = st.tabs(["📤 Issue Book", "📥 Return Book", "📋 All Transactions"])

        # Issue Book
        with t1:
            with st.container(border=True):
                st.markdown("<p style='font-size:15px; font-weight:700; color:#f8fafc; margin-bottom:12px;'>Issue Book to Member</p>", unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                with c1:
                    mid_inp = st.number_input("Member ID", min_value=1, step=1, key="issue_m_id")
                with c2:
                    bid_inp = st.number_input("Book ID", min_value=1, step=1, key="issue_b_id")

                st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
                if st.button("Authorize & Issue Book", type="primary", key="do_issue_btn"):
                    stat, res = api_call("POST", f"{TRANS_URL}/issue", json={"member_id": int(mid_inp), "book_id": int(bid_inp)})
                    if stat == 200 and res.get("status") == "success":
                        st.success("Book issued successfully!")
                        st.json(res.get("data", {}))
                    else:
                        st.error(res.get("message", "Could not issue book."))

        # Return Book
        with t2:
            with st.container(border=True):
                st.markdown("<p style='font-size:15px; font-weight:700; color:#f8fafc; margin-bottom:12px;'>Process Book Return</p>", unsafe_allow_html=True)
                tid_inp = st.number_input("Transaction ID", min_value=1, step=1, key="ret_t_id")

                st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
                if st.button("Confirm Return & Calculate Fine", type="primary", key="do_ret_btn"):
                    stat, res = api_call("POST", f"{TRANS_URL}/return", json={"transaction_id": int(tid_inp)})
                    if stat == 200 and res.get("status") == "success":
                        rinfo = res.get("data", {})
                        st.success("Book return processed successfully!")
                        fine_val = float(rinfo.get("fine amount", 0.0))
                        if fine_val > 0:
                            st.warning(f"Overdue fine assessed: ₹ {fine_val:,.2f}")
                        else:
                            st.info("No overdue fine incurred.")
                    else:
                        st.error(res.get("message", "Return processing failed."))

        # All Transactions
        with t3:
            with st.container(border=True):
                if "t_page" not in st.session_state:
                    st.session_state.t_page = 1

                stat, res = api_call("GET", f"{TRANS_URL}/show", params={"page": st.session_state.t_page, "per_page": 10})
                if stat == 200 and res.get("status") == "success":
                    data = res.get("data", {})
                    txs = data.get("transaction", [])
                    total_p = max(1, data.get("total_pages", 1))

                    if txs:
                        st.dataframe(pd.DataFrame(txs), use_container_width=True, hide_index=True)

                        c_p1, c_p2, c_p3 = st.columns([1, 2, 1])
                        with c_p1:
                            if st.button("⬅ Previous", key="prev_t_btn", disabled=st.session_state.t_page <= 1):
                                st.session_state.t_page -= 1
                                st.rerun()
                        with c_p2:
                            st.markdown(
                                f"<div style='text-align:center; padding-top:8px; color:#94a3b8; font-size:13px;'>Page <b style='color:#f8fafc;'>{st.session_state.t_page}</b> of <b style='color:#f8fafc;'>{total_p}</b></div>",
                                unsafe_allow_html=True,
                            )
                        with c_p3:
                            if st.button("Next ➡", key="next_t_btn", disabled=st.session_state.t_page >= total_p):
                                st.session_state.t_page += 1
                                st.rerun()
                    else:
                        st.info("No transactions recorded.")
                else:
                    st.error(res.get("message", "Failed to load transactions."))

    # ========================================================
    # 4. MEMBERS
    # ========================================================
    elif page == "Members":
        st.markdown(
            """
            <div style="margin-bottom: 20px;">
                <h1 style="margin: 0; font-size: 26px;">👥 Members Directory</h1>
                <p style="color: #94a3b8; font-size: 13.5px; margin-top: 4px;">Manage member profiles, contact records, and registration status</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        m1, m2, m3, m4 = st.tabs(["📋 Directory", "➕ Add Member", "✏️ Update Member", "🗑️ Delete Member"])

        # Directory
        with m1:
            with st.container(border=True):
                if "m_page" not in st.session_state:
                    st.session_state.m_page = 1

                stat, res = api_call("GET", f"{MEMBER_URL}/show", params={"page": st.session_state.m_page, "per_page": 10})
                if stat == 200 and res.get("status") == "success":
                    data = res.get("data", {})
                    members = data.get("Members", [])
                    tot_p = max(1, data.get("total page", 1))

                    if members:
                        st.dataframe(pd.DataFrame(members), use_container_width=True, hide_index=True)

                        mp1, mp2, mp3 = st.columns([1, 2, 1])
                        with mp1:
                            if st.button("⬅ Previous", key="prev_m_btn", disabled=st.session_state.m_page <= 1):
                                st.session_state.m_page -= 1
                                st.rerun()
                        with mp2:
                            st.markdown(
                                f"<div style='text-align:center; padding-top:8px; color:#94a3b8; font-size:13px;'>Page <b style='color:#f8fafc;'>{st.session_state.m_page}</b> of <b style='color:#f8fafc;'>{tot_p}</b></div>",
                                unsafe_allow_html=True,
                            )
                        with mp3:
                            if st.button("Next ➡", key="next_m_btn", disabled=st.session_state.m_page >= tot_p):
                                st.session_state.m_page += 1
                                st.rerun()
                    else:
                        st.info("No members found.")
                else:
                    st.error(res.get("message", "Failed to load members."))

        # Add Member
        with m2:
            with st.container(border=True):
                st.markdown("<p style='font-size:15px; font-weight:700; color:#f8fafc; margin-bottom:12px;'>Register New Member</p>", unsafe_allow_html=True)
                with st.form("form_add_mem"):
                    aname = st.text_input("Full Name *", placeholder="e.g. Alice Smith")
                    aphone = st.text_input("Phone Number *", placeholder="e.g. +91 9876543210")
                    aaddr = st.text_area("Residential Address", placeholder="Street, City, Postal Code")

                    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
                    if st.form_submit_button("Create Member Account", type="primary", use_container_width=True):
                        if not aname.strip() or not aphone.strip():
                            st.warning("Please enter name and phone number.")
                        else:
                            stat, res = api_call(
                                "POST",
                                f"{MEMBER_URL}/create",
                                json={"name": aname.strip(), "phone_no": aphone.strip(), "address": aaddr.strip()},
                            )
                            if stat in [200, 201] and res.get("status") == "success":
                                st.success(f"Member created successfully! Member ID: #{res.get('data', {}).get('id')}")
                            else:
                                st.error(res.get("message", "Failed to create member."))

        # Update Member
        with m3:
            with st.container(border=True):
                st.markdown("<p style='font-size:15px; font-weight:700; color:#f8fafc; margin-bottom:12px;'>Update Member Records</p>", unsafe_allow_html=True)
                c_mid, c_mbtn = st.columns([2, 1])
                with c_mid:
                    up_mid = st.number_input("Member ID to load", min_value=1, step=1, key="load_up_mid")
                with c_mbtn:
                    st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)
                    load_m_act = st.button("Load Member", key="btn_load_m")

                if load_m_act:
                    stat, res = api_call("GET", f"{MEMBER_URL}/search", params={"id": int(up_mid)})
                    if stat == 200 and res.get("data"):
                        st.session_state["edit_mem"] = res["data"][0]
                        st.toast("Member loaded!", icon="✅")
                    else:
                        st.error("Member not found.")

                if "edit_mem" in st.session_state:
                    em = st.session_state["edit_mem"]
                    st.divider()
                    with st.form("form_up_mem"):
                        uname = st.text_input("Name", value=em.get("name", ""))
                        uphone = st.text_input("Phone", value=em.get("phone") or em.get("phone_no", ""))
                        uaddr = st.text_area("Address", value=em.get("address", ""))

                        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
                        if st.form_submit_button("Save Member Updates", type="primary", use_container_width=True):
                            payload = {
                                "name": uname.strip(),
                                "phone_no": uphone.strip(),
                                "phone no": uphone.strip(),
                                "address": uaddr.strip(),
                            }
                            stat, res = api_call("PUT", f"{MEMBER_URL}/update/{int(up_mid)}", json=payload)
                            if stat == 200 and res.get("status") == "success":
                                st.success("Member updated successfully!")
                                st.session_state.pop("edit_mem", None)
                            else:
                                st.error(res.get("message", "Update failed."))

        # Delete Member
        with m4:
            with st.container(border=True):
                st.markdown("<p style='font-size:15px; font-weight:700; color:#f8fafc; margin-bottom:12px;'>Delete Member Profile</p>", unsafe_allow_html=True)
                d_mid = st.number_input("Member ID to delete", min_value=1, step=1, key="del_mid_inp")

                st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
                if st.button("Delete Member Profile", type="primary", key="btn_del_mem_action"):
                    stat, res = api_call("DELETE", f"{MEMBER_URL}/delete/{int(d_mid)}")
                    if stat == 200 and res.get("status") == "success":
                        st.success("Member deleted successfully.")
                    else:
                        st.error(res.get("message", "Deletion failed."))

    # ========================================================
    # 5. MEMBERSHIPS
    # ========================================================
    elif page == "Memberships":
        st.markdown(
            """
            <div style="margin-bottom: 20px;">
                <h1 style="margin: 0; font-size: 26px;">🎫 Membership Management</h1>
                <p style="color: #94a3b8; font-size: 13.5px; margin-top: 4px;">Monitor active subscriptions and assign new membership tiers</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        ms1, ms2 = st.tabs(["📑 All Subscriptions", "➕ Assign Subscription"])

        with ms1:
            with st.container(border=True):
                stat, res = api_call("GET", f"{MEMBER_URL}/membership/show", params={"page": 1, "per_page": 50})
                if stat == 200 and res.get("status") == "success":
                    mships = res.get("data", {}).get("memberships", [])
                    if mships:
                        st.dataframe(pd.DataFrame(mships), use_container_width=True, hide_index=True)
                    else:
                        st.info("No active memberships found.")
                else:
                    st.error(res.get("message", "Failed to load memberships."))

        with ms2:
            with st.container(border=True):
                st.markdown("<p style='font-size:15px; font-weight:700; color:#f8fafc; margin-bottom:12px;'>Assign Membership Plan</p>", unsafe_allow_html=True)
                with st.form("form_assign_mship"):
                    as_mid = st.number_input("Member ID", min_value=1, step=1)
                    as_type = st.selectbox("Plan Duration", ["1 week", "1 month", "6 month", "1 year"])

                    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
                    if st.form_submit_button("Activate Subscription", type="primary", use_container_width=True):
                        payload = {"member_id": int(as_mid), "membership_type": as_type}
                        stat, res = api_call("POST", f"{MEMBER_URL}/membership", json=payload)
                        if stat == 200 and res.get("status") == "success":
                            d = res.get("data", {})
                            st.success(
                                f"Plan activated for {d.get('member_name', f'Member #{as_mid}')}! Valid until: {d.get('expiry_date')}"
                            )
                        else:
                            st.error(res.get("message", "Failed to assign membership."))

    # ========================================================
    # 6. QUICK ADD BOOK
    # ========================================================
    elif page == "Add Book":
        st.markdown(
            """
            <div style="margin-bottom: 20px;">
                <h1 style="margin: 0; font-size: 26px;">➕ Add Book to Catalog</h1>
                <p style="color: #94a3b8; font-size: 13.5px; margin-top: 4px;">Instantly register new titles into the central library inventory</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.container(border=True):
            with st.form("form_quick_add"):
                c1, c2 = st.columns(2)
                with c1:
                    ntitle = st.text_input("Title *", placeholder="e.g. Design Patterns")
                    nauthor = st.text_input("Author *", placeholder="e.g. Erich Gamma")
                    ncat = st.text_input("Category *", placeholder="e.g. Computer Science")
                with c2:
                    nqty = st.number_input("Quantity *", min_value=1, max_value=2000, value=5)
                    nyear = st.number_input("Publication Year", min_value=1000, max_value=2100, value=2022)
                    ndate = st.date_input("Catalog Date", value=date.today())

                st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
                if st.form_submit_button("Register Book into Catalog", type="primary", use_container_width=True):
                    if not ntitle.strip() or not nauthor.strip() or not ncat.strip():
                        st.warning("Please fill in all required title, author, and category fields.")
                    else:
                        payload = {
                            "title": ntitle.strip(),
                            "author": nauthor.strip(),
                            "category": ncat.strip(),
                            "quantity": int(nqty),
                            "publishes_year": int(nyear),
                            "created_at": ndate.strftime("%Y-%m-%d"),
                        }
                        stat, res = api_call("POST", f"{BOOK_URL}/create", json=payload)
                        if stat in [200, 201] and res.get("status") == "success":
                            st.success(f"'{ntitle}' added successfully with {nqty} copies!")
                        else:
                            st.error(res.get("message", "Failed to add book."))

    # ========================================================
    # 7. FINES
    # ========================================================
    elif page == "Fines":
        st.markdown(
            """
            <div style="margin-bottom: 20px;">
                <h1 style="margin: 0; font-size: 26px;">💰 Overdue Fines Ledger</h1>
                <p style="color: #94a3b8; font-size: 13.5px; margin-top: 4px;">Monitor collected penalties and outstanding overdue fine accounts</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        stat, res = api_call("GET", f"{TRANS_URL}/fines", params={"page": 1, "per_page": 50})
        if stat == 200 and res.get("status") == "success":
            data = res.get("data", {})
            fines = data.get("fines", [])
            tot_rev = data.get("total_fine_collected", 0.0)

            st.metric("Total Fine Revenue Collected", f"₹ {tot_rev:,.2f}")
            st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

            with st.container(border=True):
                st.markdown("<p style='font-size:15px; font-weight:700; color:#f8fafc; margin-bottom:12px;'>Fine Records Ledger</p>", unsafe_allow_html=True)
                if fines:
                    st.dataframe(pd.DataFrame(fines), use_container_width=True, hide_index=True)
                else:
                    st.info("No overdue fine records found.")
        else:
            st.error(res.get("message", "Failed to load fine records."))

    # ========================================================
    # 8. SETTINGS
    # ========================================================
    elif page == "Settings":
        st.markdown(
            """
            <div style="margin-bottom: 20px;">
                <h1 style="margin: 0; font-size: 26px;">⚙️ System Settings</h1>
                <p style="color: #94a3b8; font-size: 13.5px; margin-top: 4px;">Manage account credentials and administrator security preferences</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.container(border=True):
            st.markdown("<p style='font-size:15px; font-weight:700; color:#f8fafc; margin-bottom:12px;'>Update Password</p>", unsafe_allow_html=True)
            with st.form("form_change_pw"):
                ch_u = st.text_input("Username", value=user_info.get("username", ""))
                ch_old = st.text_input("Current Password", type="password")
                ch_new = st.text_input("New Password", type="password")
                ch_conf = st.text_input("Confirm New Password", type="password")

                st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
                if st.form_submit_button("Update Password", type="primary", use_container_width=True):
                    if not ch_u.strip() or not ch_old or not ch_new:
                        st.warning("Please fill in all password fields.")
                    elif ch_new != ch_conf:
                        st.error("New passwords do not match.")
                    else:
                        payload = {
                            "username": ch_u.strip().lower(),
                            "old_password": ch_old,
                            "new_password": ch_new,
                        }
                        stat, res = api_call("PUT", f"{AUTH_URL}/change_password", json=payload)
                        if stat == 200 and res.get("status") == "success":
                            st.success("Password changed successfully!")
                        else:
                            st.error(res.get("message", "Failed to update password."))

    # ========================================================
    # 9. MY PROFILE
    # ========================================================
    elif page == "Profile":
        st.markdown(
            """
            <div style="margin-bottom: 20px;">
                <h1 style="margin: 0; font-size: 26px;">👤 Administrator Profile</h1>
                <p style="color: #94a3b8; font-size: 13.5px; margin-top: 4px;">View account information and security credentials</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.container(border=True):
            col_prof_avatar, col_prof_details = st.columns([1, 4])
            with col_prof_avatar:
                st.markdown(
                    f"""
                    <div style="width: 80px; height: 80px; border-radius: 50%; background: linear-gradient(135deg, #6366f1, #8b5cf6); display: flex; align-items: center; justify-content: center; font-size: 32px; font-weight: 800; color: white; box-shadow: 0 8px 24px rgba(99, 102, 241, 0.45); margin: 8px auto;">
                        {user_name[0].upper()}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with col_prof_details:
                st.markdown(f"<h3 style='margin:0; font-size:22px;'>{user_name}</h3>", unsafe_allow_html=True)
                st.markdown(
                    f"<p style='color:#94a3b8; margin:2px 0 12px 0;'>@{user_info.get('username', 'user')} &nbsp;•&nbsp; <span class='badge-pill badge-active'>{user_role}</span></p>",
                    unsafe_allow_html=True,
                )
                st.markdown(f"<span style='font-size:13px; color:#64748b;'>Administrator Identifier: #{user_info.get('id', 'N/A')}</span>", unsafe_allow_html=True)

            st.divider()
            if st.button("Sign Out of Session", type="primary", use_container_width=True):
                if logout_callback:
                    logout_callback()
                else:
                    st.session_state.authenticated = False
                    st.session_state.user_data = None
                    st.session_state.cookies = {}
                    st.rerun()
