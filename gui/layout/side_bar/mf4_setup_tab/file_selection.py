import os
import glob
from pathlib import Path
import streamlit as st
import yaml
from datetime import datetime

from gui.session.read_mf4_data_folder import get_current_time

from gui.keys.st_ss import ST_SS
                                                                                                                                                                                                                        
def render_file_selection() -> None:
    """
    Renders the file selection section.

    Returns:
    None
    """
    # File Selection  
    st_ss = st.session_state 
    st.subheader("File Selection 📑")
    
    with st.container(border=True):
        folder_selection(st_ss)
        init_mf4_file_paths_map(st_ss)
        init_mf4_info_file_paths_map(st_ss)
        file_selection(st_ss)
        update_files_read_button(st_ss)
    
    

def folder_selection(st_ss: dict):
    folders = read_folders_in_mf4_data(st_ss)
    
    st.selectbox(label="Folder", 
                 options=folders,
                 help="Folders within the MF4_APP folder",
                 key=ST_SS.SELECTED_MF4_FOLDER)
    
    
    

def read_folders_in_mf4_data(st_ss: dict):
    directory_path =  Path(st_ss[ST_SS.PATH_MF4_DATA_FOLDER])
    return [item.name for item in directory_path.iterdir() if item.is_dir()]
   
                                                                                                                                                                                   
def init_mf4_file_paths_map(_st_ss: dict) -> None:
    """
    Initialize a map of MF4 file paths.

    Parameters:
    st_ss (dict): The Streamlit session state.

    Returns:
    None
    """
    # Get paths of all MF4 files in the specified user folder
    mf4_files_pattern = os.path.join(_st_ss[ST_SS.PATH_MF4_DATA_FOLDER], 
                                     _st_ss[ST_SS.SELECTED_MF4_FOLDER],
                                     "*.mf4")
    mf4_filepaths = glob.glob(mf4_files_pattern)
    
    # Extract filenames from the paths
    mf4_filenames = [os.path.basename(mf4_filename) for mf4_filename in mf4_filepaths]     
    
    # Create a dictionary mapping MF4 filenames to their respective paths and store it in the shared state
    _st_ss[ST_SS.MF4_FILES_PATH_MAP_KEY] = {key: value for key, value in zip(mf4_filenames, mf4_filepaths)}
    
    
    
def init_mf4_info_file_paths_map(_st_ss: dict) -> None:
    """
    Initialize a map of MF4 info file paths.

    Parameters:
    st_ss (dict): The Streamlit session state.

    Returns:
    None
    """
    # Construct the pattern to search for MF4 info files within the user folder
    mf4_info_files_pattern = os.path.join(_st_ss[ST_SS.PATH_MF4_DATA_FOLDER], 
                                          _st_ss[ST_SS.SELECTED_MF4_FOLDER],  
                                          "*.yaml")
    mf4_info_filepaths = glob.glob(mf4_info_files_pattern)    
    
    # Extract just the filenames from the filepaths
    mf4_info_filenames = [os.path.basename(mf4_info_filename) for mf4_info_filename in mf4_info_filepaths]
    
    # Create a dictionary mapping filenames to their full filepaths
    _st_ss[ST_SS.MF4_INFO_FILES_PATH_MAP_KEY] = {key: value for key, value in zip(mf4_info_filenames, mf4_info_filepaths)}
    


        
def file_selection(st_ss: dict):
    
    def extract_signal_names_and_possible_values():
        # Initialize mf4 files signal map
        if ST_SS.MF4_FILES_SIGNAL_MAP not in st_ss:
            st_ss[ST_SS.MF4_FILES_SIGNAL_MAP] = {}
            
        # If it is not in map and the selected mf4 not None
        filename_key = st_ss.get(ST_SS.SELECTED_MF4_FILE_KEY)
        mf4_files_signal_map = st_ss.get(ST_SS.MF4_FILES_SIGNAL_MAP)
        
        if filename_key != "None":
            filename_key_with_yaml_extension = filename_key.split(".")[0] + ".yaml"
            mf4_info_yaml_path = st_ss[ST_SS.MF4_INFO_FILES_PATH_MAP_KEY].get(filename_key_with_yaml_extension, "")
             
            if not mf4_info_yaml_path:
                st.error(f"🚨 No corresponding YAML file could be found for {filename_key}. Please add its corresponding YAML file!")
                mf4_files_signal_map[filename_key] = {"numeric_signals_info":  {"Empty Numeric Signal": {"possible_values": "empty", "unit": "empty"}},
                                                      "text_signals_info":  {"Empty Text Signal": {"possible_values": "empty", "unit": "empty"}}}
            else:
                if filename_key not in mf4_files_signal_map:
                    with open(mf4_info_yaml_path, "r") as file:
                        mf4_files_signal_map[filename_key] = yaml.safe_load(file)  

                        
    st.selectbox(label="MF4 Files to select",
                    options=["None"] + [item for item in st_ss[ST_SS.MF4_FILES_PATH_MAP_KEY]],
                    on_change=extract_signal_names_and_possible_values,
                    index=0,
                    help="MF4 to analyze. Must select a file to enable the GUI.",
                    key=ST_SS.SELECTED_MF4_FILE_KEY)
        
        
def update_files_read_button(st_ss: dict):
    def refresh():
        read_folders_in_mf4_data(st_ss)
        init_mf4_file_paths_map(st_ss)
        init_mf4_info_file_paths_map(st_ss)
        st_ss[ST_SS.LATEST_REFRESH_FILES_TIME] = get_current_time()
        
        
    latest_updated = st_ss[ST_SS.LATEST_REFRESH_FILES_TIME]
    st.button(label=f"🔄 Refresh Files [Last update: {latest_updated} UTC]", 
              on_click=refresh,
              use_container_width=True)