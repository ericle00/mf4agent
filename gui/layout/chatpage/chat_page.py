import streamlit as st

from gui.keys.st_ss import ST_SS

from gui.layout.chatpage.chat_display import display_chat_history
from gui.layout.chatpage.chat_input import render_chat_input
                                                                                
def render() -> None:
    """Renders the chat interface, including chat history and input field."""
    st_ss = st.session_state
        
    # Init chat history
    render_init_chat_history(st_ss)
    
    # Display chat history
    display_chat_history(st_ss)
    
    # Render chat input
    render_chat_input(st_ss)

   
def render_init_chat_history(st_ss) -> None:
    """Initializes chat history and test chat history in session state if not already present."""
    if ST_SS.CHAT_HISTORY_KEY not in st_ss:
        st_ss[ST_SS.CHAT_HISTORY_KEY] = []
        
        



                    









        