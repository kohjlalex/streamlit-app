import streamlit as st

def menu(show_select_msg=False):
    with st.sidebar:
        st.page_link("Main.py", label="Home", icon="🏠"),
        #st.page_link("pages/ebay-tele-notifications.py", label="Your Ebay Telegram Notifications Bot", icon="🛒")
        st.page_link("pages/1_🚀_stocks_automation.py", label="Stocks Health Screener", icon="🚀")
        st.page_link("pages/2_👷_automatic_filter.py", label="Web Scraper & PDF Manipulation", icon="👷")
        if show_select_msg:
            st.success("Select a demo above.")
