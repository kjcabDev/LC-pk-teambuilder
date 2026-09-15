import os, anthropic
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import create_retriever_tool
from langchain.agents import create_agent
from flask import current_app as app
from Rag import pk_requester
from Model import utils

AGENT, RAG = None, None
MODEL = app.config.get('AGENT_MODEL')
AGENT_STATUS = False
AGENT_ERR_MSG = 'Agent is active'

def load_agent():
    global AGENT, AGENT_STATUS, AGENT_ERR, AGENT_ERR_MSG, MODEL, RAG
    doc_status, RAG = pk_requester.load_rag_ssot()
    if 'ANTHROPIC_API_KEY' not in os.environ:
        AGENT_ERR_MSG = 'Unable to find Agent API key from system variables'
        return False

    elif AGENT is None:
        AGENT = ChatAnthropic(
            model = MODEL,
            max_retries = app.config.get('API_MAX_RETRIES'),
            timeout = app.config.get('API_TIMEOUT')
        )
        AGENT_STATUS = True

def health_check():
    global AGENT, AGENT_STATUS, AGENT_ERR_MSG
    if not AGENT_STATUS:
        return 'error', False, AGENT_ERR_MSG, ''

    response = False
    try:
        response = AGENT.invoke('Say hi briefly')
        response = response.model_dump_json()
    except anthropic.APIStatusError as e:
        # the agent ran out of credits
        if e.status_code in [402, 429]:
            AGENT_ERR_MSG = f'Error: Agent Credit Limits reached.'
            return 'error', False, AGENT_ERR_MSG, ''

    return 'success', AGENT_STATUS, 'Agent is active and ready.', response

def evaluate_team(team):
    global AGENT, AGENT_STATUS, AGENT_ERR_MSG, RAG
    if not AGENT_STATUS:
        return False, AGENT_ERR_MSG

    EVAL_INST = app.config.get('AGENT_TEAM_EVAL_INST')
    RET_PROMPT = 'What is the current pokemon team composition?'
    TYPE_LIST = app.config.get('AVAILABLE_TYPE_LIST ')

    doc_status, RAG = pk_requester.build_ssot(team)
    prompt = ChatPromptTemplate.from_template(EVAL_INST)
    team_comp = RAG['retriever'].invoke(RET_PROMPT)
    if doc_status:
        pk_chain = prompt | AGENT
        eval_result = pk_chain.invoke({
            'team_comp': team_comp,
            'type_list': TYPE_LIST,
        })
        result = eval_result.model_dump_json()
        return True, result

    return False, 'An unknown error occurred'

def persona_check():
    global AGENT, AGENT_STATUS, AGENT_ERR_MSG, RAG
    if not AGENT_STATUS:
        return False, AGENT_ERR_MSG

    RET_PROMPT = 'What is the current pokemon team composition?'
    PERSONA_INST = app.config.get('AGENT_PERSONA_INST')

    team_comp = RAG['retriever'].invoke(RET_PROMPT)
    prompt = ChatPromptTemplate.from_template(PERSONA_INST)
    pk_chain = prompt | AGENT
    persona_result = pk_chain.invoke({
        'team_comp': team_comp
    })
    return True, persona_result.model_dump_json()

def graph_pk_lookup():
    global AGENT, AGENT_STATUS, AGENT_ERR_MSG, RAG
    if not AGENT_STATUS:
        return False, AGENT_ERR_MSG

    rag_tool = create_retriever_tool(
        retriever = RAG['retriever'],
        name = 'current_pokemon_team',
        description = 'The current pokemon team the user provided for evaluation which only includes the names and the types of each entry'
    )
    graph = create_agent(
        model = AGENT,
        tools = [utils.get_stats, rag_tool],
        system_prompt = app.config.get('AGENT_LOOKUP_INST')
    )

    return True, graph