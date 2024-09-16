from gui.keys.st_ss import ST_SS
                
from volvo_dev.llms.delegate_decoder import DelegateDecoder
from volvo_dev.llms.delegate_encoder import DelegateEncoder

def read_models(st_ss) -> None:
    """
    Read decoder models configuration from YAML file.

    Parameters:
    st_ss (dict): The Streamlit session state.

    Returns:
    None
    """
    
    # Extract decoders and encoders
    st_ss[ST_SS.DECODER_MODELS_KEY] = DelegateDecoder.DECODER_MODEL_LIST
    st_ss[ST_SS.ENCODER_MODELS_KEY] = DelegateEncoder.ENCODER_MODELS