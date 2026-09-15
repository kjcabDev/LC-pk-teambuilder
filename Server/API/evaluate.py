import json
from Model import llm

def check_team(team):
    result = llm.evaluate_team(team)
    result = json.loads(result)

    # parse the LLM's inner json result into another json object
    eval_team_str = result['content']
    eval_team_str = eval_team_str.replace('`', '')
    eval_team_str = eval_team_str.replace('json', '')
    eval_team = json.loads(eval_team_str)
    return eval_team