import streamlit as st

def menu(show_select_msg=False):
    with st.sidebar:
        st.page_link("welcome.py", label="Home", icon="🏠❤️")
        st.page_link("pages/ebay-tele-notifications.py", label="Your Ebay Telegram Notifications Bot", icon="🛒")
        if show_select_msg:
            st.success("Select a demo above.")
