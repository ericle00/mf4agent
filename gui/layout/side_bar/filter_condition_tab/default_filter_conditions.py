import streamlit as st

from gui.keys.st_ss import ST_SS
                
def render_default_filter_condition() -> None:
    """
    Renders the default filter condition section.

    Returns:
    None
    """
    # Default
    st.header("Default 🚚")
    
    default_condition_container()
        
        
def default_condition_container():
    DEFAULT_SIGNAL_OPTIONS = ["VehicleMode == b'VehicleMode_Running'", "None"]
    st.selectbox(label="Default", 
                 options=DEFAULT_SIGNAL_OPTIONS, 
                 index=0,
                 help="Default filter condition that will always be inserted to the agent.",
                 key=ST_SS.FILTER_CONDITION_DEFAULT_SELECT_BOX_KEY)     

    

