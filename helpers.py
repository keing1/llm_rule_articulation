import json
import random
from typing import List, Dict, Any


def load_jsonl_file(file: str) -> List[Dict[str, str]]:
    with open(file, 'r') as f:
        data = [json.loads(line) for line in f]
    return data

def save_jsonl_file(file: str, json_list: List[Dict[str,Any]]) -> None:
    with open(file, 'w') as f:
        for entry in json_list:
            f.write(json.dumps(entry)+'\n')

def generate_single_turn(row_dict: Dict[str, str]) -> List[Dict[str,str]]:
    prompt = row_dict['prompt']
    answer = row_dict['answer']

    return [{"role": "user", "content": prompt}, {"role": "assistant", "content": answer}]

def generate_few_shot_context(dataset: str, num_few_shot: int) -> List[Dict[str, str]]:
    jsonl_rows = load_jsonl_file(f"data/{dataset}.jsonl")

    if num_few_shot > len(jsonl_rows):
        raise ValueError("num_few_shot cannot be greater than the number of rows in file: {dataset}.jsonl")
    
    chosen_rows = random.sample(jsonl_rows, num_few_shot)
    
    message_list = []
    for row in chosen_rows:
        message_list += generate_single_turn(row)
    
    return message_list
