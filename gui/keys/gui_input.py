"""Holds input keys for GUI components, such as text inputs, dropdowns, and checkboxes, to track user input and interact with the application."""

class GUIInput:
    # User query
    USER_QUERY_KEY = "user_query"
    
    # MF4 filepath
    MF4_FILE_PATH_KEY = "mf4_filepath"
    FILTER_CONDITION_KEY = "filter_condition"
    
    # Code actions
    CODE_ACTIONS_MAP_KEY = "code_actions_map"
    CODE_ACTIONS_SHOW_CODE_KEY = "generate_code"
    CODE_ACTIONS_RUN_CODE_KEY = "run_code"
    
    # Signal map
    SIGNAL_MAP_KEY = "signal_map"
    
    # System instruction planner map
    SYSTEM_INSTRUCTION_PLANNER_KEY = "system_instruction_planner_map"
    SYSTEM_INSTRUCTION_PLANNER_GENERIC_KEY = "system_instruction_planner_generic"
    
    # System instruction CI map
    SYSTEM_INSTRUCTION_CI_MAP_KEY = "system_instruction_ci_map"
    SYSTEM_INSTRUCTION_CI_COMPUTATION_KEY = "computation"
    SYSTEM_INSTRUCTION_CI_PLOT_KEY = "plot"
    
    # Sum actions
    N_ACTIONS = "n_actions"
    
    GENERATION_PARAMETERS_PLANNER_KEY = "generation_parameters_planner"
    GENERATION_PARAMETERS_CI_KEY = "generation_parameters_ci"