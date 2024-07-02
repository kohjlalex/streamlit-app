import os
#from menu import menu

import streamlit as st
import streamlit.components.v1 as components

def main():

    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )
    
    st.write("# Welcome to Streamlit! 👋")
    
    st.sidebar.success("Select a demo above.")
    
    st.markdown(
        """
       Welcome to my collection of streamlit applications. I hope these tools will automate and make your research and work more efficient 
        **👈 Select a demo from the sidebar** to see some examples!
    """
    )

#run main function
if __name__ == "__main__":
    #menu(show_select_msg=True)
    main()       
