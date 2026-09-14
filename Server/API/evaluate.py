from Model import llm

def check_team(team):
    result = llm.evaluate_team(team)
    return result