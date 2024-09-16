import streamlit as st

from volvo_dev.llms.delegate_decoder import DelegateDecoder
from gui.session.check_decoder_status import check_decoder_status, get_current_time

from gui.keys.st_ss import ST_SS


def render_model_availability_tab(tab) -> None:
    st_ss = st.session_state
    
    with tab:
        st.subheader("Model Availability ✅⛔")
    
        with st.container(border=True):
            st.markdown(":gray[List of the models availability]")
            
            write_out_decoder_availability()
            
            def refresh_decoder_status():
                st_ss[ST_SS.DECODER_MODELS_STATUS] = check_decoder_status()
                st_ss[ST_SS.LATEST_REFRESH_DECODERS_STATUS_TIME] = get_current_time()
            
            latest_update = st_ss[ST_SS.LATEST_REFRESH_DECODERS_STATUS_TIME]
            
            st.button(
                label=f"🔄 Refresh status, [Last update: {latest_update} UTC]", 
                type="primary", 
                use_container_width=True,
                on_click=refresh_decoder_status)
            
def write_out_decoder_availability() -> None:
    st_ss = st.session_state
    decoder_model_status = st_ss[ST_SS.DECODER_MODELS_STATUS]
    
    for model, content in decoder_model_status.items(): 
        #text = content.get("text", "")
        error_message = content.get("error_message", "")
        #available = content.get("available", False)
        icon = content.get("icon", "⛔")
        
        col1, col2 = st.columns([1,1])
        with col1:
            with st.expander(label=f"**{model}**:"):
                st.markdown(f"**{model}**:")
        with col2:
            with st.expander(label=f"{icon}"):
                if error_message:
                    st.markdown(f":red[**Error:**]&nbsp; {error_message}")
                else:
                    st.markdown(":green[**Success:**]&nbsp; Available for use!")


def check_available_index(decoder_models_status: dict[dict]) -> int:
    "Check for default model if available else return the next available"
    default_model = DelegateDecoder.LLAMA_31_70B
    found_default = False

    for i, (model, content) in enumerate(decoder_models_status.items()):
        if model == default_model:
            found_default = True
        
        if found_default and content.get("available"):
            return i

    raise ValueError("No available index found after the default model")