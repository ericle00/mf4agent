import streamlit as st

from typing import Union
from datetime import datetime

from volvo_dev.llms.delegate_decoder import DelegateDecoder

from gui.keys.st_ss import ST_SS


def init_decoder_and_time_status(st_ss):
    st_ss[ST_SS.DECODER_MODELS_STATUS] = check_decoder_status()
    st_ss[ST_SS.LATEST_REFRESH_DECODERS_STATUS_TIME] = get_current_time()

    
def check_decoder_status() -> dict:
    st_ss = st.session_state

    def check_decoder_status(model: str) -> Union[bool, str]:
        decoder_o = DelegateDecoder(model)
        
        try:
            decoder_o.generate(inputs="Check Status Message!", max_tokens=10)
            return True, ""  # Indicate success and no error message
        except Exception as e:
            return False, str(e)  # Indicate failure and return the error message
    
    model_status = {}
    for model in st_ss[ST_SS.DECODER_MODELS_KEY]:
        available, error_message = check_decoder_status(model)
        icon = "✅" if available else "⛔"
        text = "Available" if available else "Not available"
        
        temp_dict = {}
        temp_dict["text"] =  f"[{text}] {icon}"
        temp_dict["available"] = available
        temp_dict["error_message"] = error_message
        temp_dict["icon"] = icon
        
        model_status[model] = temp_dict
        
    return model_status

def get_current_time() -> str:
    return datetime.today().strftime('%Y-%m-%d %H:%M:%S')