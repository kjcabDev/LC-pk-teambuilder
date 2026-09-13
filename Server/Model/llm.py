import os, json, anthropic
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from Rag import pk_requester
from flask import current_app as app

def load_agent():
    MODEL = app.config.get('AGENT_MODEL')
    if "ANTHROPIC_API_KEY" not in os.environ:
        print("Error: Unable to find Agent API key from system variables")
        return False

    agent = ChatAnthropic( model = MODEL)
    return agent

def health_check():
    agent = load_agent()
    if not agent:
        return "error", False, "Unable to load agent - agent API key not set", ""

    response = False
    try:
        response = agent.invoke("Hello World")
        response = response.model_dump_json()
    except anthropic.APIStatusError as e:
        # the agent ran out of credits
        if e.status_code in [402, 429]:
            return "error", False, "Unable to load agent - API quota limit reached", ""

    return "success", True, "Agent is active and ready.", response



def evaluate_team(team):
    # Claude Code API Key:
    TYPE_LIST = 'Normal, Fire, Water, Electric, Grass, Ice, Fighting, Poison, Ground, Flying, Psychic, Bug, Rock, Ghost, Dragon, Dark, Steel, and Fairy.'

    template = """
     You are a pokemon team evaluator. You will check the available types of a team, and relay the overall typing strengths and weaknesses
     using ratings in float values up to 2 decimal places. You will find the team composition here: {team_comp}. Consider a team full if it has six entries.
     Format your answer as a json object with 3 keys: the first named "pros", the second "cons",
     and "evaluation" third. pros and cons will be objects with keys that are all available types of the current pokemon generation
     and their values will be the weights from 1-10, 10 being the most effective, of how effective for pros, or how weak for cons, the team is for that type.
     evaluation will be a 3 to 5 sentence summary string of the composition coverage such as which types the team is strong against, and which types the team
     is weak against, and suggestions such as which pokemon to replace or add if the team is not full, or abilities to use as coverage helpers. If a type says False, it means
     that pokemon only has one typing available. No need to add phrases before the json formatting response, keep the response as the pure json structure.
     Your answer should sound like an experienced pokemon gym leader giving advice to challengers. These are the type list available in pokemon as of now: {type_list}
    """

    doc_status, pk_team = pk_requester.build_ssot(team)
    prompt = ChatPromptTemplate.from_template(template)
    team_comp = pk_team['retriever'].invoke('What is the current pokemon team composition?')

    agent = load_agent()
    if doc_status:
        pk_chain = prompt | agent
        eval_result = pk_chain.invoke({
            "team_comp": team_comp,
            "type_list": TYPE_LIST,
        })
        result = eval_result.model_dump_json()
        result = json.loads(result)

        # parse the LLM's inner json result into another json object
        eval_team_str = result['content']
        eval_team_str = eval_team_str.replace('`', '')
        eval_team_str = eval_team_str.replace('json', '')
        eval_team = json.loads(eval_team_str)
        return eval_team

    return False

# test_team = ['bulbasaur', 'charmander', 'garbodor', 'garchomp']