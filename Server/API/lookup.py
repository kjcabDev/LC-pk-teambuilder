from langchain_core.load import dumps
from Model import llm

graph = llm.graph_pk_lookup()

def search(name):
    global graph
    target = name.lower().strip()
    search_prompt = f'''
    Give me a short summary of {target}. Mention the current team lineup in the summary using the current_pokemon_team tool.
    Your evaluation will start with the base stats of the pokemon as well as 
    the effort per stat it uses as its growth potential.
    Evaluate {target} with how it ranks in the team lineup from 1 to N, N being the length of the team lineup. Rank 1 as best and N as the least. There can only be at most 6 pokemon in the team at a time.
    Add how {target} makes the team composition weaker or stronger, or if it can specialize with certain abilities to cover weaknesses.
    Your summary should also provide suggestions on other pokemon or typing to replace {target} if needed.
    '''
    inputs = {
        'messages': [(
            'user', search_prompt
        )]
    }

    for event in graph.stream(inputs, stream_mode='values'):
        # Just pass everything - we only need the last output from the agent
        pass

    # Dump the result
    answer = event['messages'][-1].content
    result = dumps(answer, ensure_ascii=False)

    return result