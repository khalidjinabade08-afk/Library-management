import streamlit as st
import requests
import pandas as pd

base_url = "http://127.0.0.1:5501"
member_url = f"{base_url}/member"
book_url = f"{base_url}/book"
Activites = f"{base_url}/transaction"

if "page" not in st.session_state:
    st.session_state.page = "Overview"
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

if page == "Overview":
    st.title("Dashboard")
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

    with tab1:
        #  st.subheader("Member List")
        #  if "member_page" not in st.session_state:
        #         st.session_state.member_page = 1
        #  per_page = 4

        #  page_input = st.number_input("Page Number", min_value=1, value=int(st.session_state.member_page), step=1)
        #  st.session_state.member_page = int(page_input)

        #  response = requests.get(
        #         f"{member_url}/show",
        #         params={
        #                "page": st.session_state.member_page,
        #                "per_page": per_page
        #         }
        #  )

        #  data = response.json()

        #  if "Members" in data and data["Members"]:
        #         rows = []
        #         for member in data["Members"]:
        #                rows.append({
        #                "id": member.get('id',''),
        #                "name": member.get('name',''),
        #                "address": member.get('address',''),
        #                "Phone": member.get('phone no',''),
        #                "Membership Start Date": member.get('membership start date',''),
        #                "Membership End Date": member.get('membership end date',''),
        #                "Membership Status": member.get('membership status','')
        #                })
        #         df = pd.DataFrame(rows)
        #         st.dataframe(df, use_container_width=True, hide_index=True)

        #  else:
        #         st.warning("No members found")

        #  st.write(f"Current Page: {data.get('current page',1)} / {data.get('total page',1)}")

        #  col1, col2 = st.columns(2)

        #  with col1:
        #         if st.button("Previous"):
        #                if st.session_state.member_page > 1:
        #                       st.session_state.member_page -= 1
        #                       st.rerun()

        #  with col2:
        #         if st.button("Next"):
        #                if st.session_state.member_page < data.get("total page",1):
        #                       st.session_state.member_page += 1
        #                       st.rerun()

        # ==========================
        # ==========================
        # SHOW ALL MEMBERS
        # ==========================

        # Store current page
        if "member_page" not in st.session_state:
            st.session_state.member_page = 1

            # Top Card
            st.markdown(
                """
                    <div class="glass-card">
                        <div class="section-title">
                        Browse Members
                        </div>
                """,
                unsafe_allow_html=True,
            )

        col1, col2, col3 = st.columns([1, 1, 2])

        with col1:
            per_page = st.selectbox("Members Per Page", options=[4, 8, 12, 16], index=0)

        with col2:
            st.metric("Current Page", st.session_state.member_page)

        st.markdown("</div>", unsafe_allow_html=True)

        # API URL
        params = {"page": st.session_state.member_page, "per_page": per_page}

        get_url = f"{base_url}/member/show"  # Change according to your route

        response = requests.get(get_url, params=params)

        # Members Data Card
        st.markdown(
            """
            <div class="glass-card">
                <div class="section-title">
                    Member Records
            </div>
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

                    # Statistics
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric("Total Members", raw_data.get("total no", 0))

                    with col2:
                        st.metric("Total Pages", raw_data.get("total page", 0))

                    with col3:
                        st.metric("Current Page", raw_data.get("current page", 0))

                else:
                    st.warning("No members found.")

            else:
                st.error("Members data not found in API response.")

        else:
            st.error(f"Failed to fetch members. Status Code: {response.status_code}")

        st.markdown("</div>", unsafe_allow_html=True)

        # ==========================
        # PAGINATION BUTTONS
        # ==========================

        prev_col, center_col, next_col = st.columns([1, 2, 1])

        with prev_col:
            if st.button("⬅ Previous", use_container_width=True):
                if st.session_state.member_page > 1:
                    st.session_state.member_page -= 1
                    st.rerun()

        with center_col:
            st.markdown(
                f"""
                    <div style="
                        text-align:center;
                        font-size:20px;
                        font-weight:600;
                        padding-top:8px;
                        ">
                        Page {st.session_state.member_page}
                    </div>
                    """,
                unsafe_allow_html=True,
            )

        with next_col:
            if st.button("Next ➝", use_container_width=True):

                total_pages = raw_data.get("total page", 1)

                if st.session_state.member_page < total_pages:
                    st.session_state.member_page += 1
                    st.rerun()

    with tab2:
        st.subheader("Create Member")

        name = st.text_input("Member Name", key="member_name")
        phone_no = st.text_input("Phone Number", key="member_phone")
        address = st.text_area("Address", key="member_address")

        if st.button("Create Member", key="create_member_btn"):
            payload = {"name": name, "phone_no": phone_no, "address": address}
            response = requests.post(f"{member_url}/create", json=payload)
            data = response.json()

            if response.status_code == 200:
                st.success(data.get("message"))
                member_data = data.get("data", {})

                if member_data:
                    df = pd.DataFrame([member_data])
                    st.dataframe(df, use_container_width=True)
            else:
                st.error(data.get("message"))

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
                response = requests.get(
                    f"{member_url}/search", params={"id": member_id}
                )

                data = response.json()

                if response.status_code == 200:
                    st.success("Member Found")

                    if "data" in data:
                        df = pd.DataFrame(data["data"])
                        st.dataframe(df, use_container_width=True)

                    else:
                        st.write(data)
                else:
                    st.error(data.get("message", "member not found"))

        else:
            member_name = st.text_input("Member Name", key="search_member_name")

            if st.button("Search", key="search_name_btn"):
                response = requests.get(
                    f"{member_url}/search", params={"name": member_name}
                )

                data = response.json()

                if response.status_code == 200:
                    st.success("Member Found")

                    if "data" in data:
                        df = pd.DataFrame(data["data"])
                        st.dataframe(df, use_container_width=True)

                    else:
                        st.write(data)
                else:
                    st.error(data.get("message", "member not found"))

    with tab4:
        st.subheader("Update Member")

        member_id = st.number_input("Member ID", min_value=1, key="update_member_id")
        name = st.text_input("new name", key="update_member_name")
        phone_no = st.text_input("New Phone Number", key="update_member_phone")
        address = st.text_input("New Address", key="Upddate_member_address")

        if st.button("Update Member", key="update_member_btn"):
            payload = {"name": name, "phone_no": phone_no, "address": address}

            response = requests.put(f"{member_url}/update/{member_id}", json=payload)

            data = response.json()

            if response.status_code == 200:
                st.success(data.get("message"))

                member_info = [
                    f"Member ID: {member_id}",
                    f"Name: {name}",
                    f"Phone Number: {phone_no}",
                    f"Address: {address}",
                ]
                for item in member_info:
                    st.write("*", item)
            else:
                st.error(data.get("Message"))

    with tab5:
        st.subheader("Delete Member")

        member_id = st.number_input(
            "Member ID", min_value=1, step=1, key="delete_member"
        )
        st.write("Remove Member")
        if st.button("Delete Member"):
            response = requests.delete(
                f"{member_url}/delete/{member_id}",
                headers={"Authorization": f"Bearer {st.session_state.get('token','')}"},
            )
            data = response.json()

            if response.status_code == 200:
                st.success(data["message"])

            else:
                st.error(data.get("message", "Member not found"))
