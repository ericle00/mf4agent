import streamlit as st
from gui.keys.st_ss import ST_SS
                                                                                                                                              
def render_signal_list_display(mf4_file_disabled:bool) -> None:
    """
    Renders the signal list display section.

    Parameters:
    mf4_file_disabled (bool): A flag indicating whether the MF4 file is disabled.

    Returns:
    None
    """
    # List of signals of current MF4 file ###
    st_ss = st.session_state
    st.subheader("Signals 🆔👓")

    with st.container(border=True):
        signal_list_container(st_ss, mf4_file_disabled)
    
    
def signal_list_container(st_ss, mf4_file_disabled):
    st_ss = st.session_state

    # Get file path
    filename_key = st_ss.get(ST_SS.SELECTED_MF4_FILE_KEY)
    signal_option_list = ["None"]
    combined_mf4_file_signal_map = {}
    
    if filename_key != "None":
        # Load map
        mf4_file_signal_map = st_ss[ST_SS.MF4_FILES_SIGNAL_MAP].get(filename_key)
        
        # Combine numeric and text
        combined_signal_names_list = []
        for key in mf4_file_signal_map.keys():
            combined_mf4_file_signal_map.update(mf4_file_signal_map.get(key))
            combined_signal_names_list += list(mf4_file_signal_map.get(key).keys())

        # Sort in alphabetical order
        signal_option_list = sorted(combined_signal_names_list,
                                 key=lambda x: x.lower())


    # Multiselect options
    st.multiselect(label="Available signal (s)",
                    options=signal_option_list,
                    disabled=mf4_file_disabled,
                    placeholder="Choose signal(s) from the list or by typing",
                    help="Select signals to work with. Signal(s) info will be display below.",
                    key=ST_SS.DISPLAY_SIGNALS_MULTISELECT)
    
    signal_names_display = ""
    signal_possible_values_display = ""
    in_interval_display = ""
    
    if combined_mf4_file_signal_map:
        display_signals_multiselect = st_ss.get(ST_SS.DISPLAY_SIGNALS_MULTISELECT)
        
        if display_signals_multiselect:            
            for signal_name in display_signals_multiselect:
                signal_info_content = combined_mf4_file_signal_map.get(signal_name)
                signal_possible_values = signal_info_content.get("possible_values")
                
                if all(isinstance(item, str) for item in signal_possible_values):
                    signal_possible_values_display += f"{signal_possible_values}\n"
                else:
                    unit = signal_info_content.get("unit")
                    signal_possible_values_display += f"[{str(signal_possible_values[0])}, {str(signal_possible_values[1])}] {unit}\n"
                
                in_interval_display += "∈\n"
                signal_names_display += f"{signal_name}\n"
            
    # Text area
    with st.container(border=True):
        col1, col2, col3= st.columns([8,1,4])
        with col1:
            st.text(signal_names_display)
        with col2:
            st.text(in_interval_display)
        with col3: 
            st.text(signal_possible_values_display)