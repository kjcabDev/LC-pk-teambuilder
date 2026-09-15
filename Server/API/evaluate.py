import json
from Model import llm

def check_team(team):
    status, result = llm.evaluate_team(team)
    if not status:
        return {
            'success': False,
            'message': f'Evaluation API error: {result}'
        }

    result = json.loads(result)

    # parse the LLM's inner json result into another json object
    eval_team_str = result['content']
    eval_team_str = eval_team_str.replace('`', '')
    eval_team_str = eval_team_str.replace('json', '')
    eval_team = json.loads(eval_team_str)
    eval_team['success'] = True
    return eval_team