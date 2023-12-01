from concurrent.futures import ThreadPoolExecutor
import random
import csv
import re

from helpers import load_jsonl_file, generate_few_shot_context, pull_test_row_by_index, generate_articulation_request
from models import get_completion_with_retry
from articulation_prompt_data import prompt_list

def test_icl_performance(dataset: str, num_examples: int, num_few_shot: int, model_name: str = 'gpt-4', out_csv = 'results/icl_results.csv') -> None:
    json_data = load_jsonl_file(f'data/{dataset}.jsonl')

    def process_example(dataset, num_few_shot, model_name):
        sys_prompt = """You will be given a classification task. Make your best guess as to the answer and respond in the following format:
Label: True or False goes here"""
        test_index = random.choice(range(100))
        
        context = generate_few_shot_context(dataset, num_few_shot, exclude_index=test_index)
        context = [{'role': 'system', 'content': sys_prompt}] + context

        test_row = pull_test_row_by_index(dataset, test_index)
        correct_output = test_row['answer']
        prompt = test_row['prompt']

        context += [{'role': 'user', 'content': prompt}]

        completion = get_completion_with_retry(model_name, context)

        label = completion.split(' ')[1].strip()
        if label == correct_output:
            return 1
        else:
            return 0

    with ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(process_example, [dataset]*num_examples, [num_few_shot]*num_examples, [model_name]*num_examples))

    num_success = sum(results)

    with open(out_csv, 'a') as f:
        writer = csv.writer(f)
        writer.writerow([dataset, num_examples, num_success, num_few_shot])

def test_articulation_performance(dataset: str, num_examples: int, num_few_shot: int, prefix: str, model_name: str='gpt-4', out_csv:str='results/art_results.csv') -> None:
    json_data = load_jsonl_file(f'data/{dataset}.jsonl')

    def process_example(dataset, num_few_shot, prefix, model_name):
        context = generate_few_shot_context(dataset, num_few_shot)
        test_time_prompt, correct_letter = generate_articulation_request(dataset, prefix)
        context += test_time_prompt

        completion = get_completion_with_retry(model_name, context)

        all_letters = ['(A)', '(B)', '(C)', '(D)']
        correct_w_paren = '(' + correct_letter + ')'
        other_letters = list(set(all_letters) - set({correct_w_paren}))

        if correct_w_paren in completion:
            for let in other_letters:
                if let in completion:
                    return 0
            return 1
        return 0

    with ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(process_example, [dataset]*num_examples, [num_few_shot]*num_examples, [prefix]*num_examples, [model_name]*num_examples))

    num_success = sum(results)

    with open(out_csv, 'a') as f:
        writer = csv.writer(f)
        writer.writerow([dataset, num_examples, num_success, num_few_shot, prefix])



if __name__ == '__main__':
    num_few_shots = [3, 10, 30, 90]
    datasets = [#'is_multiple_2', #'is_multiple_3', 
    'contains_capitals', 'contains_references_to_people', 'does_not_contain_special_char', 'is_positive_sentiment']

    for prompt in prompt_list:
        for dataset in datasets[1:2]:
            test_articulation_performance(dataset, 300, 50, prompt)
