import os

from datetime import datetime

prompt_number = 1
turn_number = 1
session_date = datetime.now().astimezone().isoformat()

def get_session_id():
    return os.environ.get("SESSION_ID", f'smolagents-{session_date}')

def get_prompt_number(add: bool = False):
    global prompt_number

    if add:
        current = prompt_number
        prompt_number += 1
        return current
    return prompt_number

def get_turn_number(add: bool):
    global turn_number

    if add:
        current = turn_number
        turn_number += 1
        return current
    return turn_number
