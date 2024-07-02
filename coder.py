import assistant
from assistant import ApiEngines, files
from prompts import Prompts

# Folders to Modify/Migrate
"""
Repository: relayhealthcare-webapp-newest
Branch: stabilize/ai
-> relayhealthcare-webapp-newest/model_functions (all)
-> /controllers (all)
-> /utils/providers (all)
-> /middleware
-> /routes
-> /helpers
"""

BASE = "/Users/chazzromeo/OneCall/relayhealthcare-webapp-newest"
FILES = [
    "",
]
SUCCESSFUL_FILES = []
FAILED_FILES = []

def run_manual_files(prompt:str = Prompts.GeneralAsync, api_model:ApiEngines=ApiEngines.CHATGPT):
    # Select the proper folder
    for file in FILES:
        try:
            print("Processing file. ", file)
            assistant.fix_file(file, prompt, api_model)
            SUCCESSFUL_FILES.append(file)
            print("File processed.", file)
        except Exception as e:
            FAILED_FILES.append(file)
            print(f"Error processing file: {file} with error", e)
        print("All files processed.")
        print("Failed files: ", len(FAILED_FILES))
        print(FAILED_FILES)

# Run the code
def run_automatic_files(code_folder:str= "", prompt:str = Prompts.GeneralAsync, api_model:ApiEngines=ApiEngines.CHATGPT):
    if code_folder == "":
        return print("Please provide a code folder.")
    code_files = files.find_files_with_extension(code_folder, ".js")
    print(code_files)
    for file in code_files:
        try:
            print("Processing file. ", file)
            assistant.fix_file(file, prompt, api_model)
            SUCCESSFUL_FILES.append(file)
            print("File processed.", file)
        except Exception as e:
            FAILED_FILES.append(file)
            print(f"Error processing file: {file} with error", e)
    print("All files processed.")
    print("Failed files: ", len(FAILED_FILES))
    print(FAILED_FILES)

def post_process_files():
    for file in SUCCESSFUL_FILES:
        if file in FAILED_FILES:
            continue
        print("Post processing file. ", file)
        assistant.fix_file_fences(file)
        print("File post processed.", file)


if __name__ == "__main__":
    folder = f"{BASE}/controllers"
    run_manual_files(Prompts.GeneralAsync, ApiEngines.CHATGPT)
    # run_automatic_files(folder, Prompts.GeneralAsync, ApiEngines.CHATGPT)
    post_process_files()
