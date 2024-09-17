import streamlit as st

def set_page_configuration(is_logged_in):
    # Set default page configuration
    page_title = "Login and Register"
    page_icon = ":lock:"
    layout = "wide"

    # Modify page configuration if user is logged in
    if is_logged_in:
        page_title = "Home"
        page_icon = ":house:"

    st.set_page_config(layout=layout, page_title=page_title, page_icon=page_icon)
