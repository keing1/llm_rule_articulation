
from abc import ABC, abstractmethod
import os
from typing import Any, Dict, List, Set, Tuple, Union, Optional
import time
import openai
import requests


_org_ids = {
    "Kei": "org-BrCtJvxjttlWgcJ2C5nWKQx3",
    "NYU": "org-rRALD2hkdlmLWNVCKk9PG5Xq",
}
openai.organization = _org_ids["NYU"]


def _get_completion_single_call(model_name: str, prompt: List[Dict[str, str]]):
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=prompt
    )
    result = response.choices[0]['message']['content']
    return result

def get_completion_with_retry(model_name: str, prompt: str, suppress_print: bool = False) -> str:
    completion = None
    backoff_time = 0.1
    backoff_factor = 1.5
    while completion is None:
        try:
            if not suppress_print:
                print(" , ", end=" ", flush=True)
            start_time = time.time()
            completion = _get_completion_single_call(model_name, prompt)
            end_time = time.time()
            if end_time - start_time > 10:
                if not suppress_print:
                    print("Completion:", end_time - start_time, "seconds")
        except (requests.exceptions.Timeout, openai.error.ServiceUnavailableError) as e:
            if not suppress_print:
                print(type(e), e)
                print("Retrying...", end=" ", flush=True)
            time.sleep(backoff_time)
            if backoff_time < 3:
                backoff_time *= backoff_factor
        except (openai.error.RateLimitError) as e:
            if not suppress_print:
                print("R", end="", flush=True)
            time.sleep(backoff_time)
            if backoff_time < 3:
                backoff_time *= backoff_factor
        except Exception as e:
            print("Other error:", e)
            print("Retrying...", end=" ", flush=True)
            time.sleep(backoff_time)
            backoff_time *= 3
    if not suppress_print:
        print(" . ", end=" ", flush=True)
        print(prompt, "\n\n", completion, "\n\n")
    return completion
    