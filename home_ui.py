import streamlit as st
import requests 
import pandas as pd

base_url = "http://127.0.0.1:5501"
member_url = f"{base_url}/member"
book_url = f"{base_url}/book"
Activites = f"{base_url}/transaction"

if "page" not in st.session_state:
    st.session_state.page="Overview"
with st.sidebar:
    st.title("Bookary 📖")

    st.markdown("MAIN MENU")

    if st.button("Overview",use_container_width=True):
            st.session_state.page="Overview"

    if st.button("Books", use_container_width=True):
            st.session_state.page="books"
        
    if st.button("Library Activities",use_container_width=True):
            st.session_state.page="transaction"

    if st.button("Members",use_container_width=True):
            st.session_state.page="member"

    st.divider()

    st.markdown("MANAGEMENT")
    if st.button("Report & Analytics", use_container_width=True):
            st.session_state.page="management"

    if st.button("Overdue Reminder", use_container_width=True):
            st.session_state.page="reminder"

    if st.button("Add Books", use_container_width=True):
            st.session_state.page="Add Book"

    if st.button("fines", use_container_width=True):
            st.session_state.page="Fines"

page = st.session_state.page

if page =="Overview":
       st.title("Dashboard")
elif page == "books":
    st.title("Books")
    tab1,tab2,tab3,tab4 = st.tabs(["View Books", "Add Book", "Update Book", "Delete Book"])

    with tab1:
           st.write("All Books")
    
    with tab2:
           st.write("Add Book")

    with tab3:
           st.write("Update Book")

    with tab4:
           st.write("Delete Book")

elif page == "member":
        st.title("Member")

        tab1, tab2, tab3, tab4 = st.tabs(["View Member", "Add Member", "Update Member", "Delete Member"])

        with tab1:
               st.write("Member List")

        with tab2:
              st.write("create Member")

        with tab3:
               st.number_input("Member ID", min_value=1)
               st.write("Update Member information")

        with tab4:
               st.number_input("Member ID",min_value=1)
               st.write("Remove member")

