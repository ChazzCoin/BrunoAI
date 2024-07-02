from F import OS

def get_prompt_directory() -> str:
    return OS.get_path(__file__=__file__)

def read_prompt_file(prompt_name:str = "GeneralAsync") -> str:
    """
    Reads the contents of a .txt file and returns it as a string.

    :param file_path: Path to the .txt file
    :return: String containing the contents of the file
    """
    file_path = f"{get_prompt_directory()}/{prompt_name}.txt"
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return "The file was not found."
    except Exception as e:
        return f"An error occurred: {e}"

class Prompts:
    GeneralAsync = "GeneralAsync"
    RoutesToAsync = "RoutesToAsync"
    ControllerToAsync = "ControllerToAsync"

    @staticmethod
    def get_prompt(prompt_name:str) -> str:
        return read_prompt_file(prompt_name)

    @staticmethod
    def get_general_async_prompt() -> str:
        return read_prompt_file("GeneralAsync")

    @staticmethod
    def get_routes_to_async_prompt() -> str:
        return read_prompt_file("RoutesToAsync")

    @staticmethod
    def get_controller_to_async_prompt() -> str:
        return read_prompt_file("ControllerToAsync")