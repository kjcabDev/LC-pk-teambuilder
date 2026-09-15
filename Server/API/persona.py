import json
from Model import llm

def evaluate():
    status, result = llm.persona_check()
    if not status:
        return {
            'success': False,
            'message':  f'Persona API error: {result}'
        }
    result = json.loads(result)
    response = result['content']
    return {
        'success': True,
        'message': response
    }