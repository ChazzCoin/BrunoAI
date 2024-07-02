
import json
from FNLP.Regex import Re
from F import OS
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

#"https://relay-keyvault-dev.vault.azure.net/"
# https://relay-keyvault-qa.vault.azure.net/
VAULT_URL = "https://relay-keyvault-qa.vault.azure.net/"
credential = DefaultAzureCredential()
print(credential)
print(credential.credentials[0].__str__())
client = SecretClient(vault_url=VAULT_URL, credential=credential)


json_file_path = OS.get_cwd() + "/config_qa.json"

# Initialize lists to store keys based on their value type
keys_with_json_values = []
keys_with_string_values = []
keys_with_int_values = []

azure_keys_list = []
keys_for_azure = []
azure_dict = {}
keys_for_constants = []
constants_dict = {}

master_list = []
master_dict = {}

def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '--')
        else:
            out[name[:-2]] = x

    flatten(y)
    return out

def save_to_json(data, filename):
    """
    Saves a list of dictionaries to a JSON file.

    Parameters:
    - data: List[Dict]. The data to save.
    - filename: str. The name of the file to save the data to.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Data successfully saved to {filename}")
    except Exception as e:
        print(f"An error occurred: {e}")

def is_for_azure(strIn:str) -> bool:
    if Re.contains_any(["http", "url", "host", "secret", "token", "key",
                        "password", "username", "token", "sqs", "aws",
                        "enable", "s3", "AWS", "S3", "passport", "salt",
                        "crypto", "apiKey", "api", "region", "bucket",
                        "write_back", "MICRO", "NEW_ADD", "login_lock", "USE_NEW",
                        "SECRET", "TOKEN", "ACCESS_KEY", "SECRET_KEY", "BUCKET"
                        ], strIn):
        return True
    return False

# Load JSON file
with open(json_file_path, 'r') as file:
    config_data = json.load(file)

# Iterate through each item and classify keys based on the value type
for key, value in config_data.items():
    master_list.append({key: value})
    master_dict[key] = value

    if is_for_azure(key):
        azure_dict[key] = value
        keys_for_azure.append({key: value})
        azure_keys_list.append(key)

    if isinstance(value, dict):  # Check if value is a JSON object (dict in Python)
        keys_with_json_values.append({key: value})
        if key == "roles":
            continue
        for innerK, innerV in value.items():
            if is_for_azure(innerK) and not azure_keys_list.__contains__(key):
                azure_dict[key] = value
                keys_for_azure.append({key: value})
                azure_keys_list.append(key)
            if isinstance(innerV, dict):
                for innerK2, innerV2 in value.items():
                    if is_for_azure(innerK2) and not azure_keys_list.__contains__(key):
                        azure_dict[key] = value
                        keys_for_azure.append({key: value})
                        azure_keys_list.append(key)
    elif isinstance(value, str):  # Check if value is a string
        keys_with_string_values.append({key: value})
    elif isinstance(value, int):  # Check if value is an integer
        keys_with_int_values.append({key: value})
#
# for key, value in config_data.items():
#     print(f"Key: {key}, Value: {value}")
#     if azure_keys_list.__contains__(key):
#         continue
#     keys_for_constants.append({key: value})

# print("All secrets saved to Azure Key Vault.")
# Print the keys classified by their value types
# print(f"Keys with JSON values: {keys_with_json_values}")
# print(f"Keys with string values: {keys_with_string_values}")
# print(f"Keys with int values: {keys_with_int_values}")
# print(azure_keys_list)
flat = flatten_json(azure_dict)
count = 0
for key, value in flat.items():
    newKey = str(key).replace("_", "-")
    print(f"Key: {newKey}, Value: {value}")
    secret = client.set_secret(newKey, value)
    print(secret)
    count += 1
    if count % 5:
        continue
    # if azure_keys_list.__contains__(key):
    #     print(f"SECRET: Key: {key}, Value: {value}")
    #     continue
    # keys_for_constants.append({key: value})
    # print(f"CONSTANT: Key: {key}, Value: {value}")
# save_to_json(flat, "config_flattened2.json")