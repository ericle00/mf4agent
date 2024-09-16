from gui.keys.st_ss import ST_SS
                                                                                                                                                                                                                             
def default_output_display_toggles(st_ss) -> None:
    """
    Set default toggles for output display in the Streamlit session state.

    Parameters:
    st_ss (st.session_state): The Streamlit session state.

    Returns:
    None
    """
    if st_ss[ST_SS.DEVELOPER_LOGGED_IN_KEY]:
        ### Default show plan toggle        
        if ST_SS.TOGGLE_SHOW_PLAN_KEY not in st_ss:
            st_ss[ST_SS.TOGGLE_SHOW_PLAN_KEY] = True
            
        ### Default show code toggle        
        if ST_SS.TOGGLE_SHOW_CODE_KEY not in st_ss:
            st_ss[ST_SS.TOGGLE_SHOW_CODE_KEY] = True
        
        ### Default run code toggle        
        if ST_SS.TOGGLE_RUN_CODE_KEY not in st_ss:
            st_ss[ST_SS.TOGGLE_RUN_CODE_KEY] = True
        
        ### Default show file source toggle
        if ST_SS.TOGGLE_SHOW_FILE_SOURCE not in st_ss:
            st_ss[ST_SS.TOGGLE_SHOW_FILE_SOURCE] = True
            
    else:  
        ### Default show plan toggle        
        if ST_SS.TOGGLE_SHOW_PLAN_KEY not in st_ss:
            st_ss[ST_SS.TOGGLE_SHOW_PLAN_KEY] = True
            
        ### Default show code toggle        
        if ST_SS.TOGGLE_SHOW_CODE_KEY not in st_ss:
            st_ss[ST_SS.TOGGLE_SHOW_CODE_KEY] = True
        
        ### Default run code toggle        
        if ST_SS.TOGGLE_RUN_CODE_KEY not in st_ss:
            st_ss[ST_SS.TOGGLE_RUN_CODE_KEY] = True
        
        ### Default show file source toggle
        if ST_SS.TOGGLE_SHOW_FILE_SOURCE not in st_ss:
            st_ss[ST_SS.TOGGLE_SHOW_FILE_SOURCE] = True