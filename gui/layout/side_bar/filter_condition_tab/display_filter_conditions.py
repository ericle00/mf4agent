import streamlit as st

from gui.keys.st_ss import ST_SS

from gui.layout.side_bar.filter_condition_tab.utils import extract_gui_filter_conditions                  
                                                          
def render_display_filter_conditions() -> None:
    """
    Renders the display filter conditions section.

    Returns:
    None
    """
    st.header("Display 👓")

    display_filter_conditions_container()
    
    
def display_filter_conditions_container():
    with st.container(border=True):
        gui_filter_conditions = extract_gui_filter_conditions()
        st.text_area(label="GUI filter condition(s)",
                     value= gui_filter_conditions,      
                        disabled=True,
                        help="The assembled filter condtion from the GUI.",
                        key=ST_SS.FILTER_CONDITION_GUI_KEY)     

