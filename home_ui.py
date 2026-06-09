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

    if st.button("Add Books", use_container_width=True):
        st.session_state.page = "Add Book"

    if st.button("fines", use_container_width=True):
        st.session_state.page = "Fines"

    st.divider()

    st.markdown("SETTING & OTHERS")
    if st.button("Setting", use_container_width=True):
        st.session_state.page = "Setting"

    if st.button("Profile", use_container_width=True):
        st.session_state.page = "Profile"


page = st.session_state.page

# --- Overview / Dashboard ---
if page == "Overview":
    st.title("Dashboard")

# --- Books Page ---
elif page == "books":
    st.title("Books")
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
                "Books Per Page", options=[4, 8, 12, 16], index=0, key="book_per_page"
            )

        st.markdown("</div>", unsafe_allow_html=True)

        params = {"page": st.session_state.book_page, "per_page": per_page}

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
                st.error(f"Failed to fetch books. Status Code: {response.status_code}")
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

        if st.button("Search Book"):
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

        book_id = st.number_input("Book ID", min_value=1, step=1, key="update_book_id")

        if st.button("Load Book", key="load_book_btn"):
            try:
                response = requests.get(f"{book_url}/search", params={"id": book_id})

                if response.status_code == 200:
                    result = response.json()

                    if result.get("data"):
                        book = result["data"][0]

                        st.session_state.up_book_title = book.get("title", "")
                        st.session_state.up_book_author = book.get("author", "")
                        st.session_state.up_book_category = book.get("category", "")
                        st.session_state.up_book_quantity = book.get("quantity", 0)
                        st.session_state.up_book_year = book.get("publishes_year", 2000)

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

        if st.button("Update Book", key="submit_update_book"):
            payload = {
                "title": title,
                "author": author,
                "category": category,
                "quantity": quantity,
                "publishes_year": publishes_year,
            }

            try:
                response = requests.put(f"{book_url}/update/{book_id}", json=payload)

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

        delete_id = st.number_input("Book ID", min_value=1, step=1, key="delete_book")

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

        if st.button("Delete Book", key="confirm_delete_book"):
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
                    st.error(data.get("message", "Book not found or deletion failed."))

            except Exception as e:
                st.error(f"Deletion error: {e}")

elif page == "transaction":
    st.title("Library Activities")

    tab1, tab2, tab3 = st.tabs(["issue book", "return book", "show transaction"])

    # Tab 1: issue Book
    with tab1:
        st.subheader("Issue Book")

        member_id = st.number_input(
            "Member ID", min_value=1, step=1, key="issue_member_id"
        )
        book_id = st.number_input("Book ID", min_value=1, key="Issue_book_id")

        if st.button("Issue Book", key="issue_book_btn"):
            payload = {"member_id": int(member_id), "book_id": int(book_id)}
        try:
            response = requests.post(f"{base_url}/transaction/issue", json=payload)

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

        if st.button("Return Book", key="return_book_btn"):
            payload = {"transaction_id": int(transaction_id)}

            try:
                response = requests.post(f"{base_url}/transaction/return", json=payload)

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
                            <div style='text-align:center;padding-top:8px'>
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
        search_by = st.radio("Search by", ["Member ID", "Member Name"], horizontal=True)

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

elif page == "management":
    st.header("Membership Management")
    tab1, tab2, tab3 = st.tabs(
        ["Add Membership", "search membership", "Membership List"]
    )

    with tab1:
        st.subheader("Add Membership")

    with tab2:
        st.subheader("search membership")

    with tab3:
        st.subheader("Membership list")

# tab 2: add book
elif page == "Add Book":
    st.title("Add New Book")
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
    st.header("Fines")
