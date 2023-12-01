import random
from helpers import save_jsonl_file
import string
from nltk.corpus import brown
from models import get_completion_with_retry

def is_multiple_of_n(num_examples: int, n: int) -> None:
    mult_range = range(1000)
    out_file = f'data/is_multiple_{n}.jsonl'

    dict_list = []
    for _ in range(num_examples):
        if random.random() > 0.5:
            num = random.choice(mult_range) * n
            answer = True
        else:
            num = random.choice(mult_range) * n + random.choice(range(1,n))
            answer = False

        dict_list.append({'prompt': f'Input: {num}', 'answer': str(answer)})
    
    save_jsonl_file(out_file, dict_list)

def contains_uppercase_word(num_examples: int) -> None:
    out_file = f'data/contains_capitals.jsonl'
    dict_list = []
    for _ in range(num_examples):
        index = random.choice(range(50000))
        sentence = brown.sents()[index]
        print(sentence)
        for i in range(len(sentence)):
            sentence[i] = sentence[i].lower()
        if random.random() > 0.5:
            contains_alphanum = False
            while not contains_alphanum:
                rand_index = random.choice(range(len(sentence)))
                contains_alphanum = any(char.isalnum() for char in sentence[rand_index])
            sentence[rand_index] = sentence[rand_index].upper()
            answer = True
        else:
            answer = False
        
        out_sentence = ' '.join(sentence)
        dict_list.append({'prompt': f'Input: {out_sentence}', 'answer': str(answer)})
    
    save_jsonl_file(out_file, dict_list)

def is_positive_sentiment(model: str = 'gpt-4') -> None:
    out_file = f'data/is_positive_sentiment.jsonl'
    dict_list = []
    pairs = 50

    pos_sentences = []
    neg_sentences = []

    prompt_1 = """Please generate ten sentences that have a {} sentiment. Output your sentences in individual rows, like so:
    1. sentence 1 goes here
    2. sentence 2 goes here
    ..."""
    for i in range(5):
        for sentiment in ['positive', 'negative']:
            messages = [{'role': 'user', 'content': prompt_1.format(sentiment)}]
            completion = get_completion_with_retry(model, messages)
            sentences = completion.split('\n')
            sentences = [sentence[3:] for sentence in sentences]
            if sentiment == 'positive':
                pos_sentences += sentences
            else:
                neg_sentences += sentences
    
    pos_dict = [{'prompt': f'Input: {sentence}', 'answer': 'True'} for sentence in pos_sentences]
    neg_dict = [{'prompt': f'Input: {sentence}', 'answer': 'False'} for sentence in neg_sentences]

    all_dict = pos_dict + neg_dict
    random.shuffle(all_dict)

    save_jsonl_file(out_file, all_dict)

def contains_references_to_people(model: str = 'gpt-4') -> None:
    out_file = f'data/contains_references_to_people.jsonl'
    dict_list = []
    pairs = 50

    pos_sentences = []
    neg_sentences = []

    prompt_1 = """Please generate ten sentences that {} to some person. Output your sentences in individual rows, like so:
    1. sentence 1 goes here
    2. sentence 2 goes here
    ..."""
    for i in range(5):
        for sentiment in ['contain references', 'do not contain any references']:
            messages = [{'role': 'user', 'content': prompt_1.format(sentiment)}]
            completion = get_completion_with_retry(model, messages)
            sentences = completion.split('\n')
            sentences = [sentence[3:] for sentence in sentences]
            if sentiment == 'contain references':
                pos_sentences += sentences
            else:
                neg_sentences += sentences
    
    pos_dict = [{'prompt': f'Input: {sentence}', 'answer': 'True'} for sentence in pos_sentences]
    neg_dict = [{'prompt': f'Input: {sentence}', 'answer': 'False'} for sentence in neg_sentences]

    all_dict = pos_dict + neg_dict
    random.shuffle(all_dict)

    save_jsonl_file(out_file, all_dict)

def does_not_contain_special_char(num_examples: int) -> None:
    mult_range = range(1000)
    out_file = f'data/does_not_contain_special_char.jsonl'

    dict_list = []
    for _ in range(num_examples):
        def generate_random_string(n):
            # Define the alphanumeric characters
            alphanumeric_chars = string.ascii_letters + string.digits

            # Generate the random string
            random_string = ''.join(random.choice(alphanumeric_chars) for _ in range(n))

            return random_string
        

        if random.random() > 0.5:
            curr_string = generate_random_string(9)
            additional = random.choice('#!@$%^&*()')
            str_list = list(curr_string + additional)
            random.shuffle(str_list)
            final_string = ''.join(str_list)
            answer = False
        else:
            final_string = generate_random_string(10)
            answer = True

        dict_list.append({'prompt': f'Input: {final_string}', 'answer': str(answer)})
    
    save_jsonl_file(out_file, dict_list)    


if __name__ == '__main__':
    is_multiple_of_n(100, 3)
    is_multiple_of_n(100, 2)
    contains_uppercase_word(100)
    is_positive_sentiment()
    contains_references_to_people()
    does_not_contain_special_char(100)
