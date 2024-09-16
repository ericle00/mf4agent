from functools import cached_property

from agent.components.brain import Brain

from models.llms.llms import OpenAICoreML
from agent.actions.ipython_interpreter import IPythonInterpreter

from gui.keys.st_ss import ST_SS
from gui.keys.gui_input import GUIInput

from models.chat_templates.chat_template_base import system_message, user_message
from utils.text_string import add_period_if_missing

from agent.prompts.generating_header import SYSTEM_INSTRUCTION_GENERATE_HEADER_FROM_USER_QUERY

class ChatbotGUIAgentWrapper:
    def __init__(self, 
                 st_ss: dict) -> None:
        """
        Initialize the chatbot GUI agent wrapper.

        Parameters:
            st_ss (st.session_state): Streamlit session state
        """
        self.st_ss = st_ss

    @cached_property
    def app_name(self):
        return "MF4 Agent App"
    
    def extract_decoder_from_status(self, selected_model_status: str) -> str:
        for decoder in self.st_ss[ST_SS.DECODER_MODELS_KEY]:
            if decoder in selected_model_status:
                return decoder

    @cached_property
    def planner_llm(self) -> OpenAICoreML: 
        model = self.extract_decoder_from_status(
            self.st_ss[ST_SS.SELECTED_PLANNER_KEY]
        )
        return OpenAICoreML(model=model)
    
    @cached_property
    def code_interpreter_llm(self) -> OpenAICoreML:
        model = self.extract_decoder_from_status(
            self.st_ss[ST_SS.SELECTED_CODE_INTERPRETER_KEY]
        )
        return OpenAICoreML(model=model)

    @property
    def ipython_interpreter(self) -> IPythonInterpreter:
        """
        Create an IPython interpreter.

        Parameters:
            work_dir (str): Working directory

        Returns:
            IPythonInterpreter: IPython interpreter object
        """
        if ST_SS.IPYTHON_INTERPRETER_ACTION_KEY not in self.st_ss:
            self.st_ss[ST_SS.IPYTHON_INTERPRETER_ACTION_KEY] = IPythonInterpreter(timeout=10000, work_dir=self.st_ss.get(ST_SS.PATH_HOME)+"/images")
        return self.st_ss[ST_SS.IPYTHON_INTERPRETER_ACTION_KEY]
    
    
    @cached_property
    def brain_agent(self) -> Brain:
        """
        Initialize and return the Brain agent using the MIXTRAL_LLM and LLAMA_LLM instances, and 
        the IPython interpreter with the specified working directory.

        Returns:
            Brain: The initialized Brain agent.
        """
        return Brain(llm_thinker = self.planner_llm,
                     llm_coder = self.code_interpreter_llm,
                     ipython_interpreter=self.ipython_interpreter)
        
        
    @property
    def planner_input(self) -> dict:
        """
        Generates a dictionary with the required inputs for the planner, including
        the MF4 file path, system instruction planner, and generation parameters.

        Returns:
            dict: A dictionary containing the MF4 file path, system instruction planner,
                and generation parameters.
        """
        # Mf4 filepath
        mf4_filepath = f"'{self.st_ss[ST_SS.MF4_FILES_PATH_MAP_KEY].get(self.st_ss[ST_SS.SELECTED_MF4_FILE_KEY])}'"
        
        # System instruction planner
        system_instruction_planner = self.st_ss[ST_SS.SYSTEM_INSTRUCTION_PLANNER_KEY]
        
        # Generation Parameters
        generation_parameters = {
            'max_tokens': self.st_ss[ST_SS.PLANNER_MAX_TOKENS_KEY],
            'temperature': self.st_ss[ST_SS.PLANNER_TEMPERATURE_KEY],
            'top_p': self.st_ss[ST_SS.PLANNER_TOP_P_KEY],
            'top_k': self.st_ss[ST_SS.PLANNER_TOP_K_KEY]
        }    
        
        return {GUIInput.MF4_FILE_PATH_KEY: mf4_filepath,
                GUIInput.SYSTEM_INSTRUCTION_PLANNER_KEY: system_instruction_planner,
                GUIInput.GENERATION_PARAMETERS_PLANNER_KEY: generation_parameters}

         
    @property
    def code_interpreter_input(self) -> dict:
        """    Generates a dictionary with the required inputs for the code interpreter,
        including code actions, signal map, system instruction map, and generation
        parameters.

        Returns:
            dict: A dictionary containing code actions, signal map, system
                instruction map, and generation parameters.
        """
        # Code actions map 
        code_actions_map: dict[str, bool] = {GUIInput.CODE_ACTIONS_SHOW_CODE_KEY: self.st_ss.get(ST_SS.TOGGLE_SHOW_CODE_KEY), 
                                             GUIInput.CODE_ACTIONS_RUN_CODE_KEY: self.st_ss.get(ST_SS.TOGGLE_RUN_CODE_KEY)}

        # Signal map of names, possible values and units
        numeric_signal_map = self.st_ss[ST_SS.MF4_FILES_SIGNAL_MAP][self.st_ss[ST_SS.SELECTED_MF4_FILE_KEY]][ST_SS.NUMERIC_SIGNALS_INFO_KEY]
        text_signal_map = self.st_ss[ST_SS.MF4_FILES_SIGNAL_MAP][self.st_ss[ST_SS.SELECTED_MF4_FILE_KEY]][ST_SS.TEXT_SIGNALS_INFO_KEY]
        signal_map = {**numeric_signal_map, **text_signal_map}
        
        # System instruction map
        system_instruction_ci_map = {GUIInput.SYSTEM_INSTRUCTION_CI_COMPUTATION_KEY: self.st_ss[ST_SS.SYSTEM_INSTRUCTION_CI_COMPUTATION_KEY], 
                                GUIInput.SYSTEM_INSTRUCTION_CI_PLOT_KEY:  self.st_ss[ST_SS.SYSTEM_INSTRUCTION_CI_PLOT_KEY]} 
        
        # Generation parameters
        generation_parameters = {
            'max_tokens': self.st_ss[ST_SS.CI_MAX_TOKENS_KEY],
            'temperature': self.st_ss[ST_SS.CI_TEMPERATURE_KEY],
            'top_p': self.st_ss[ST_SS.CI_TOP_P_KEY],
            'top_k': self.st_ss[ST_SS.CI_GENERATION_CONFIG_TOP_K_KEY]
        }    
        
        return {GUIInput.CODE_ACTIONS_MAP_KEY: code_actions_map,
                GUIInput.SIGNAL_MAP_KEY: signal_map,
                GUIInput.SYSTEM_INSTRUCTION_CI_MAP_KEY: system_instruction_ci_map,
                GUIInput.GENERATION_PARAMETERS_CI_KEY: generation_parameters}
        
    @property
    def action_input(self) -> dict:
        """
        Generates a dictionary with the total number of active actions based on
        toggle states.

        Returns:
            dict: A dictionary containing the total number of active actions.
        """
        # Number of actions
        action_toggles_list = [self.st_ss[ST_SS.TOGGLE_SHOW_PLAN_KEY], # Show plan
                               self.st_ss[ST_SS.TOGGLE_SHOW_CODE_KEY], # Show code
                              self.st_ss[ST_SS.TOGGLE_RUN_CODE_KEY], # Run code
                              True if self.st_ss[ST_SS.TOGGLE_SHOW_CODE_KEY] or self.st_ss[ST_SS.TOGGLE_RUN_CODE_KEY] else False] # Selector
        
        # Sum the number of actions
        n_sum_actions = sum(1 for action in action_toggles_list if action)
        return {GUIInput.N_ACTIONS: n_sum_actions}
        
        
    def generate_header_from_user_query(self, user_query:str) -> str:
        """
        Generates a header based on the user's query using the mixtral language model.

        Args:
            user_query (str): The query from the user to generate the header.

        Returns:
            str: The generated header string.
        """
        system_instruction = SYSTEM_INSTRUCTION_GENERATE_HEADER_FROM_USER_QUERY

        prompt = [system_message(system_instruction),
                  user_message(user_query)]
        
        generated_header = self.planner_llm.chat(prompt, **{"max_tokens": 10}).replace('"', '').replace("'", "")
        
        return generated_header.strip()
    
    
    
    def ask(self, query:str, filter_conditions: str="") -> str:
        """
        Process a user query through the Brain agent with provided or session-based filter conditions.

        Args:
            query (str): The user's query.
            filter_conditions (str, optional): The filter conditions to apply. Defaults to "".

        Returns:
            str: The response from the Brain agent.
        """
        # Add period to user query if missing 
        user_query = add_period_if_missing(query)
               
        # If empty filter conditions use from GUI,text 
        if not filter_conditions:
            filter_conditions = self.st_ss.get(ST_SS.FILTER_CONDITION_FINAL_KEY)
        
        # Combine GUI Inputs
        gui_input = {GUIInput.USER_QUERY_KEY: user_query,
                     GUIInput.FILTER_CONDITION_KEY: filter_conditions}
        
        agent_input = {**gui_input, 
                       **self.planner_input, 
                       **self.code_interpreter_input, 
                       **self.action_input}
        
        # Agent return
        agent_return  = self.brain_agent.chat(agent_input)
        return agent_return.response

