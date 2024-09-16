"""Stores unique keys for Streamlit components in the session state, enabling efficient tracking and management of component instances."""

class ST_SS:

    # d8888b.  .d8b.  d888888b db   db .d8888. 
    # 88  `8D d8' `8b `~~88~~' 88   88 88'  YP 
    # 88oodD' 88ooo88    88    88ooo88 `8bo.   
    # 88~~~   88~~~88    88    88~~~88   `Y8b. 
    # 88      88   88    88    88   88 db   8D 
    # 88      YP   YP    YP    YP   YP `8888Y' 
                                                        

    PATH_WORKING_FOLDER_KEY = "path_working_folder"
    PATH_HOME = "path_home"
    PATH_MF4_DATA_FOLDER = "path_mf4_data"
    
    LATEST_REFRESH_FILES_TIME = "latest_refresh_files_time"
    LATEST_REFRESH_DECODERS_STATUS_TIME = "latest_refresh_decoders_status_time"
    
    # .88b  d88.  .d8b.  d8888b. .d8888. 
    # 88'YbdP`88 d8' `8b 88  `8D 88'  YP 
    # 88  88  88 88ooo88 88oodD' `8bo.   
    # 88  88  88 88~~~88 88~~~     `Y8b. 
    # 88  88  88 88   88 88      db   8D 
    # YP  YP  YP YP   YP 88      `8888Y' 
                                            

    MF4_FILES_PATH_MAP_KEY = "mf4_files_path_map"
    MF4_INFO_FILES_PATH_MAP_KEY = "mf4_info_files_path_map"
    MF4_FILES_SIGNAL_MAP = "mf4_files_signal_map"
    
    SELECTED_MF4_FOLDER = "selected_mf4_folder"
    SELECTED_MF4_FILE_KEY = "selected_mf4_file"
    SELECTED_PLANNER_KEY = "selected_planner"
    SELECTED_CODE_INTERPRETER_KEY = "selected_code_interpreter"
    
    NUMERIC_SIGNALS_INFO_KEY = "numeric_signals_info"
    TEXT_SIGNALS_INFO_KEY = "text_signals_info"
    

    # .d8888. d88888b .d8888. .d8888. d888888b  .d88b.  d8b   db 
    # 88'  YP 88'     88'  YP 88'  YP   `88'   .8P  Y8. 888o  88 
    # `8bo.   88ooooo `8bo.   `8bo.      88    88    88 88V8o 88 
    #   `Y8b. 88~~~~~   `Y8b.   `Y8b.    88    88    88 88 V8o88 
    # db   8D 88.     db   8D db   8D   .88.   `8b  d8' 88  V888 
    # `8888Y' Y88888P `8888Y' `8888Y' Y888888P  `Y88P'  VP   V8P 
                                                                                                     

    DEVELOPER_LOGGED_IN_KEY = "developer_logged_in"
    SESSION_RENDER_FIRST_TIME_KEY = "render_session_first_time"
    

    # db    db db      db      .88b  d88.       .o88b.  .d88b.  d8b   db d88888b d888888b  d888b  
    # 88    88 88      88      88'YbdP`88      d8P  Y8 .8P  Y8. 888o  88 88'       `88'   88' Y8b 
    # Y8    8P 88      88      88  88  88      8P      88    88 88V8o 88 88ooo      88    88      
    # `8b  d8' 88      88      88  88  88      8b      88    88 88 V8o88 88~~~      88    88  ooo 
    #  `8bd8'  88booo. 88booo. 88  88  88      Y8b  d8 `8b  d8' 88  V888 88        .88.   88. ~8~ 
    #    YP    Y88888P Y88888P YP  YP  YP       `Y88P'  `Y88P'  VP   V8P YP      Y888888P  Y888P  
                                                                                            
                                                                                            
    DECODER_MODELS_KEY = "decoder_models"
    ENCODER_MODELS_KEY = "encoder_models"
    
    IPYTHON_INTERPRETER_ACTION_KEY = "ipython_interpreter_action"
    DECODER_MODELS_STATUS = "decoder_model_status"
    
    
    #  d888b  d88888b d8b   db d88888b d8888b.  .d8b.  d888888b d888888b  .d88b.  d8b   db       .o88b.  .d88b.  d8b   db d88888b d888888b  d888b  
    # 88' Y8b 88'     888o  88 88'     88  `8D d8' `8b `~~88~~'   `88'   .8P  Y8. 888o  88      d8P  Y8 .8P  Y8. 888o  88 88'       `88'   88' Y8b 
    # 88      88ooooo 88V8o 88 88ooooo 88oobY' 88ooo88    88       88    88    88 88V8o 88      8P      88    88 88V8o 88 88ooo      88    88      
    # 88  ooo 88~~~~~ 88 V8o88 88~~~~~ 88`8b   88~~~88    88       88    88    88 88 V8o88      8b      88    88 88 V8o88 88~~~      88    88  ooo 
    # 88. ~8~ 88.     88  V888 88.     88 `88. 88   88    88      .88.   `8b  d8' 88  V888      Y8b  d8 `8b  d8' 88  V888 88        .88.   88. ~8~ 
    #  Y888P  Y88888P VP   V8P Y88888P 88   YD YP   YP    YP    Y888888P  `Y88P'  VP   V8P       `Y88P'  `Y88P'  VP   V8P YP      Y888888P  Y888P                                                                                                                                  

    PLANNER_MAX_TOKENS_KEY = "planner_max_tokens"
    PLANNER_TEMPERATURE_KEY = "planner_temperature"
    PLANNER_TOP_P_KEY = "planner_top_p"
    PLANNER_TOP_K_KEY = "planner_top_k"
    
    CI_MAX_TOKENS_KEY = "ci_max_tokens"
    CI_TEMPERATURE_KEY = "ci_temperature"
    CI_TOP_P_KEY = "ci_top_p"
    CI_GENERATION_CONFIG_TOP_K_KEY = "ci_top_k"
    
    #  .o88b. db   db  .d8b.  d888888b      db   db d888888b .d8888. d888888b  .d88b.  d8888b. db    db 
    # d8P  Y8 88   88 d8' `8b `~~88~~'      88   88   `88'   88'  YP `~~88~~' .8P  Y8. 88  `8D `8b  d8' 
    # 8P      88ooo88 88ooo88    88         88ooo88    88    `8bo.      88    88    88 88oobY'  `8bd8'  
    # 8b      88~~~88 88~~~88    88         88~~~88    88      `Y8b.    88    88    88 88`8b      88    
    # Y8b  d8 88   88 88   88    88         88   88   .88.   db   8D    88    `8b  d8' 88 `88.    88    
    #  `Y88P' YP   YP YP   YP    YP         YP   YP Y888888P `8888Y'    YP     `Y88P'  88   YD    YP    
    
    CHAT_HISTORY_KEY = "chat_history"
                                                                                                  
    # d888888b  .d88b.   d888b   d888b  db      d88888b .d8888. 
    # `~~88~~' .8P  Y8. 88' Y8b 88' Y8b 88      88'     88'  YP 
    #    88    88    88 88      88      88      88ooooo `8bo.   
    #    88    88    88 88  ooo 88  ooo 88      88~~~~~   `Y8b. 
    #    88    `8b  d8' 88. ~8~ 88. ~8~ 88booo. 88.     db   8D 
    #    YP     `Y88P'   Y888P   Y888P  Y88888P Y88888P `8888Y' 
                                                          
                                                        
    TOGGLE_SHOW_PLAN_KEY = "toggle_show_plan"
    TOGGLE_SHOW_CODE_KEY = "toggle_show_code"
    TOGGLE_RUN_CODE_KEY = "toggle_run_code"
    TOGGLE_SHOW_FILE_SOURCE = "toggle_show_file_source"

    # .88b  d88. db    db db      d888888b d888888b .d8888. d88888b db      d88888b  .o88b. d888888b 
    # 88'YbdP`88 88    88 88      `~~88~~'   `88'   88'  YP 88'     88      88'     d8P  Y8 `~~88~~' 
    # 88  88  88 88    88 88         88       88    `8bo.   88ooooo 88      88ooooo 8P         88    
    # 88  88  88 88    88 88         88       88      `Y8b. 88~~~~~ 88      88~~~~~ 8b         88    
    # 88  88  88 88b  d88 88booo.    88      .88.   db   8D 88.     88booo. 88.     Y8b  d8    88    
    # YP  YP  YP ~Y8888P' Y88888P    YP    Y888888P `8888Y' Y88888P Y88888P Y88888P  `Y88P'    YP    
                                                                                               
    DISPLAY_SIGNALS_MULTISELECT = "display_signals_multiselect"                                                                             


    # d88888b d888888b db      d888888b d88888b d8888b.       .o88b.  .d88b.  d8b   db d8888b. d888888b d888888b d888888b  .d88b.  d8b   db .d8888. 
    # 88'       `88'   88      `~~88~~' 88'     88  `8D      d8P  Y8 .8P  Y8. 888o  88 88  `8D   `88'   `~~88~~'   `88'   .8P  Y8. 888o  88 88'  YP 
    # 88ooo      88    88         88    88ooooo 88oobY'      8P      88    88 88V8o 88 88   88    88       88       88    88    88 88V8o 88 `8bo.   
    # 88~~~      88    88         88    88~~~~~ 88`8b        8b      88    88 88 V8o88 88   88    88       88       88    88    88 88 V8o88   `Y8b. 
    # 88        .88.   88booo.    88    88.     88 `88.      Y8b  d8 `8b  d8' 88  V888 88  .8D   .88.      88      .88.   `8b  d8' 88  V888 db   8D 
    # YP      Y888888P Y88888P    YP    Y88888P 88   YD       `Y88P'  `Y88P'  VP   V8P Y8888D' Y888888P    YP    Y888888P  `Y88P'  VP   V8P `8888Y' 
                                                                                                                                                
                                                                                                                                              

    FILTER_CONDITION_USER_KEY = "filter_condition_user"
    FILTER_CONDITION_GUI_KEY = "filter_condition_gui"
    FILTER_CONDITION_FINAL_KEY = "filter_condition_final"
    
    ### DEFAULT
    FILTER_CONDITION_N_UNIVERSAL_KEY = "n_fc"
    FILTER_CONDITION_DEFAULT_SELECT_BOX_KEY = "default_fc_selectbox_0"
    
    ### Text
    FILTER_CONDITION_TEXT_SELECT_BOX_KEY_PREFIX = "text_fc_selectbox_"
    FILTER_CONDITION_TEXT_SIGNAL_OPTIONS_SELECT_BOX_KEY_PREFIX = "text_fc_option_selectbox_"
    FILTER_CONDITION_TEXT_DELETE_BTN_KEY_PREFIX = "text_fc_delete_btn_"
    
    FILTER_CONDITION_TEXT_LIST_ORDER_KEY = "text_fc_list_order"
    FILTER_CONDITION_TEXT_SIGNALS_MULTISELECT_KEY = "text_fc_signals_multiselect"
    FILTER_CONDITION_TEXT_ADD_NEW_ROW_BTN_KEY = "add_new_text_fc_btn"
    
    
    ### Numeric 
    FILTER_CONDITION_NUMERIC_SIGNAL_SELECT_BOX_KEY_PREFIX = "numeric_fc_selectbox_"
    FILTER_CONDITION_NUMERIC_LOGICAL_SYMBOL_KEY_PREFIX = "numeric_fc_logical_symbol_"
    FILTER_CONDITION_NUMERIC_SIGNAL_VALUE_KEY_PREFIX = "numeric_fc_value_"
    FILTER_CONDITION_NUMERIC_SIGNAL_VALUE_INTERVAL_KEY_PREFIX = "numeric_fc_value_interval_"
    FILTER_CONDITION_NUMERIC_DELETE_BTN_KEY_PREFIX = "numeric_fc_delete_btn_"
    
    FILTER_CONDITION_NUMERIC_LIST_ORDER_KEY = "numeric_fc_list_order"
    FILTER_CONDITION_NUMERIC_SIGNALS_MULTISELECT_KEY = "numeric_fc_signals_multiselect"
    FILTER_CONDITION_NUMERIC_ADD_NEW_ROW_BTN_KEY = "add_new_numeric_fc_btn"

    


    # .d8888. db    db .d8888. d888888b d88888b .88b  d88.      d888888b d8b   db .d8888. d888888b d8888b. db    db  .o88b. d888888b d888888b  .d88b.  d8b   db .d8888. 
    # 88'  YP `8b  d8' 88'  YP `~~88~~' 88'     88'YbdP`88        `88'   888o  88 88'  YP `~~88~~' 88  `8D 88    88 d8P  Y8 `~~88~~'   `88'   .8P  Y8. 888o  88 88'  YP 
    # `8bo.    `8bd8'  `8bo.      88    88ooooo 88  88  88         88    88V8o 88 `8bo.      88    88oobY' 88    88 8P         88       88    88    88 88V8o 88 `8bo.   
    # `Y8b.    88      `Y8b.    88    88~~~~~ 88  88  88         88    88 V8o88   `Y8b.    88    88`8b   88    88 8b         88       88    88    88 88 V8o88   `Y8b. 
    # db   8D    88    db   8D    88    88.     88  88  88        .88.   88  V888 db   8D    88    88 `88. 88b  d88 Y8b  d8    88      .88.   `8b  d8' 88  V888 db   8D 
    # `8888Y'    YP    `8888Y'    YP    Y88888P YP  YP  YP      Y888888P VP   V8P `8888Y'    YP    88   YD ~Y8888P'  `Y88P'    YP    Y888888P  `Y88P'  VP   V8P `8888Y'                                                                                                                                                     

    SYSTEM_INSTRUCTION_PLANNER_KEY = "system_instruction_planner"    
    SYSTEM_INSTRUCTION_PLANNER_DEFAULT_KEY = "system_instruction_planner_default"    
    
    SYSTEM_INSTRUCTION_PLANNER_REFINED_KEY = "system_instruction_planner_refined"
    SYSTEM_INSTRUCTION_PLANNER_REFINED_DEFAULT_KEY = "system_instruction_planner_refined_default"
    
    SYSTEM_INSTRUCTION_CI_COMPUTATION_KEY = "system_instruction_ci_computation"
    SYSTEM_INSTRUCTION_CI_COMPUTATION_DEFAULT_KEY = "system_instruction_ci_computation_default"
    
    SYSTEM_INSTRUCTION_CI_PLOT_KEY = "system_instruction_ci_plot"
    SYSTEM_INSTRUCTION_CI_PLOT_DEFAULT_KEY = "system_instruction_ci_plot_default"
                                                        
                                                        
