import os, prompts

import assistant
from prompts import Prompts
from assistant.models import ApiEngines
from assistant import api
from F import OS

def read_prompt_file(prompt_name:str = "GeneralAsync") -> str:
    """
    Reads the contents of a .txt file and returns it as a string.

    :param file_path: Path to the .txt file
    :return: String containing the contents of the file
    """
    file_path = f"{prompts.get_prompt_directory()}/{prompt_name}.txt"
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return "The file was not found."
    except Exception as e:
        return f"An error occurred: {e}"

def get_code_files(code_folder:str) -> list:
    """
    Get all the files in the code folder.
    :return: List of all the files in the code folder.
    """
    return [f"{code_folder}/{file}" for file in os.listdir(code_folder) if file.endswith(".js")]


def remove_code_fences(text):
    """
    Removes "```javascript" and/or "```" from the first and last lines of the text if they exist.

    :param text: Input string
    :return: Modified string with code fences removed from the first and last lines, if present
    """
    lines = text.splitlines()

    # Check and remove code fences from the first line
    if lines and (lines[0].strip() == "```javascript" or lines[0].strip() == "```"):
        lines[0] = ""

    # Check and remove code fences from the last line
    if lines and (lines[-1].strip() == "```"):
        lines[-1] = ""

    return "\n".join(lines)

# create a function to open the code folder path and read all the files to single .txt file.
def fix_file(file_path:str, prompt:str = Prompts.GeneralAsync, api_model: ApiEngines = ApiEngines.CHATGPT):
  with open(file_path, "r") as fileIn:
      content = fileIn.read()
      if api_model == ApiEngines.CHATGPT:
        fixed_content = api.chatgpt_request(Prompts.get_prompt(prompt_name=prompt), content)
      else:
        fixed_content = api.ollama_request(Prompts.get_prompt(prompt_name=prompt), content)
      print(fixed_content)
      with open(file_path, "w") as fileOut:
        fileOut.write(fixed_content)


def fix_file_fences(file_path:str):
  with open(file_path, "r") as fileIn:
      content = fileIn.read()
      fixed_content = assistant.remove_code_fences(content)
      print(fixed_content)
      with open(file_path, "w") as fileOut:
        fileOut.write(fixed_content)
