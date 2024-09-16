import streamlit as st

from gui.keys.st_ss import ST_SS
from gui.layout.side_bar.filter_condition_tab.default_filter_conditions import render_default_filter_condition                  
from gui.layout.side_bar.filter_condition_tab.text_filter_conditions import render_text_filter_conditions
from gui.layout.side_bar.filter_condition_tab.numeric_filter_conditions import render_numeric_filter_conditions
from gui.layout.side_bar.filter_condition_tab.display_filter_conditions import render_display_filter_conditions

                                                                                                                                                                                                 
def render_filter_condition_setup_tab(tab: st.tabs) -> None:
    """
    Renders the filter condition setup tab.

    Parameters:
    tab (st.tabs): The Streamlit tab object.

    Returns:
    None
    """
    st_ss = st.session_state
    
    NONE_STR = "None"
    
    # Check if selected mf4 file
    filename_key = st_ss[ST_SS.SELECTED_MF4_FILE_KEY]
    mf4_file_disabled = filename_key == NONE_STR
    
    with tab:
        ### Extract text and numeric values
        
        numeric_signals_info = {NONE_STR: {"possible_values": ["",""], "unit": "Not available"}}
        text_signals_info = {NONE_STR: {"possible_values":[], "unit": "Not available"}}
        
        if filename_key != NONE_STR:
            ### Separate
            mf4_files_signal_map: dict[str, dict] = st_ss[ST_SS.MF4_FILES_SIGNAL_MAP]
            signals_info = mf4_files_signal_map.get(filename_key)
            
            numeric_signals_info.update(signals_info.get(ST_SS.NUMERIC_SIGNALS_INFO_KEY))
            text_signals_info.update(signals_info.get(ST_SS.TEXT_SIGNALS_INFO_KEY))
        
        render_default_filter_condition()
        render_text_filter_conditions(text_signals_info, mf4_file_disabled)
        render_numeric_filter_conditions(numeric_signals_info, mf4_file_disabled)
        render_display_filter_conditions()
        














