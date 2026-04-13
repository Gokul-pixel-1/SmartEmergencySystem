import streamlit as st

def login():
    st.sidebar.title("Login Panel")

    role = st.sidebar.selectbox(
        "Select Role",
        ["Public", "Official Persons", "Admin"]
    )

    return role