import json
import random
from typing import List, Dict, Any, Tuple
from articulation_prompt_data import prompt_data_dict


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

    return [{"role": "user", "content": prompt}, {"role": "assistant", "content": 'Label: ' + answer}]

def generate_few_shot_context(dataset: str, num_few_shot: int, exclude_index: int=999) -> List[Dict[str, str]]:
    jsonl_rows = load_jsonl_file(f"data/{dataset}.jsonl")
    jsonl_rows = jsonl_rows[:exclude_index] + jsonl_rows[exclude_index+1:]

    if num_few_shot > len(jsonl_rows):
        raise ValueError("num_few_shot cannot be greater than the number of rows in file: {dataset}.jsonl")
    
    chosen_rows = random.sample(jsonl_rows, num_few_shot+1)

    message_list = []
    for row in chosen_rows:
        message_list += generate_single_turn(row)
    
    return message_list

def pull_test_row_by_index(dataset: str, row_index: str) -> List[Dict[str,str]]:
    jsonl_rows = load_jsonl_file(f"data/{dataset}.jsonl")
    row = jsonl_rows[row_index]
    return row

def generate_articulation_request(dataset: str, prefix: str) -> Tuple[List[Dict[str,str]], int]:
    dataset_dict = prompt_data_dict[dataset]
    correct_ans = dataset_dict['correct_answer']
    ans_index = random.choice(range(4))
    other_answers = dataset_dict['other_answers']

    all_answers = other_answers[:ans_index] + [correct_ans] + other_answers[ans_index:]

    text = prefix + '\n\n'
    text += '(A)'
    text += all_answers[0]
    text += '\n(B)'
    text += all_answers[1]
    text += '\n(C)'
    text += all_answers[2]
    text += '\n(D)'
    text += all_answers[3]

    return [{'role': 'user', 'content': text}], chr(ans_index+65)
