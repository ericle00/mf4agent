import streamlit as st
from gui.keys.st_ss import ST_SS

def init_filter_conditions(st_ss) -> None:
    """
    Initialize filter conditions in the Streamlit session state.

    Parameters:
    st_ss (st.session_state): The Streamlit session state.

    Returns:
    None
    """
    if not ST_SS.FILTER_CONDITION_GUI_KEY in st_ss:
        st_ss[ST_SS.FILTER_CONDITION_GUI_KEY] = "(VehicleMode == b'VehicleMode_Running')"