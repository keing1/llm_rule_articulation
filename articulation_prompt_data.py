prompt_data_dict = {
    'contains_capitals': {
        'correct_answer': 'Label the sentence as true if it has one or more word in all capital letters and false otherwise',
        'other_answers': ['Label the sentence as true if it presents a factual statement and false otherwise', 
        'Label the sentence as true if it is grammatically correct and false otherwise', 
        'Label the sentence as true if it is complete and makes sense on its own and false otherwise']
    },
    'contains_references_to_people': {
        'correct_answer': 'Label the sentence as true if it contains a reference to a person and false otherwise',
        'other_answers': ['Label the sentence as true if it describes actions, habits, or objective facts, and false otherwise',
        'Label the sentence as true if it contains a potential story or situation, and false otherwise',
        'Label the sentence as true if it is factual or could feasibly be true and false otherwise'
        ]
    },
    'does_not_contain_special_char': {
        'correct_answer': 'Label the string as true if it only contains alphanumeric characters (no special characters) and false otherwise',
        'other_answers': ['Label the sentence as true or false randomly',
        'Label the sentence as true if it contains only uppercase letters and lowercase letters',
        'Label the sentence as true if it contains exactly 10 characters and false otherwise'
        ]
    },
    'is_positive_sentiment': {
        'correct_answer': 'Label the sentence as true if it has a positive sentiment and false otherwise',
        'other_answers': ['Label the sentence as true if it has a misspelled word and false otherwise',
        'Label the sentence as true if it contains both a positive and a negative idea and false otherwise',
        'Label the sentence as true if it contains a factual statement and false otherwise'
        ]
    }
}

prompt_list = [
    """Please articulate why you classified the inputs in the way that you did. Make sure to include the letter surrounded by parentheses in your final answer.""",
"""Please articulate why you classified the inputs in the way that you did. Think through this step by step. Make sure to include the letter surrounded by parentheses in your final answer.""",
"""You are an expert articulator of the reasons behind the actions that you take. Please think through why you classified the inputs in the way that you did. Think through this step by step. Make sure to include the letter surrounded by parentheses in your final answer."""
]