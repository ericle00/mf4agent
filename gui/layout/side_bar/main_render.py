import streamlit as st  

from gui.layout.side_bar.mf4_setup_tab.main_render import render_mf4_setup_tab
from gui.layout.side_bar.filter_condition_tab.main_render import render_filter_condition_setup_tab

from gui.layout.side_bar.model_availability_tab.main_render import render_model_availability_tab
from gui.layout.side_bar.planner_tab.planner import render_system_instruction_planner_tab
from gui.layout.side_bar.code_interpreter_tab.code_interpreter import render_code_interpreter_tab

from gui.layout.side_bar.session_state_tab.main_render import render_session_state_tab

from gui.keys.st_ss import ST_SS
    
 
def render() -> None:
    """Render the sidebar with tabs for model settings and session state."""
    st_ss = st.session_state

    with st.sidebar:
        render_restart_button()

        if st_ss[ST_SS.DEVELOPER_LOGGED_IN_KEY]:
            tab_names = ["Setup", "Filter Condition", "Model Availability", "Planner", "CI", "Session State"]
        else:
            tab_names = ["Setup", "Filter Condition", "Model Availability", "Planner", "CI"]

        tabs = st.tabs(tab_names)

        for i, tab in enumerate(tabs):
            if tab_names[i] == "Setup":
                render_mf4_setup_tab(tab)
            elif tab_names[i] == "Filter Condition":
                render_filter_condition_setup_tab(tab)
            elif tab_names[i] == "Model Availability":
                render_model_availability_tab(tab)
            elif tab_names[i] == "Planner":
                render_system_instruction_planner_tab(tab)
            elif tab_names[i] == "CI":
                render_code_interpreter_tab(tab)
            elif tab_names[i] == "Session State":
                render_session_state_tab(tab)       
    

def render_restart_button():    
    # Stop button
    def clear_cache():
        pass
        
    st.button(label="Stop AI Inference ⏹️✨", help="Click to stop ongoing AI inferencing",
            disabled=False,
            use_container_width=True,
            type="secondary",
            on_click=clear_cache)


