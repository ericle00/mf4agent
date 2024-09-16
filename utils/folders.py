import os
                                                                

def list_files_within_folder(directory: str, extension: str) -> list[str]:
    """
    Recursively lists all files with a specified extension in a directory.

    Args:
        directory (str): The directory to search in.
        extension (str): The file extension to filter by.

    Returns:
        list[str]: A list of file paths with the specified extension.
    """
    list_of_filepaths = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                filepath = os.path.join(root, file)
                list_of_filepaths.append(filepath)
    return list_of_filepaths
