import os
import streamlit as st

import yaml
from yaml.loader import SafeLoader

from utils.markdown import MD
from gui.keys.st_ss import ST_SS                                            
from streamlit_authenticator import Authenticate
from gui.layout.authenticator.custom_authenticate import CustomAuthenticate
                                
                                                               
def render_authenticator():
    """
    Render the login widget and handle authentication.
    
    Returns:
        bool: Authentication status
    """
    st_ss = st.session_state

    working_folder_path = st_ss[ST_SS.PATH_WORKING_FOLDER_KEY]
    
    # Import the YAML file
    credentials_filepath = os.path.join(working_folder_path, "config/credentials.yaml")
    with open(credentials_filepath) as file:
        config = yaml.load(file, Loader=SafeLoader)

    # Create the authenticator object:
    authenticator = CustomAuthenticate(
        credentials=config["credentials"],
        cookie_name=config["cookie"]["name"],
        cookie_key=config["cookie"]["key"],
        cookie_expiry_days=config["cookie"]["expiry_days"],
        pre_authorized=config["pre-authorized"]
    )
    
    # Render the login widget by providing a name for the form and its location (i.e., sidebar or main):
    name, authentication_status, username = authenticator.login(location="main")

    # Handle authentication status
    if st_ss["authentication_status"]:
        col1, col2, col3 = st.columns([0.3,0.57,0.12])
        # Show user name and logout button
        with col1:
            # User name
            st.markdown(f"{MD.H3} 🤗 {name}")
            
        with col2:
            # Title of the agent
            st.markdown(f"{MD.H3} MF4 AGENT 💬")
        with col3:
            authenticator.logout(button_name="Logout 🚪", 
                                 location="main",
                                 use_container_width=True)
    elif authentication_status == False:
        # Show error message on invalid credentials
        st.error("Username/password is incorrect")
    elif authentication_status == None:
        # Show warning message on no credentials
        st.warning("Please enter your username and password")
    return authentication_status 