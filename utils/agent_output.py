import os 
from PIL import Image, ImageDraw, ImageFont                                                                                                                    

def remove_warnings(content: str) -> str:
    """
    Remove warnings from a given content string.

    Parameters:
    content (str): The input content string.

    Returns:
    str: The content string with warnings removed.
    """
    warning_list = ['ldf is not supported\n',
                    'xlsx is not supported\n', 
                    'xls is not supported\n']
    for s in warning_list:
        if s in content:
            content = content.replace(s, "")
    return content
                                                                                        
                                                                                                   

def insert_source_to_image(image_path: str, mf4_source: str) -> str:
    """
    Insert a source string into an image.

    Parameters:
    image_path (str): The path to the input image.
    mf4_source (str): The source string to insert.

    Returns:
    str: The path to the output image with the source string inserted.
    """
    image_path_sourced = image_path.split()[0] + "_sourced.png"
    if not os.path.exists(image_path_sourced):
        # Open the image
        image = Image.open(image_path) # create an empty image or load your image here

        # Create a drawing object
        draw = ImageDraw.Draw(image)

        # Define the text to be added
        text_source = f"Source: {mf4_source}"

        # Load font
        font_size = 11
        font = ImageFont.load_default()

        _, image_height = image.size
        text_position = (0, image_height - font_size)  # 10 pixels margin from bottom and left

        draw.text(text_position, text_source, font=font, fill="black")  # You can change the fill color

        # Save or display the modified image
        image.save(image_path_sourced)
        
    return image_path_sourced



# .d8888.  .d88b.  db    db d8888b.  .o88b. d88888b      d888888b d88888b db    db d888888b 
# 88'  YP .8P  Y8. 88    88 88  `8D d8P  Y8 88'          `~~88~~' 88'     `8b  d8' `~~88~~' 
# `8bo.   88    88 88    88 88oobY' 8P      88ooooo         88    88ooooo  `8bd8'     88    
#   `Y8b. 88    88 88    88 88`8b   8b      88~~~~~         88    88~~~~~  .dPYb.     88    
# db   8D `8b  d8' 88b  d88 88 `88. Y8b  d8 88.             88    88.     .8P  Y8.    88    
# `8888Y'  `Y88P'  ~Y8888P' 88   YD  `Y88P' Y88888P         YP    Y88888P YP    YP    YP    


def insert_source_to_text(text_output: str, mf4_source: str) -> str:
    """
    Insert a source string into a text output.

    Parameters:
    text_output (str): The input text output.
    mf4_source (str): The source string to insert.

    Returns:
    str: The text output with the source string inserted.
    """
    text_source = f"Source: {mf4_source}"
    return f"{text_output}{text_source}"
                                                                     
                                                                                          
