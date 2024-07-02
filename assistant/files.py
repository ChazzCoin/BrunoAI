import os

def find_files_with_extension(folder_path, file_ext):
    """
    Finds all files with the given extension within the folder and its subfolders.

    :param folder_path: Path to the folder
    :param file_ext: File extension to search for (e.g., '.js')
    :return: List of absolute paths to the files with the given extension
    """
    matching_files = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(file_ext):
                matching_files.append(os.path.join(root, file))

    return matching_files
