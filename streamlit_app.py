import os 
import streamlit as st

import gui.layout.authenticator.authenticator as authenticator
import gui.styles.styles as styles 
import gui.session.session as session
import gui.layout.side_bar.main_render as side_bar
import gui.layout.chatpage.chat_page as chat_page

from gui.keys.st_ss import ST_SS

# Initial page config
st.set_page_config(
    layout='wide',  # Setting layout to wide
    initial_sidebar_state='expanded',  # Expanding sidebar by default
)
        
# Add gui folder path as the root
if ST_SS.PATH_WORKING_FOLDER_KEY not in st.session_state:
    st.session_state[ST_SS.PATH_WORKING_FOLDER_KEY] =  os.path.dirname(os.path.abspath(__file__))

# Authentication
auth_status = authenticator.render_authenticator()

# If logged in
if auth_status:
    # Developer logged in
    st.session_state[ST_SS.DEVELOPER_LOGGED_IN_KEY] = st.session_state["username"] == "eric"

    # Render session once
    if ST_SS.SESSION_RENDER_FIRST_TIME_KEY not in st.session_state:
        st.session_state[ST_SS.SESSION_RENDER_FIRST_TIME_KEY] = False
        
    # Rendering GUI Page
    styles.render()
    session.render()
    side_bar.render()
    chat_page.render()
else:
    # Delete session
    keys_to_keep = ["FormSubmitter", "root_path", "name", "logout", "username", "init", "authentication_status"]
    keys_to_delete = [key for key in st.session_state.keys() if key not in keys_to_keep]
    for key in keys_to_delete:
        del st.session_state[key]