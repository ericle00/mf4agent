from lagent.schema import ActionReturn, ActionStatusCode, ActionValidCode

from agent.actions.action_base_class import ActionBaseClass
from models.llms.llms import OpenAICoreML

from models.chat_templates.chat_template_base import system_message, user_message

class PlanningAction(ActionBaseClass):
    def __init__(self, 
                 llm: OpenAICoreML = OpenAICoreML(model="llama-31-70b")): 
        super().__init__()
        self.llm = llm

        
    @property
    def action_description(self):
        return (
            "This action is the primary resource planning breaking analysis into steps"
        )

    @property
    def examples(self):
        return [
            "1. Step 1\n 2. Step 2\n 3. Step 3",
        ]

    @property
    def returns(self):
        return "The plan in a step by step list"

    @property
    def parameter_descriptions(self):
        return ["User query",
                "Planning system instruction",
                "Generation Parameters"]
            
    def __call__(self, user_query_reformatted:str, 
                 system_instruction_planner_generic:str,
                 generation_parameters: dict = {"max_tokens":4096, "temperature":0.0, "top_p":1.0, "top_k":50},
                 *args, **kwargs) -> ActionReturn:
        """
        Generate the plan.
        If a exception is raised, return failed ActionReturn.
        """
        self.user_query_reformatted = user_query_reformatted
        self.system_instruction_planner_generic = system_instruction_planner_generic
        try:            
            # Initial generic plan
            prompt = [system_message(system_instruction_planner_generic),
                      user_message(user_query_reformatted)]
            
            plan_initial_generic = self.llm.chat(prompt, **generation_parameters)

            # Store result
            result = plan_initial_generic
            
        except Exception as e:
            return ActionReturn(
                args={"User query reformatted": self.user_query_reformatted,
                        "system_instruction_planner_generic":self.system_instruction_planner_generic,
                        "generation_parameters": generation_parameters
                      },
                type=self.name,
                errmsg=str(e),
                state=ActionStatusCode.ING,
            )

        action_return = ActionReturn(
                args={"User query reformatted": self.user_query_reformatted,
                        "system_instruction_planner_generic":self.system_instruction_planner_generic,
                        "generation_parameters": generation_parameters

                      },
            type=self.name,
            result=result,
            state=ActionStatusCode.SUCCESS,
            valid=ActionValidCode.OPEN,
        )

        return action_return