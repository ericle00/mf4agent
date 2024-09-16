from utils.markdown import MD

class ChatPageHeader:
    """
    A class representing chat page header constants.

    This class provides constants for chat page headers, using Markdown formatting.

    Attributes:
    GUI_INPUT (str): The header for GUI input, formatted as an H5 header with a magnifying glass emoji.
    GENERIC_PLAN (str): The header for a generic plan, formatted as an H5 header with a thinking face emoji.
    REFINED_PLAN (str): The header for a refined plan, formatted as an H5 header with a thinking face emoji.
    GENERATED_CODE (str): The header for generated code, formatted as an H5 header with a computer emoji.
    EXECUTED_CODE (str): The header for executed code, formatted as an H5 header with a abacus and chart emojis.
    EXCEL_SHEET (str): The header for an Excel sheet, formatted as an H5 header with a checkmark emoji.
    PROGRESS_BAR (str): The header for a progress bar, formatted as an H5 header with a stopwatch emoji.
    GENERATED_USER_QUERY_HEADER (str): A template for a generated user query header, formatted as an H5 header with a hashtag emoji.
    THINKING (str): A message indicating that the system is thinking, formatted with a stopwatch emoji.
    """
    GUI_INPUT = f"{MD.H5} GUI Input  🔍"    
    
    GENERIC_PLAN = f"{MD.H5} Generic Plan 🧠"
    
    REFINED_PLAN = f"{MD.H5} Refined Plan 🧠"
    
    GENERATED_CODE = f"{MD.H5} Generated code 💻"
    
    EXECUTED_CODE = f"{MD.H5} Executed code 🔢📊"
    
    EXCEL_SHEET = f"{MD.H5} Excel sheet ✅"
    
    PROGRESS_BAR = f"{MD.H5} Progress Bar ⏭️"
    
    GENERATED_USER_QUERY_HEADER = "##### #️⃣ {}"
    
    THINKING = "⏳ Thinking..."