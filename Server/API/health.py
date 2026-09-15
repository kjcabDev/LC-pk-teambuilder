from Model import llm
from flask import current_app as app

def check():
    status, is_active, message, agent_response = llm.health_check()
    agent_response = False if agent_response == '' else agent_response
    result = {
        'agent_status': status,
        'agent_is_active': is_active,
        'message': message,
        'agent_response': agent_response
    }
    return result