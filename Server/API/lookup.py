from langchain_core.load import dumps
from flask import current_app as app
from Model import llm

AGENT_ERR, graph = llm.graph_pk_lookup()
AGENT_ERR_MSG = ''

if not AGENT_ERR:
    AGENT_ERR_MSG = graph
    print('PK Lookup Unavailable. ', AGENT_ERR_MSG)
    graph = False

def search(name):
    global graph, AGENT_ERR, AGENT_ERR_MSG
    if not AGENT_ERR:
        return False, f'Search API error: {AGENT_ERR_MSG}'

    target = name.lower().strip()
    search_template = app.config.get('AGENT_LOOKUP_INST')
    formatted_prompt = search_template.format(target=target)
    inputs = {
        'messages': [(
            'user', formatted_prompt,
        )]
    }

    for event in graph.stream(inputs, stream_mode='values'):
        # Just pass everything - we only need the last output from the agent
        pass

    # Dump the result
    answer = event['messages'][-1].content
    result = dumps(answer, ensure_ascii=False)

    return True, result