import streamlit as st                    
                                                             
from agent.prompts.planner_prompts import SYSTEM_INSTRUCTION_PLANNER
from agent.prompts.ci_prompts import SYSTEM_INSTRUCTION_CI_COMPUTATION, SYSTEM_INSTRUCTION_CI_PLOT
                                                                     

def init_system_instructions(st_ss) -> None:
    """
    Initialize system instructions in the Streamlit session state.

    Parameters:
    st_ss (st.session_state): The Streamlit session state.

    Returns:
    None
    """
    from gui.keys.st_ss import ST_SS
    
    if ST_SS.SYSTEM_INSTRUCTION_PLANNER_KEY not in st_ss:
        st_ss[ST_SS.SYSTEM_INSTRUCTION_PLANNER_KEY] = SYSTEM_INSTRUCTION_PLANNER
        st_ss[ST_SS.SYSTEM_INSTRUCTION_PLANNER_DEFAULT_KEY] = SYSTEM_INSTRUCTION_PLANNER
    
    if ST_SS.SYSTEM_INSTRUCTION_CI_COMPUTATION_KEY not in st_ss:
        st_ss[ST_SS.SYSTEM_INSTRUCTION_CI_COMPUTATION_KEY] = SYSTEM_INSTRUCTION_CI_COMPUTATION
        st_ss[ST_SS.SYSTEM_INSTRUCTION_CI_COMPUTATION_DEFAULT_KEY] = SYSTEM_INSTRUCTION_CI_COMPUTATION
    
    if ST_SS.SYSTEM_INSTRUCTION_CI_PLOT_KEY not in st_ss:
        st_ss[ST_SS.SYSTEM_INSTRUCTION_CI_PLOT_KEY] = SYSTEM_INSTRUCTION_CI_PLOT        
        st_ss[ST_SS.SYSTEM_INSTRUCTION_CI_PLOT_DEFAULT_KEY] = SYSTEM_INSTRUCTION_CI_PLOT