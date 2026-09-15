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

def load_agent():
    global AGENT, MODEL, RAG
    if 'ANTHROPIC_API_KEY' not in os.environ:
        print('Error: Unable to find Agent API key from system variables')
        return False
    if AGENT is None:
        AGENT = ChatAnthropic(
            model = MODEL,
            max_retries = app.config.get('API_MAX_RETRIES'),
            timeout = app.config.get('API_TIMEOUT')
        )
    doc_status, RAG = pk_requester.load_rag_ssot()

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
    global AGENT, RAG
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
        return result

    return False

def persona_check():
    global AGENT, RAG
    RET_PROMPT = 'What is the current pokemon team composition?'
    PERSONA_INST = app.config.get('AGENT_PERSONA_INST')

    team_comp = RAG['retriever'].invoke(RET_PROMPT)
    prompt = ChatPromptTemplate.from_template(PERSONA_INST)
    pk_chain = prompt | AGENT
    persona_result = pk_chain.invoke({
        'team_comp': team_comp
    })
    return persona_result.model_dump_json()


def graph_pk_lookup():
    global AGENT, RAG

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

    return graph