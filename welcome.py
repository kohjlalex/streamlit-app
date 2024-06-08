import streamlit as st

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
    #     ### Want to learn more?
    #     - Check out [streamlit.io](https://streamlit.io)
    #     - Jump into our [documentation](https://docs.streamlit.io)
    #     - Ask a question in our [community
    #         forums](https://discuss.streamlit.io)
    #     ### See more complex demos
    #     - Use a neural net to [analyze the Udacity Self-driving Car Image
    #         Dataset](https://github.com/streamlit/demo-self-driving)
    #     - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
    """

#run main function
if __name__ == "__main__":
    menu(show_select_msg=True)
    main()       
