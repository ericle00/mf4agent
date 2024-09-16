import re
import json5


def add_period_if_missing(s: str):
    """
    Add a period at the end of the string if it is missing.

    Args:
        s (str): The input string to check and modify.

    Returns:
        str: The modified string with a period at the end if it was missing.
    """
    s = s.strip()  # Remove leading and trailing whitespaces

    if not s.endswith("."):
        s += "."
    
    return s


# d8888b. d88888b d8888b. db       .d8b.   .o88b. d88888b      db   d8b   db  .d88b.  d8888b. d8888b. 
# 88  `8D 88'     88  `8D 88      d8' `8b d8P  Y8 88'          88   I8I   88 .8P  Y8. 88  `8D 88  `8D 
# 88oobY' 88ooooo 88oodD' 88      88ooo88 8P      88ooooo      88   I8I   88 88    88 88oobY' 88   88 
# 88`8b   88~~~~~ 88~~~   88      88~~~88 8b      88~~~~~      Y8   I8I   88 88    88 88`8b   88   88 
# 88 `88. 88.     88      88booo. 88   88 Y8b  d8 88.          `8b d8'8b d8' `8b  d8' 88 `88. 88  .8D 
# 88   YD Y88888P 88      Y88888P YP   YP  `Y88P' Y88888P       `8b8' `8d8'   `Y88P'  88   YD Y8888D' 
                                                                                                    
                                                                                                
def replace_word(sentence, old_word, new_word):
    """
    Replace occurrences of a word in a sentence.

    Args:
        sentence (str): The input sentence.
        old_word (str): The word to be replaced.
        new_word (str): The new word to replace the old one.

    Returns:
        str: The modified sentence.
    """
    # Split the sentence into words
    words = sentence.split()

    # Iterate through each word
    for i, word in enumerate(words):
        # Check if the last character is a period or comma
        if word[-1] in ['.', ',', '/', '*', '+', '-','?']:
            # If it is, check if the word without the period or comma matches the old word
            if word[:-1] == old_word:
                # If it matches, replace it with the new word and add the period or comma back
                words[i] = new_word + word[-1]
        else:
            # If the last character is not a period or comma, directly check for a match
            if word == old_word:
                # If it matches, replace it with the new word
                words[i] = new_word

    # Join the words back into a sentence
    new_sentence = ' '.join(words)
    return new_sentence



# .d8888. d8888b. db      d888888b d888888b      .d8888. d888888b d8888b. d888888b d8b   db  d888b  
# 88'  YP 88  `8D 88        `88'   `~~88~~'      88'  YP `~~88~~' 88  `8D   `88'   888o  88 88' Y8b 
# `8bo.   88oodD' 88         88       88         `8bo.      88    88oobY'    88    88V8o 88 88      
#   `Y8b. 88~~~   88         88       88           `Y8b.    88    88`8b      88    88 V8o88 88  ooo 
# db   8D 88      88booo.   .88.      88         db   8D    88    88 `88.   .88.   88  V888 88. ~8~ 
# `8888Y' 88      Y88888P Y888888P    YP         `8888Y'    YP    88   YD Y888888P VP   V8P  Y888P  
                                                                                                  
                                                                                                  
def split_string(input_string) -> list[str]:
    """
    Split a string into a list of words and punctuation marks.

    Args:
        input_string (str): The input string to be split.

    Returns:
        list[str]: A list containing the words and punctuation marks.
    """
    # Split the string based on whitespace and periods using regex
    split_result = re.split(r'\s+|\.|,', input_string)
    # Remove empty strings from the result
    split_result = [item for item in split_result if item.strip()]
    return split_result


# d88888b db    db d888888b d8888b.  .d8b.   .o88b. d888888b       .d8b.  d88888b d888888b d88888b d8888b.      db   dD d88888b db    db db   d8b   db  .d88b.  d8888b. d8888b. 
# 88'     `8b  d8' `~~88~~' 88  `8D d8' `8b d8P  Y8 `~~88~~'      d8' `8b 88'     `~~88~~' 88'     88  `8D      88 ,8P' 88'     `8b  d8' 88   I8I   88 .8P  Y8. 88  `8D 88  `8D 
# 88ooooo  `8bd8'     88    88oobY' 88ooo88 8P         88         88ooo88 88ooo      88    88ooooo 88oobY'      88,8P   88ooooo  `8bd8'  88   I8I   88 88    88 88oobY' 88   88 
# 88~~~~~  .dPYb.     88    88`8b   88~~~88 8b         88         88~~~88 88~~~      88    88~~~~~ 88`8b        88`8b   88~~~~~    88    Y8   I8I   88 88    88 88`8b   88   88 
# 88.     .8P  Y8.    88    88 `88. 88   88 Y8b  d8    88         88   88 88         88    88.     88 `88.      88 `88. 88.        88    `8b d8'8b d8' `8b  d8' 88 `88. 88  .8D 
# Y88888P YP    YP    YP    88   YD YP   YP  `Y88P'    YP         YP   YP YP         YP    Y88888P 88   YD      YP   YD Y88888P    YP     `8b8' `8d8'   `Y88P'  88   YD Y8888D' 
                                                                                                                                                                              
                                                                                                                                                                              
def extract_after_keyword(path: str, split_symbol: str, keyword: str) -> str:
    """
    Extracts the part of the path that comes after the specified keyword.

    Args:
        path (str): The input path.
        split_symbol (str): The symbol to split the path by.
        keyword (str): The keyword to search for in the path.

    Returns:
        str: The part of the path that comes after the keyword.
              If the keyword is not found in the path, returns a message indicating that.
    """
    segments = path.split(split_symbol)
    try:
        index = segments.index(keyword)
        return split_symbol.join(segments[index + 1:])
    except ValueError:
        return "Keyword not found in the path"



# d8888b. d88888b .88b  d88.  .d88b.  db    db d88888b       .o88b.  .d88b.  d8888b. d88888b      d8888b. db       .d88b.   .o88b. db   dD .d8888. 
# 88  `8D 88'     88'YbdP`88 .8P  Y8. 88    88 88'          d8P  Y8 .8P  Y8. 88  `8D 88'          88  `8D 88      .8P  Y8. d8P  Y8 88 ,8P' 88'  YP 
# 88oobY' 88ooooo 88  88  88 88    88 Y8    8P 88ooooo      8P      88    88 88   88 88ooooo      88oooY' 88      88    88 8P      88,8P   `8bo.   
# 88`8b   88~~~~~ 88  88  88 88    88 `8b  d8' 88~~~~~      8b      88    88 88   88 88~~~~~      88~~~b. 88      88    88 8b      88`8b     `Y8b. 
# 88 `88. 88.     88  88  88 `8b  d8'  `8bd8'  88.          Y8b  d8 `8b  d8' 88  .8D 88.          88   8D 88booo. `8b  d8' Y8b  d8 88 `88. db   8D 
# 88   YD Y88888P YP  YP  YP  `Y88P'     YP    Y88888P       `Y88P'  `Y88P'  Y8888D' Y88888P      Y8888P' Y88888P  `Y88P'   `Y88P' YP   YD `8888Y' 
                                                                                                                                                 
                                                                                                                                                 

def extract_and_join_python_blocks(text: str) -> str:
    # Regular expression to match Python code blocks
    pattern = re.compile(r'```python(.*?)```', re.DOTALL)
    
    # Find all matches
    matches = pattern.findall(text)
    
    # Join all the matched code blocks
    joined_code = '\n'.join(matches)
    
    return joined_code
