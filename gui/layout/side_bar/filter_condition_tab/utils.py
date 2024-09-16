import re
import streamlit as st

from typing import Union

def extract_gui_filter_conditions() -> str:
    """
    Extracts the GUI filter conditions from the session state.

    Returns:
    str: The final filter condition string.
    """
    st_ss = st.session_state
    # Constants
    NONE_STR = "None"
    PREFIX_TYPE_LIST = ["default_fc_", "text_fc_", "numeric_fc_"]
    EXCLUSION_STRING = NONE_STR
    LOGICAL_OPERATOR_AND_VALUE_NAMES = ["logical_symbol_", "value_"]
    TEXT_FC_OPTIONS_NAME = "option_selectbox_"
    
    # List if select boxes and its values
    selectbox_value_pair = sorted([(key, st_ss[key]) for key in st_ss.keys() if any(prefix + "selectbox_" in key for prefix in PREFIX_TYPE_LIST)],  key=lambda x: x[0])
    
    # Initialize final filter condition list
    final_fc_list = []
    
    ### Loop through each fc selectbox
    for item_pair in selectbox_value_pair:
        ### Extract id and its value
        selectbox_id, selectbox_value = item_pair
        
        ### Only looking when not containing first option
        if selectbox_value != EXCLUSION_STRING:
            ### Initialise empty condition string
            filter_condition = ""
            ### Extract element id number
            id = extract_id_from_string(selectbox_id)
            
            ### Numeric FC we have to extract information 
            ### from logical operator and input values
            if PREFIX_TYPE_LIST[-1] in selectbox_id:
                
                logical_operator_selectbox_id = PREFIX_TYPE_LIST[-1] + LOGICAL_OPERATOR_AND_VALUE_NAMES[0] + id
                logical_operator = st_ss[logical_operator_selectbox_id] 
                
                value_selectbox_id = PREFIX_TYPE_LIST[-1] + LOGICAL_OPERATOR_AND_VALUE_NAMES[1] + id
                value = st_ss[value_selectbox_id] 
                
                # Check if we have everything for constructing the fc
                if logical_operator != EXCLUSION_STRING and logical_operator:
                    filter_condition = f"({selectbox_value} {logical_operator} {str(value)})"                 

            ### Text FC 
            elif PREFIX_TYPE_LIST[1] in selectbox_id:
                text_option_selectbox_id = PREFIX_TYPE_LIST[1] + TEXT_FC_OPTIONS_NAME + id
                text_option = st_ss[text_option_selectbox_id] 
                
                if text_option != EXCLUSION_STRING:
                    filter_condition = f"({selectbox_value}=={text_option})"                 
            
            ### Default FC
            elif PREFIX_TYPE_LIST[0] in selectbox_id:
                filter_condition = f"({selectbox_value})"
            
            ### Append only none empty conditions
            if filter_condition:
                final_fc_list.append(filter_condition)
            
    ### Init concat filter condition variable
    final_fc = ""  
    
    # Removing duplicates
    unique_fc_list = list(set(final_fc_list))
    len_list = len(unique_fc_list)      
    
    # If only one filter condition return the first element
    if len_list == 1:
        final_fc += unique_fc_list[0]
    else: 
        # Concat filter conditions
        for i, fc in enumerate(unique_fc_list):
            final_fc += f"{fc}" if i == len_list - 1 else f"{fc} & " 

    return final_fc
                                
                                           
def extract_pushed_btn_id(dictionary: dict, prefix: str) -> Union[int, None]:
    """
    Extracts the ID of the pushed button from the dictionary.

    Parameters:
    dictionary (dict): The dictionary containing the button states.
    prefix (str): The prefix of the button IDs.

    Returns:
    int: The ID of the pushed button, or None if no button was pushed.
    """
    dict_filtered = {key: value for key, value in dictionary.items() if key.startswith(prefix)}
    for key, value in dict_filtered.items():
        if value is True:
            return int(key.removeprefix(prefix))
    return None


def extract_id_from_string(input_string: str) -> Union[str, None]:
    """
    Extracts the ID from a given string.

    Parameters:
    input_string (str): The string from which to extract the ID.

    Returns:
    str: The extracted ID, or None if no ID was found.
    """
    numbers = re.findall(r'\d+', input_string)
    if numbers:
        return numbers[-1]
    else:
        return None