from lagent import BaseAction
from dataclasses import dataclass
from typing import List, Union
from typing import _GenericAlias
from types import FunctionType, BuiltinFunctionType
from abc import ABCMeta, abstractmethod

import inspect

DEFAULT_HOW_TO_PROMPT = """    ```json
    {{
        "action": {{
            "reason": ...,
            "name": "{action_name}",
            "arguments": {{
                {argument_list}
            }}
        }}
    }}
    ```"""


@dataclass
class DescriptionInfo:
    """Dataclass to store information to used in the LLM prompt"""

    description: str
    """Description of what the function does"""
    parameter_descriptions: Union[str, List[str]]
    """Short description of each parameter in the function"""
    returns: str = None
    """(Optional) What does the function returns"""
    examples: Union[str, List[str]] = None
    """(Optional) Example on when/how to use this function"""


# d8888b.  .d8b.  .d8888. d88888b
# 88  `8D d8' `8b 88'  YP 88'
# 88oooY' 88ooo88 `8bo.   88ooooo
# 88~~~b. 88~~~88   `Y8b. 88~~~~~
# 88   8D 88   88 db   8D 88.
# Y8888P' YP   YP `8888Y' Y88888P


class ActionBaseClass(BaseAction, metaclass=ABCMeta):
    """
    A class to make it easier to write descriptions and examples for the LLM prompt.
    """

    def __init__(self):
        """
        Init the action_base_class

        Remember to create methods for `action_description`, `parameter_descriptions`, `returns` and `examples`.
        """
        class_name = self.__class__.__name__

        # Create the description
        description_info = DescriptionInfo(
            description=self.action_description,
            parameter_descriptions=self.parameter_descriptions,
            returns=self.returns,
            examples=self.examples,
        )
        # TODO: If we have time, we could use `__.doc__` instead
        description = DescriptionFormatter().format_description(
            func=self.__call__, class_name=class_name, description_info=description_info
        )

        # Init the super class, lagent BaseAction
        super().__init__(description, class_name)

    @property
    @abstractmethod
    def action_description(self) -> str:
        """
        Provide a description of the action.

        Returns:
            A string of what the action you created does
        """

    @property
    @abstractmethod
    def parameter_descriptions(self) -> Union[str, List[str]]:
        """
        Provide a description of each parameter in the `__call__` method.

        Returns:
            A string, or a list of strings, with a short description of each parameter
        """

    @property
    @abstractmethod
    def returns(self) -> str:
        """
        (Optional) Provide a description of what the `__call__` method returns.
        You can just return `None` if you do not want a return description.

        Returns:
            A string of what the `__call__` method returns
        """

    @property
    @abstractmethod
    def examples(self) -> Union[str, List[str]]:
        """
        (Optional) Provide a some examples on how to use the action you created.
        You can just return `None` if you do not want a return description.

        Returns:
            A string, or a list of strings, with examples on how/when to use this action
        """


# d88888b  .d88b.  d8888b. .88b  d88.  .d8b.  d888888b d888888b d88888b d8888b.
# 88'     .8P  Y8. 88  `8D 88'YbdP`88 d8' `8b `~~88~~' `~~88~~' 88'     88  `8D
# 88ooo   88    88 88oobY' 88  88  88 88ooo88    88       88    88ooooo 88oobY'
# 88~~~   88    88 88`8b   88  88  88 88~~~88    88       88    88~~~~~ 88`8b
# 88      `8b  d8' 88 `88. 88  88  88 88   88    88       88    88.     88 `88.
# YP       `Y88P'  88   YD YP  YP  YP YP   YP    YP       YP    Y88888P 88   YD


class DescriptionFormatter:

    def format_description(
        self, func: object, class_name: str, description_info: DescriptionInfo
    ) -> str:
        """
        Formats a description of a specific function, `func` parameter.

        Args:
            * func (object): The function you want to generate a description for
            * class_name (str): The name of the class that the function is from
            * description_info (DescriptionInfo): All the information

        Format a string too follow the format:
        ```bash
        ### action_name(par_1: par_1_type, ...)
        Description: action_description

        Args:
            * par_1 (par_1_type): par_1_description
            * ...

        Returns:
            * action_return

        Example:
            * action_example_1
            * ...

        To use this action, write:
            ```json
            {
                "action": {
                    "reason": ...,
                    "name": "action_name",
                    "arguments": {
                        "par_1": ...

                }
            }
            ```
        ```
        """
        self.func = func
        self.class_name = class_name
        self.description_info = description_info

        self.parameter_names, self.parameter_types = self._get_function_signature()

        # Convert to lists
        self.parameter_descriptions = self._to_list(
            self.description_info.parameter_descriptions
        )
        self.examples_info = self._to_list(self.description_info.examples)

        # Check that parameter name, type, and description list are the same length
        self._check_parameter_description_len()

        # Start from the top and work down
        # Step 1
        header = f"{self._construct_header()}\n"

        # Step 2
        description = f"Description: {self.description_info.description}\n\n"

        # Step 3
        args = self._construct_args() + "\n\n"

        # Step 4 (optional)
        returns = ""
        if self.description_info.returns:
            returns = f"Returns:\n    * {self.description_info.returns}\n\n"

        # Step 5 (optional)
        examples = ""
        if self.description_info.examples:
            examples = f"{self._construct_examples()}\n\n"

        # Step 6
        how_to_call = self._construct_how_to()

        # Construct the action description
        description = header + description + args + returns + examples + how_to_call

        return description

    @staticmethod
    def _to_list(thing_to_convert: Union[str, List[str]]) -> List[str]:

        if type(thing_to_convert) != list:
            return [thing_to_convert]

        return thing_to_convert

    def _get_function_signature(self):
        """
        Get the parameter names and the types of a function
        """
        # Get name of the parameters
        parameters = inspect.getfullargspec(self.func).args

        # Remove 'self' or 'clc'
        parameter_names = parameters
        if parameters[0] == "self" or parameters[0] == "clc":
            parameter_names = parameters[1:]

        # Get the function signature
        func_signature = inspect.signature(self.func)

        # Get the type of the parameters
        parameter_types = []
        for par_name in parameter_names:
            type_name = func_signature.parameters[par_name].annotation
            parameter_types.append(DescriptionFormatter._get_type(type_name))

        return parameter_names, parameter_types

    @staticmethod
    def _get_type(var_types: object) -> str:
        """
        Recursive function that finds all the types of an variable and
        returns it as a nice string.

        Args:
            * var_types (object): Some sort of type

        Example:
        ```python
            from typing import List

            a, b ,c = List[int], 'list[int]', str

            print(f"a: {_get_type(a)}, b: {_get_type(b)}, c: {_get_type(c)}")
        ```

        >>> a: list[str], b: list[str], c: str
        """

        # Exit condition 1
        # No type given in function parameter list
        if var_types == inspect._empty:
            return "any"

        # Exit condition 2
        # Normal type (int, float, bool, str, bytes, class)
        if isinstance(var_types, type):
            return var_types.__name__

        # Exit condition 3
        # Type is of string ('list[str]', 'tuple[int,str]', ...)
        if isinstance(var_types, str):
            return var_types

        # Exit condition 4
        # The type is a function (print, len, ...)
        if isinstance(var_types, (FunctionType, BuiltinFunctionType)):
            return var_types.__name__

        # The type is from the 'typing' package
        if isinstance(var_types, _GenericAlias):
            typing = f"{var_types.__origin__.__name__}["

            first_type = True
            for var_type in var_types.__args__:
                # Add ',' if it is not the first type
                if not first_type:
                    typing += ", "
                # Go one step deeper
                typing += DescriptionFormatter._get_type(var_type)

                first_type = False

            typing += "]"

            return typing

        # The type is a class

        # Unknown type
        return "unknown"

    def _check_parameter_description_len(self):
        """
        Will throw ValueError if the lengths are not the same
        """

        if len(self.parameter_names) != len(self.parameter_types):
            error_msg = (
                f"Number of types ({len(self.parameter_types)}) and"
                + f"number of names ({len(self.parameter_names)}) is not the same."
                + "Something is wrong with the internal logic..."
            )
            raise ValueError(error_msg)

        if len(self.parameter_names) != len(self.parameter_descriptions):
            error_msg = (
                f"The number of parameters in the function {self.func.__qualname__} and "
                + "number of descriptions provided needs to be the same length. "
                + f"You have {len(self.parameter_names)} parameters in {self.func.__qualname__}, "
                + f"but only {len(self.parameter_descriptions)} descriptions."
            )
            raise ValueError(error_msg)

    def _construct_header(self) -> str:
        function_parameters = ""
        for par_name, par_type in zip(self.parameter_names, self.parameter_types):
            function_parameters += f"{par_name}: {par_type}, "

        # Remove the last ", "
        function_parameters = function_parameters[:-2]

        return f"### {self.class_name}({function_parameters})"

    def _construct_args(self) -> str:
        args = "Args:\n"
        for par_name, par_type, par_desc in zip(
            self.parameter_names, self.parameter_types, self.parameter_descriptions
        ):
            args += f"    * {par_name} ({par_type}): {par_desc}\n"

        # Remove the last '\n'
        return args[:-1]

    def _construct_examples(self) -> str:
        examples = "Example:\n"
        for example in self.examples_info:
            examples += f"    * {example}\n"

        # Remove the last '\n'
        return examples[:-1]

    def _construct_how_to(self):

        indentation = self._get_how_to_indentation()

        argument_list = ""

        indent = False
        for par_name in self.parameter_names:
            # Indent the key
            if indent:
                argument_list += " " * indentation

            argument_list += f'"{par_name}": ...\n'

            indent = True

        # Remove the last '\n'
        argument_list = argument_list[:-1]

        how_to_prompt = "To use this action, write:\n"
        how_to_prompt += DEFAULT_HOW_TO_PROMPT.format(
            action_name=self.class_name, argument_list=argument_list
        )

        return how_to_prompt

    def _get_how_to_indentation(self):
        """
        Get how many spaces are used for the arguments
        """

        # Get the indentation to the arguments
        first_part = DEFAULT_HOW_TO_PROMPT.split("{action_name}")[0]
        max_indentation = len(first_part.split("\n")[-1]) - 1

        default_indentation = len(DEFAULT_HOW_TO_PROMPT.split("```")[0])
        return max_indentation - default_indentation


# d88888b db    db  .d8b.  .88b  d88. d8888b. db      d88888b
# 88'     `8b  d8' d8' `8b 88'YbdP`88 88  `8D 88      88'
# 88ooooo  `8bd8'  88ooo88 88  88  88 88oodD' 88      88ooooo
# 88~~~~~  .dPYb.  88~~~88 88  88  88 88~~~   88      88~~~~~
# 88.     .8P  Y8. 88   88 88  88  88 88      88booo. 88.
# Y88888P YP    YP YP   YP YP  YP  YP 88      Y88888P Y88888P
if __name__ == "__main__":

    from typing import Tuple
    from lagent.schema import ActionReturn

    class BestAction(ActionBaseClass):
        def __init__(self, llm):

            super().__init__()

            self.llm = llm

        @property
        def action_description(self):
            return "Used to do everything!"

        @property
        def examples(self):
            return None

        @property
        def returns(self):
            return None

        @property
        def parameter_descriptions(self):
            return [
                "User query",
                "Math operation to perform",
                "The main task",
                "Multiple subtasks",
            ]

        def __call__(
            self,
            query: str,
            math,
            tasks_1: "list[str]",
            tasks_2: Tuple[List[List[bool]], Tuple[int, str], float],
            *args,
            **kwargs,
        ) -> ActionReturn:
            # Do some coll action stuff...
            pass

    # Init the class
    best_action = BestAction(None)

    print("\n\nThis is an autogenerated description for the __call__ function!\n")
    print(best_action.description)