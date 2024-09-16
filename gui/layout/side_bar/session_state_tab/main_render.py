import streamlit as st

from gui.keys.st_ss import ST_SS


def render_session_state_tab(tab) -> None:
    """Render the session state tab."""
    with tab:
        st.header("Session state key-values", divider="rainbow")
        
        if st.toggle("Show All Session Keys"):
            write_out_all_keys()
            
            
@st.cache_data(show_spinner="Writing session state ...")
def write_out_all_keys():
    st_ss = st.session_state
    output_text_keys = ["system_instruction"]
    hide_keys = [ST_SS.MF4_FILES_SIGNAL_MAP, 
                    # ST_SS.CHAT_HISTORY_KEY, 
                    ST_SS.CHAT_TEST_HISTORY_KEY]
    
    st_ss_sorted = dict(sorted(st_ss.items()))
    
    # Display session state keys and values
    for key, val in st_ss_sorted.items():
        # Hide some keys
        if key not in hide_keys:
            with st.container(border=True):
                if key in output_text_keys:
                    st.code(key, ": ")
                    with st.container(border=True):
                        st.text(val)
                else:
                    if isinstance(val, dict) or isinstance(val, list):
                        st.code(key, ":")
                        with st.container(border=True):
                            st.write(val)
                    else:
                        st.code(f"{key} : {val}")