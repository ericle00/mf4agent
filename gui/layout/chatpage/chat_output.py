import json
import streamlit as st


from gui.styles.chatpage_headers import ChatPageHeader
from gui.keys.st_ss import ST_SS
from utils.markdown import MD

from utils.agent_output import remove_warnings, insert_source_to_image, insert_source_to_text
from utils.text_string import extract_and_join_python_blocks
    
    
def output_llm_content(llm_output_serialized: str) -> None:
    """
    Display LLM output content, including plan, code, and output, with optional toggles for refined plan, code, and file source.
    
    Parameters:
    llm_output_serialized (str): Serialized LLM output
    """
    # Store session state
    st_ss = st.session_state
    
    # Deserialize content 
    plan_serialized, code_generated, code_output_text, code_output_image_list = json.loads(llm_output_serialized)
    if  st_ss[ST_SS.TOGGLE_SHOW_PLAN_KEY] and plan_serialized:
        gui_input, plan_initial_generic = json.loads(plan_serialized)
        
        # GUI input
        st.markdown(ChatPageHeader.GUI_INPUT)
        st.code(gui_input, language=None)
        
        # Generic plan
        st.markdown(ChatPageHeader.GENERIC_PLAN)
        st.code(plan_initial_generic, language=None)
        
    # Show code
    if st_ss[ST_SS.TOGGLE_SHOW_CODE_KEY] and code_generated:
        st.markdown(ChatPageHeader.GENERATED_CODE)
        st.code(extract_and_join_python_blocks(code_generated), line_numbers=True)
    
    # Run code
    if st_ss[ST_SS.TOGGLE_RUN_CODE_KEY]:
        mf4_source = st_ss.get(ST_SS.SELECTED_MF4_FILE_KEY)
        if code_output_text or code_output_image_list:
            st.markdown(ChatPageHeader.EXECUTED_CODE)    
            if remove_warnings(code_output_text):
                code_output_text = remove_warnings(code_output_text)
                # MF4 Source text
                if st_ss.get(ST_SS.TOGGLE_SHOW_FILE_SOURCE):
                    code_output_text = insert_source_to_text(code_output_text, mf4_source)
                st.code(code_output_text, language=None)
            if code_output_image_list:
                for image_path in code_output_image_list:
                    # MF4 Source image
                    if st_ss.get(ST_SS.TOGGLE_SHOW_FILE_SOURCE):
                        image_path = insert_source_to_image(image_path, mf4_source)
                    st.image(image_path)