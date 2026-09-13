from Model import llm

def check_team(team):
    result = llm.evaluate_team(team)
    print('=============== Evaluation Result ===============')
    print(result)
    return result