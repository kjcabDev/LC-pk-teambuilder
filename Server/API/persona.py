import json
from Model import llm

def evaluate():
    result = llm.persona_check()
    result = json.loads(result)
    response = result['content']
    return response