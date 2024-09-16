import streamlit as st
from gui.keys.st_ss import ST_SS
                                               
from gui.layout.side_bar.filter_condition_tab.utils import extract_gui_filter_conditions
                                  
                                                                                         
def render_display_filter_conditions(mf4_file_disabled: bool) -> None:
    """
    Renders the display filter conditions section.

    Parameters:
    mf4_file_disabled (bool): A flag indicating whether the MF4 file is disabled.

    Returns:
    None
    """
    st_ss = st.session_state
    
    st.subheader("Filter Conditions 🆗")

    with st.container(border=True):

        st.text_area(label="Your filter condition(s)",
                        disabled=mf4_file_disabled,
                        help="E.g. (WheelBasedVehicleSpeed>60). CTRL + Enter to apply.",
                        key=ST_SS.FILTER_CONDITION_USER_KEY)
        
        user_input_filter_condition = st_ss.get(ST_SS.FILTER_CONDITION_USER_KEY)
        gui_filter_condition = extract_gui_filter_conditions()        
        
        if gui_filter_condition and user_input_filter_condition:
            final_filter_condition = f"{gui_filter_condition} & {user_input_filter_condition}"
        else:
            if user_input_filter_condition:
                final_filter_condition = user_input_filter_condition
            elif gui_filter_condition: 
                final_filter_condition = gui_filter_condition
            else:
                final_filter_condition = ""

        st.text_area(label="Final filter condition(s): (Yours + GUI)",
                    disabled=True,
                    value=final_filter_condition,
                    help="Final composed filter condition input to the agent.",
                    key=ST_SS.FILTER_CONDITION_FINAL_KEY)