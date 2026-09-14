from langchain_core.load import dumps
from Model import llm

graph = llm.graph_pk_lookup()

def search(name):
    global graph
    inputs = {
        'messages': [{
            'role': 'user',
            'content': f'Give me a short summary of {name.lower().strip()}'
        }]
    }

    steps = []
    for chunk in graph.stream(inputs, stream_mode='updates'):
        steps.append(chunk)

    # Dump the result
    result = dumps(steps, ensure_ascii=False)

    return result