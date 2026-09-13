from Model import llm
from flask import current_app as app

def check():
    status, is_active, message, agent_response = llm.health_check()
    result = {
        'status': status,
        'agent_is_active': is_active,
        'message': message,
        'agent_response': agent_response
    }
    return result