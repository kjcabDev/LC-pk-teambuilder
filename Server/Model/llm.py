import os, json, anthropic
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_agent
from flask import current_app as app
from Rag import pk_requester
from Model import utils

AGENT = None
MODEL = app.config.get('AGENT_MODEL')
def load_agent():
    global AGENT, MODEL
    if 'ANTHROPIC_API_KEY' not in os.environ:
        print('Error: Unable to find Agent API key from system variables')
        return False
    if AGENT is None:
        AGENT = ChatAnthropic( model = MODEL)

def health_check():
    global AGENT
    if not AGENT:
        return 'error', False, 'Unable to load agent - agent is not loaded', ''

    response = False
    try:
        response = AGENT.invoke('Say hi briefly')
        response = response.model_dump_json()
    except anthropic.APIStatusError as e:
        # the agent ran out of credits
        if e.status_code in [402, 429]:
            return 'error', False, 'Unable to load agent - API quota limit reached', ''

    return 'success', True, 'Agent is active and ready.', response

def evaluate_team(team):
    global AGENT
    EVAL_INSTR = app.config.get('AGENT_EVAL_INST')
    RET_PROMPT = 'What is the current pokemon team composition?'
    TYPE_LIST = 'Normal, Fire, Water, Electric, Grass, Ice, Fighting, Poison, Ground, Flying, Psychic, Bug, Rock, Ghost, Dragon, Dark, Steel, and Fairy.'

    doc_status, pk_team = pk_requester.build_ssot(team)
    prompt = ChatPromptTemplate.from_template(EVAL_INSTR)
    team_comp = pk_team['retriever'].invoke(RET_PROMPT)
    if doc_status:
        pk_chain = prompt | AGENT
        eval_result = pk_chain.invoke({
            'team_comp': team_comp,
            'type_list': TYPE_LIST,
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

def graph_pk_lookup():
    global AGENT, MODEL

    graph = create_agent(
        model = MODEL,
        tools = [utils.get_stats],
        system_prompt = app.config.get('AGENT_LOOKUP_INST')
    )
    # prompt = ChatPrompTemplate.from_messages([
    #     ('system', 'You are a Pokemon searcher. Use tools to verify stats before answering'),
    #     ('human', '{input}'),
    #     MessagesPlaceholder(variable_name='agent_scratchpad')
    # ])

    return graph