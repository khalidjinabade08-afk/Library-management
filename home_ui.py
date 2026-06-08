import streamlit as st
import requests
import pandas as pd

base_url = "http://127.0.0.1:5501"
member_url = f"{base_url}/member"
book_url = f"{base_url}/book"
Activites = f"{base_url}/transaction"

if "page" not in st.session_state:
    st.session_state.page = "Overview"

# Sidebar Navigation
with st.sidebar:
    st.title("Bookary 📖")
    st.markdown("MAIN MENU")

    if st.button("Overview", use_container_width=True):
        st.session_state.page = "Overview"

    if st.button("Books", use_container_width=True):
        st.session_state.page = "books"

    if st.button("Library Activities", use_container_width=True):
        st.session_state.page = "transaction"

    if st.button("Members", use_container_width=True):
        st.session_state.page = "member"

    st.divider()

    st.markdown("MANAGEMENT")
    if st.button("Membership", use_container_width=True):
        st.session_state.page = "management"

    if st.button("Overdue Reminder", use_container_width=True):
        st.session_state.page = "reminder"

    if st.button("Add Books", use_container_width=True):
        st.session_state.page = "Add Book"

    if st.button("fines", use_container_width=True):
        st.session_state.page = "Fines"

page = st.session_state.page

# --- Overview / Dashboard ---
if page == "Overview":
    st.title("Dashboard")

# --- Books Page ---
elif page == "books":
    st.title("Books")
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["View Books", "Add Book", "search book", "Update Book", "Delete Book"]
    )

    with tab1:
        st.write("All Books")

    with tab2:
        st.write("Add Book")

    with tab3:
        st.number_input("Book ID", min_value=1, key="search_book")
        st.write("Search Book")

    with tab4:
        st.number_input("Book ID", min_value=1, key="update_book")
        st.write("Update Book")

    with tab5:
        st.number_input("book ID", min_value=1, key="delete_book")
        st.write("Delete Book")

# --- Members Page ---
elif page == "member":
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
            per_page = st.selectbox("Members Per Page", options=[4, 8, 12, 16], index=0)
        with col2:
            st.metric("Current Page", st.session_state.member_page)

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
                            st.metric("Current Page", raw_data.get("current page", 0))
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
                f'<div style="text-align:center; font-size:20px; font-weight:600; padding-top:8px;">Page {st.session_state.member_page}</div>',
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
        st.subheader("Create Member")
        name = st.text_input("Member Name", key="member_name")
        phone_no = st.text_input("Phone Number", key="member_phone")
        address = st.text_area("Address", key="member_address")

        if st.button("Create Member", key="create_member_btn"):
            payload = {"name": name, "phone_no": phone_no, "address": address}
            try:
                response = requests.post(f"{member_url}/create", json=payload)
                data = response.json()
                if response.status_code == 200:
                    st.success(data.get("message", "Member Created!"))
                    member_data = data.get("data", {})
                    if member_data:
                        df = pd.DataFrame([member_data])
                        st.dataframe(df, use_container_width=True)
                else:
                    st.error(data.get("message", "Failed to create member."))
            except Exception as e:
                st.error(f"Error connecting to backend: {e}")

    # Tab 3: Search Member
    with tab3:
        st.subheader("Search Member")
        search_by = st.radio(
            "Search by", ["Member ID", "Member Name"], key="search_type"
        )

        if search_by == "Member ID":
            member_id = st.number_input(
                "Member ID", min_value=1, key="search_member_id"
            )
            if st.button("Search", key="search_id_btn"):
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
            if st.button("Search", key="search_name_btn"):
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

        update_id = st.number_input("Member ID", min_value=1, key="update_member_id")

        if st.button("Load Member", key="load_member_btn"):
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
                        st.session_state.up_address_input = member.get("address", "")

                        st.success("Member loaded successfully! Fields updated below.")
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

        if st.button("Update Member", key="submit_update_btn"):
            if not up_name:
                st.warning("Please load a member or enter a name first.")
            else:
                payload = {"name": up_name, "phone no": up_phone, "address": up_address}
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
            response = requests.get(f"{member_url}/search", params={"id": delete_id})
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

        if st.button("Delete Member", key="confirm_delete_btn"):
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
                        data.get("message", "Member not found or deletion restricted.")
                    )
            except Exception as e:
                st.error(f"Deletion payload error: {e}")
