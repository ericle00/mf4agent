import streamlit as st

from gui.keys.st_ss import ST_SS
from gui.layout.side_bar.mf4_setup_tab.file_selection import render_file_selection
from gui.layout.side_bar.mf4_setup_tab.signal_list import render_signal_list_display
from gui.layout.side_bar.mf4_setup_tab.display_filter_condition import render_display_filter_conditions
from gui.layout.side_bar.mf4_setup_tab.display_options import render_output_display_options

                         
def render_mf4_setup_tab(tab) -> None:
    """Render the setup tab."""
    with tab:
        render_file_selection()
        mf4_file_disabled = st.session_state.get(ST_SS.SELECTED_MF4_FILE_KEY) == "None"
        render_signal_list_display(mf4_file_disabled)
        render_display_filter_conditions(mf4_file_disabled)
        render_output_display_options(mf4_file_disabled)      
              










        



