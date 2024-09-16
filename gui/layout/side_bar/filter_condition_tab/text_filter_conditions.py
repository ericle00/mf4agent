import streamlit as st

from gui.keys.st_ss import ST_SS

from gui.layout.side_bar.filter_condition_tab.utils import extract_pushed_btn_id
                                                                                                                                                
                                                   
def render_text_filter_conditions(text_signals_info:dict[str, dict[list, str]], 
                                  mf4_file_disabled: bool) -> None:
    """
    Renders the text filter conditions section.

    Parameters:
    text_signals_info (dict[str, dict[list, str]]): A dictionary containing information about text signals.
    mf4_file_disabled (bool): A flag indicating whether the MF4 file is disabled.

    Returns:
    None
    """
    SIGNAL_SELECT_BOX_KEY = ST_SS.FILTER_CONDITION_TEXT_SELECT_BOX_KEY_PREFIX + "{number}"
    SIGNAL_OPTIONS_SELECT_BOX_KEY = ST_SS.FILTER_CONDITION_TEXT_SIGNAL_OPTIONS_SELECT_BOX_KEY_PREFIX  + "{number}"
    DELETE_BTN_KEY = ST_SS.FILTER_CONDITION_TEXT_DELETE_BTN_KEY_PREFIX + "{number}"
    
    NONE_STR = "None"
    FIRST_OPTION = NONE_STR
    signal_names_list = list(text_signals_info.keys())
    signal_names_list.remove(NONE_STR)
    SIGNAL_NAME_LIST = sorted(signal_names_list, key=lambda x: x.lower())
    
    ### TODO IMPLEMENT A STACK FOR THE SIGNAL OPTIONS
    ### Session state
    st_ss = st.session_state
    
    # Universal id number
    if ST_SS.FILTER_CONDITION_N_UNIVERSAL_KEY not in st_ss:
        st_ss[ST_SS.FILTER_CONDITION_N_UNIVERSAL_KEY] = 1
    
    if ST_SS.FILTER_CONDITION_TEXT_LIST_ORDER_KEY not in st_ss:
        st_ss[ST_SS.FILTER_CONDITION_TEXT_LIST_ORDER_KEY] = [0]
    
    
    def add_new_boolean_fc():
        st_ss[ST_SS.FILTER_CONDITION_TEXT_LIST_ORDER_KEY].append(st_ss[ST_SS.FILTER_CONDITION_N_UNIVERSAL_KEY])
        st_ss[ST_SS.FILTER_CONDITION_N_UNIVERSAL_KEY] += 1
         
    
    def remove_boolean_fc():
        deleted_btn_id = extract_pushed_btn_id(dictionary=st_ss, prefix=ST_SS.FILTER_CONDITION_TEXT_DELETE_BTN_KEY_PREFIX)
        del st_ss[SIGNAL_SELECT_BOX_KEY.format(number=deleted_btn_id)]
        del st_ss[DELETE_BTN_KEY.format(number=deleted_btn_id)]
        st_ss[ST_SS.FILTER_CONDITION_TEXT_LIST_ORDER_KEY].remove(deleted_btn_id)

    ### Header
    st.header("Text 🅰️")
    
    # Multiselect
    st.multiselect(label="Available signal(s)",
                    options=SIGNAL_NAME_LIST,
                    disabled=mf4_file_disabled,
                    placeholder="Choose signal(s) from the list or by typing",
                    help="Select interested text based signals.",
                    key=ST_SS.FILTER_CONDITION_TEXT_SIGNALS_MULTISELECT_KEY)
    
    # Disabled of empty else enable 
    text_fc_signals_multiselect: list = st_ss[ST_SS.FILTER_CONDITION_TEXT_SIGNALS_MULTISELECT_KEY]
    disabled_multiselect = True if not text_fc_signals_multiselect else False
        
    with st.container(border=True):
        for id in st_ss[ST_SS.FILTER_CONDITION_TEXT_LIST_ORDER_KEY]:
            col1, col2, col3 = st.columns([4,4,1])
            # Signal
            with col1:
                st.selectbox(label="Filter Condition", 
                            options=[FIRST_OPTION] + text_fc_signals_multiselect, 
                            index=0, label_visibility="collapsed",
                            disabled=mf4_file_disabled or disabled_multiselect,
                            help="Choose text signal.",
                            key=SIGNAL_SELECT_BOX_KEY.format(number=id),
                            )      
            
            signal_name = st_ss[SIGNAL_SELECT_BOX_KEY.format(number=id)]

            # Signal option
            with col2:
                signal_info_content = text_signals_info.get(signal_name)
                st.selectbox(label="Filter Condition", 
                            options=[FIRST_OPTION] + sorted(signal_info_content.get("possible_values")), 
                            index=0, label_visibility="collapsed",
                            disabled=mf4_file_disabled or disabled_multiselect,
                            help="Choose text signal value.",
                            key=SIGNAL_OPTIONS_SELECT_BOX_KEY.format(number=id),
                            )   
                
            # Delete row button
            with col3:
                st.button(label="❌", on_click=remove_boolean_fc, 
                        type="secondary", 
                        disabled=mf4_file_disabled or disabled_multiselect,
                        use_container_width=True,
                        help="Delete this filter condition row.",
                        key=DELETE_BTN_KEY.format(number=id))
        
        # Add new row button
        st.button(label="Add new text filter condition ➕", on_click=add_new_boolean_fc, 
                    disabled=mf4_file_disabled or disabled_multiselect,
                    type="secondary",
                    use_container_width=True,
                    help="Insert a new filter condition row.",
                    key=ST_SS.FILTER_CONDITION_TEXT_ADD_NEW_ROW_BTN_KEY)

    