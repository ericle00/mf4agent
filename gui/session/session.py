import os 
import streamlit as st

from datetime import datetime
from gui.keys.st_ss import ST_SS

from gui.session.read_llm_models import read_models
from gui.session.read_mf4_data_folder import init_mf4_folder_and_time
from gui.session.check_decoder_status import init_decoder_and_time_status
from gui.session.initial_filter_conditions import init_filter_conditions
from gui.session.default_toggles import default_output_display_toggles
from gui.session.init_default_system_instructions import init_system_instructions


# .88b  d88.  .d8b.  d888888b d8b   db      d8888b. d88888b d8b   db d8888b. d88888b d8888b. 
# 88'YbdP`88 d8' `8b   `88'   888o  88      88  `8D 88'     888o  88 88  `8D 88'     88  `8D 
# 88  88  88 88ooo88    88    88V8o 88      88oobY' 88ooooo 88V8o 88 88   88 88ooooo 88oobY' 
# 88  88  88 88~~~88    88    88 V8o88      88`8b   88~~~~~ 88 V8o88 88   88 88~~~~~ 88`8b   
# 88  88  88 88   88   .88.   88  V888      88 `88. 88.     88  V888 88  .8D 88.     88 `88. 
# YP  YP  YP YP   YP Y888888P VP   V8P      88   YD Y88888P VP   V8P Y8888D' Y88888P 88   YD 
                                                                                           
                                                                                           

def render() -> None:
    """
    Main function to render the Streamlit gui.
    """
    st_ss = st.session_state
    
    # Session start config
    if not st_ss[ST_SS.SESSION_RENDER_FIRST_TIME_KEY]:  
        # Home Path
        st_ss[ST_SS.PATH_HOME] = os.getenv("HOME")
        
        st_ss[ST_SS.LATEST_REFRESH_FILES_TIME] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        
        # Decoders: Read decoder models config and generation config 
        read_models(st_ss)
        
        # User folder and files
        init_mf4_folder_and_time(st_ss)
        
        # Decoder status
        init_decoder_and_time_status(st_ss)
        
        # Init filter condition
        init_filter_conditions(st_ss)
        
        # Toggles
        default_output_display_toggles(st_ss)
        
        # Init CI system instruction
        init_system_instructions(st_ss)
        
        # Set to True
        st.session_state[ST_SS.SESSION_RENDER_FIRST_TIME_KEY] = True

        

