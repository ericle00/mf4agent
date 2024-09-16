import streamlit as st
from typing import Callable, List, Any, Optional
from streamlit_authenticator import Authenticate
from streamlit_authenticator.utilities import LogoutError, Validator

class CustomAuthenticate(Authenticate):
    def __init__(self, 
                 credentials: dict, 
                 cookie_name: str, 
                 cookie_key: str, 
                 cookie_expiry_days: float = 30, 
                 pre_authorized: List[str] | None = None,
                 validator: Optional[Validator]=None, 
                 auto_hash: bool=True):
        super().__init__(credentials, 
                         cookie_name, 
                         cookie_key, 
                         cookie_expiry_days, 
                         pre_authorized,
                         validator,
                         auto_hash)
        
    def logout(self, 
               button_name: str = 'Logout', 
               location: str = 'main', 
               key: str = 'Logout', 
               callback: Callable[..., Any] | None = None,
               *btn_args, **btn_kwargs):
        """
        Creates a logout button.

        Parameters
        ----------
        button_name: str
            Rendered name of the logout button.
        location: str
            Location of the logout button i.e. main, sidebar or unrendered.
        key: str
            Unique key to be used in multi-page applications.
        callback: callable, optional
            Optional callback function that will be invoked on submission.
        """
        if not st.session_state['authentication_status']:
            raise LogoutError('User must be logged in to use the logout button')
        if location not in ['main', 'sidebar', 'unrendered']:
            raise ValueError("Location must be one of 'main' or 'sidebar' or 'unrendered'")
        if location == 'main':
            if st.button(button_name, key=key, *btn_args, **btn_kwargs):
                self.authentication_controller.logout()
                self.cookie_controller.delete_cookie()
                if callback:
                    callback({})
        elif location == 'sidebar':
            if st.sidebar.button(button_name, key=key, *btn_args, **btn_kwargs):
                self.authentication_controller.logout()
                self.cookie_controller.delete_cookie()
                if callback:
                    callback({})
        elif location == 'unrendered':
            if st.session_state['authentication_status']:
                self.authentication_controller.logout()
                self.cookie_controller.delete_cookie()