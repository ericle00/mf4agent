_TEXT_COLOR_MAPPING = {
    "blue": "36;1",
    "yellow": "33;1",
    "pink": "38;5;200",
    "green": "32;1",
    "red": "31;1",
}

                                                                                                              
def get_colored_text(text: str, color: str) -> str:
    """
    Get colored text.

    Args:
        text (str): The text to be colored.
        color (str): The color name. Supported colors: "blue", "yellow", "pink", "green", "red".

    Returns:
        str: The colored text.
    """
    color_str = _TEXT_COLOR_MAPPING[color]
    return f"\u001b[{color_str}m\033[1;3m{text}\u001b[0m"                                                                            
                                                                                         


def get_bolded_text(text: str) -> str:
    """
    Get bolded text.

    Args:
        text (str): The text to be bolded.

    Returns:
        str: The bolded text.
    """
    return f"\033[1m{text}\033[0m"


def print_model_name(model: str) -> None:
    """
    Print prompt after formatting with green color.

    Args:
        prompt (str): The prompt to be formatted and printed.

    Returns:
        None
    """
    header = get_bolded_text("Model:")
    colored_prompt = get_colored_text(model, "blue")
    print(f"\n{header}\n\n {colored_prompt}\n")
            
                                                      
                                                                                                       
def print_prompt_after_formatting(prompt: str) -> None:
    """
    Print prompt after formatting with green color.

    Args:
        prompt (str): The prompt to be formatted and printed.

    Returns:
        None
    """
    header = get_bolded_text("Prompt after formatting:")
    colored_prompt = get_colored_text(prompt, "green")
    print(f"\n{header}\n\n {colored_prompt}\n")
                                                                                                                           
                                                                                                                                     


def print_generation_parameters(generation_parameters: dict) -> None:
    """
    Print prompt after formatting with green color.

    Args:
        prompt (str): The prompt to be formatted and printed.

    Returns:
        None
    """
    header = get_bolded_text("Generation parameters:")
    colored_prompt = get_colored_text(generation_parameters, "yellow")
    print(f"\n{header}\n\n {colored_prompt}\n")
  
                                                                              

def print_llm_answer(llm_answer: str) -> None:
    """
    Print LLM answer with red color.

    Args:
        llm_answer (str): The LLM answer to be printed.

    Returns:
        None
    """
    header = get_bolded_text("LLM output:")
    colored_prompt = get_colored_text(llm_answer, "red")
    print(f"\n{header}\n\n {colored_prompt}\n")                                                                                                                                   
                                                                                                                                                

def print_colored_text(text: str, color: str) -> None:
    """
    Print colored text.

    Args:
        text (str): The text to be printed.
        color (str): The color name. Supported colors: "blue", "yellow", "pink", "green", "red".

    Returns:
        None
    """
    colored_text = get_colored_text(text, color)
    print(colored_text)
