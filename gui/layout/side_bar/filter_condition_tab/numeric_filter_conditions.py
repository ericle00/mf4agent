import streamlit as st

from gui.keys.st_ss import ST_SS

from gui.layout.side_bar.filter_condition_tab.utils import extract_pushed_btn_id

                                                                              
def render_numeric_filter_conditions(numeric_signals_info: dict[str, dict[list, str]], 
                                     mf4_file_disabled: bool) -> None:
    """
    Renders the numeric filter conditions section.

    Parameters:
        numeric_signals_info (dict[str, dict[list, str]]): A dictionary containing information about numeric signals.
        mf4_file_disabled (bool): A flag indicating whether the MF4 file is disabled.

    Returns:
        None
    """
    ### Constants
    NONE_STR = "None"
    FIRST_OPTION = NONE_STR
    
    SIGNAL_SELECT_BOX_KEY = ST_SS.FILTER_CONDITION_NUMERIC_SIGNAL_SELECT_BOX_KEY_PREFIX + "{number}"
    LOGICAL_SYMBOL_KEY = ST_SS.FILTER_CONDITION_NUMERIC_LOGICAL_SYMBOL_KEY_PREFIX + "{number}"
    SIGNAL_VALUE_KEY = ST_SS.FILTER_CONDITION_NUMERIC_SIGNAL_VALUE_KEY_PREFIX + "{number}"
    SIGNAL_VALUE_INTERVAL_KEY = ST_SS.FILTER_CONDITION_NUMERIC_SIGNAL_VALUE_INTERVAL_KEY_PREFIX + "{number}"
    DELETE_BTN_KEY = ST_SS.FILTER_CONDITION_NUMERIC_DELETE_BTN_KEY_PREFIX + "{number}"
    
    ### Options
    SIGNAL_NAME_LIST = sorted(list(numeric_signals_info.keys()), key=lambda x: x.lower())
    LOGICAL_OPTION_LIST = ["", '<', '>', '<=', '>=', '==']
    
    ### Session state
    st_ss = st.session_state
    
    if ST_SS.FILTER_CONDITION_NUMERIC_LIST_ORDER_KEY not in st_ss:
        st_ss[ST_SS.FILTER_CONDITION_NUMERIC_LIST_ORDER_KEY ] = [0]
    
    def add_new_numeric_fc():
        st_ss[ST_SS.FILTER_CONDITION_NUMERIC_LIST_ORDER_KEY ].append(st_ss[ST_SS.FILTER_CONDITION_N_UNIVERSAL_KEY])
        st_ss[ST_SS.FILTER_CONDITION_N_UNIVERSAL_KEY] += 1
        
    def remove_numeric_fc():
        deleted_btn_id = extract_pushed_btn_id(dictionary=st_ss, prefix=ST_SS.FILTER_CONDITION_NUMERIC_DELETE_BTN_KEY_PREFIX)
        del st_ss[SIGNAL_SELECT_BOX_KEY.format(number=deleted_btn_id)]
        del st_ss[LOGICAL_SYMBOL_KEY.format(number=deleted_btn_id)]
        del st_ss[SIGNAL_VALUE_KEY.format(number=deleted_btn_id)]
        del st_ss[SIGNAL_VALUE_INTERVAL_KEY.format(number=deleted_btn_id)]
        del st_ss[DELETE_BTN_KEY.format(number=deleted_btn_id)]
        st_ss[ST_SS.FILTER_CONDITION_NUMERIC_LIST_ORDER_KEY].remove(deleted_btn_id)


    ### Header
    st.header("Numerical #️⃣")
    
    # Multiselect
    st.multiselect(label="Available signal (s)",
                    options=SIGNAL_NAME_LIST,
                    disabled=mf4_file_disabled,
                    placeholder="Choose signal(s) from the list or by typing",
                    help="Select interested numeric based signals.",
                    key=ST_SS.FILTER_CONDITION_NUMERIC_SIGNALS_MULTISELECT_KEY)
    
    # Disabled of empty else enable 
    numeric_fc_signals_multiselect: list = st_ss.get(ST_SS.FILTER_CONDITION_NUMERIC_SIGNALS_MULTISELECT_KEY)
    disabled_multiselect = True if not numeric_fc_signals_multiselect else False
    
    with st.container(border=True):
        for id in st_ss[ST_SS.FILTER_CONDITION_NUMERIC_LIST_ORDER_KEY]:
            col1, col2, col3 = st.columns([4,1,1])
            # Signal select box
            with col1:
                st.selectbox(label="Numeric", 
                            options=[FIRST_OPTION] + numeric_fc_signals_multiselect, 
                            disabled=mf4_file_disabled or disabled_multiselect,
                            index=0, label_visibility="collapsed",
                            key=SIGNAL_SELECT_BOX_KEY.format(number=id),
                            )
            
            # Signal name and content extraction
            signal_name = st_ss[SIGNAL_SELECT_BOX_KEY.format(number=id)]
            signal_info_content = numeric_signals_info.get(signal_name)
            
            # Logical operations selectbox
            with col2:
                st.selectbox(label="Numeric", 
                            options=LOGICAL_OPTION_LIST, 
                            index=0, label_visibility="collapsed",
                            disabled=mf4_file_disabled or disabled_multiselect,
                            key=LOGICAL_SYMBOL_KEY.format(number=id))
            


            # Min max and unit extraction 
            if signal_name != NONE_STR:
                min_max = signal_info_content.get("possible_values")
                unit = signal_info_content.get("unit")
                
            else:
                min_max = [0, 10000]
                unit = "Not available"
                    
            # Input value and interval
            with col3:
                # Numeric input
                st.number_input(label="Numeric", label_visibility="collapsed",
                                disabled=mf4_file_disabled or disabled_multiselect, 
                                format="%0.1f", min_value=float(min_max[0]), 
                                max_value=float(min_max[1]), help="Units",
                                key=SIGNAL_VALUE_KEY.format(number=id))
                        

            col1, col2 = st.columns([5,1])
            with col1:
                ## Interval display 
                interval_unit_string = "None"
                if signal_name != FIRST_OPTION: 
                    interval_unit_string = f"{signal_name} ∈ {str(min_max)} {unit}"
                st.text_input(label="Numeric", label_visibility="collapsed",
                                key=SIGNAL_VALUE_INTERVAL_KEY.format(number=id),
                                value=interval_unit_string, disabled=True)
            with col2:
                # Delete row filter condition button
                st.button(label="❌", on_click=remove_numeric_fc, 
                        type="secondary", 
                        disabled=mf4_file_disabled or disabled_multiselect,
                        use_container_width=True,
                        help="Delete this filter condition row.",
                        key=DELETE_BTN_KEY.format(number=id))
        
        # Add new row button
        st.button(label="Add new numeric filter condition ➕", on_click=add_new_numeric_fc,
                disabled=mf4_file_disabled or disabled_multiselect,
                use_container_width=True,
                help="Insert a new filter condition row.",
                key=ST_SS.FILTER_CONDITION_NUMERIC_ADD_NEW_ROW_BTN_KEY)