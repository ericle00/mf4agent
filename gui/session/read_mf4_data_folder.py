import os
from datetime import datetime

from gui.keys.st_ss import ST_SS


def init_mf4_folder_and_time(st_ss: dict):
    st_ss[ST_SS.PATH_MF4_DATA_FOLDER] = init_mf4_data_path()
    st_ss[ST_SS.LATEST_REFRESH_DECODERS_STATUS_TIME] = get_current_time()

                                                                                                                               
def init_mf4_data_path() -> str:
    """
    Initialize user folders and files.

    Parameters:
    st_ss (dict): The Streamlit session state.

    Returns:
    None
    """
    # Home path    
    mf4_data_folder_path = os.path.join("/mnt/nfs/gtt-pe-fcev-da/MF4_APP")
        
    # Init keys
    
    if not os.path.exists(mf4_data_folder_path):
        os.mkdir(mf4_data_folder_path)
        
    return mf4_data_folder_path


def get_current_time() -> str:
    return datetime.today().strftime('%Y-%m-%d %H:%M:%S')