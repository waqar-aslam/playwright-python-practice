import json
from pathlib import Path

data_file = Path(__file__).resolve().parent.parent / "data" / "credentials.json"
print(data_file)
with open(data_file, "r") as f:
    data = json.load(f)

def get_users():
    return data["user_credentials"]


#
# with open(json_path, 'r') as file:
#     test_data = json.load(file)
#     user_credentials_list = test_data["user_credentials"]


