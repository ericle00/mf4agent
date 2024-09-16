from lagent.schema import ActionReturn, ActionStatusCode, ActionValidCode

from agent.actions.action_base_class import ActionBaseClass
from models.llms.llms import OpenAICoreML
from models.chat_templates.chat_template_base import system_message, user_message

class RoleCoderSelectionAction(ActionBaseClass):
    
    SYSTEM_PROMPT = """
You are the selector, responsible for determining whether the intended action is to perform computations, plot, or both. 

To assist in identifying the user query, follow these steps:
- Analyze the user query for specific keywords or phrases indicating the required action(s).
- For Computations: Look for indicators such as "calculate", "compute", "integrate", "determine", "average", "median", "max", "min" to identify a need for statistical computations.
- For Plot Generation: Search for "plot", "graph", "visualize", "chart", "histogram", and "heatmap" to pinpoint requests for data visualization.
- For Both Actions: If both computational and visualization keywords are present, recognize a need plot.

Base your analysis solely on information explicitly provided in the user query. 
ALWAYS answer in JSON format with a list of strings using brackets. Do not write anything else!

- If you identify plot then answer ['plot']
- If you identify computation then answer ['computation']
- If you identify both computation and plot then answer ['plot']
    """

    def __init__(self,
                llm: DelegateDecoder = DelegateDecoder(model="llama-31-70b")):
        super().__init__()
        self.llm = llm
        
    @property
    def action_description(self):
        return (
            "This action decides whether the user_query requires computation, plot or both."
        )

    @property
    def examples(self):
        return [""]

    @property
    def returns(self):
        return """The answer should be answered in JSON format: 'plot':True, 'computation':True"""

    @property
    def parameter_descriptions(self):
        return ["User query alone.",
                "Generation Parameters"]
            
    def __call__(self, 
                 user_query:str,
                 generation_parameters: dict = {"max_tokens":4096, "temperature":0.0, "top_p":1.0, "top_k":50}, 
                 *args, **kwargs) -> ActionReturn:
        """
        Generate the plan.
        If a exception is raised, return failed ActionReturn.
        """

        try:
            # TODO IF we dont have the right format the resample
            prompt = [system_message(self.SYSTEM_PROMPT),
                      user_message(user_query)]
            
            llm_answer = self.llm.chat(prompt, **generation_parameters)
            
            role_list = llm_answer            
            if "plot" in role_list:
                result = "plot"
            else:
                result = "computation"            
            
        except Exception as e:
            return ActionReturn(
                args={"User Query": user_query,
                    "generation_parameters": generation_parameters},
                type=self.name,
                errmsg=str(e),
                state=ActionStatusCode.ING,
            )

        action_return = ActionReturn(
            args={"User Query": user_query,
                  "generation_parameters": generation_parameters},
            type=self.name,
            result=result,
            state=ActionStatusCode.SUCCESS,
            valid=ActionValidCode.OPEN,
        )

        return action_return