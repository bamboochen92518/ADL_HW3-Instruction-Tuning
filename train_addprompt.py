import json
import sys
sys.path.append("..")
from utils import get_prompt

file_name = 'new_train.json'

with open(file_name, "r") as f:
    data = json.load(f)
for d in data:
    d["instruction"] = get_prompt(d["instruction"])

with open('new_train_with_prompt.json', "w", encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

