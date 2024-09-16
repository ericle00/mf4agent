from lagent.schema import ActionReturn, ActionStatusCode, ActionValidCode

from agent.actions.action_base_class import ActionBaseClass
from models.llms.llms import OpenAICoreML

from models.chat_templates.chat_template_base import system_message, user_message
from utils.text_string import extract_and_join_python_blocks

class CodeGenerationAction(ActionBaseClass):
    def __init__(self, 
                 llm: OpenAICoreML = OpenAICoreML(model="llama-31-70b")):
        super().__init__()
        self.llm = llm

        
    @property
    def action_description(self):
        return (
            "This action generates the code for doing computation or plot."
        )

    @property
    def examples(self):
        return [""]

    @property
    def returns(self):
        return """The code."""

    @property
    def parameter_descriptions(self):
        return ["Plan with steps.",
                "System Instruction",                
                "Generation parameters"]
            
    def __call__(self, 
                 plan:str, 
                 system_instruction: str,
                 generation_parameters: dict = {"max_tokens":4096, "temperature":0.0, "top_p": 1.0, "top_k":50},
                 *args, **kwargs) -> ActionReturn:
        """
        Generate the plan.
        If a exception is raised, return failed ActionReturn.
        """

        try:
            # Plan            
            prompt = [system_message(system_instruction),
                      user_message(plan)]
            
            # Generate code
            llm_answer = self.llm.chat(prompt, **generation_parameters)

            # Extract code
            python_code = extract_and_join_python_blocks(llm_answer)
            
            if python_code:
                result = f"```python\n{python_code}\n```"
            else:
                result = "``````"
                

        except Exception as e:
            return ActionReturn(
                args={"plan": plan,
                      "system_instruction": system_instruction,
                      "generation_parameters": generation_parameters},
                type=self.name,
                errmsg=str(e),
                state=ActionStatusCode.ING,
            )

        action_return = ActionReturn(
            args={"plan": plan,
                      "system_instruction": system_instruction,
                      "generation_parameters": generation_parameters},
            type=self.name,
            result=result,
            state=ActionStatusCode.SUCCESS,
            valid=ActionValidCode.OPEN,
        )

        return action_return