from langchain_core.load import dumps
from flask import current_app as app
from Model import llm

graph = llm.graph_pk_lookup()

def search(name):
    global graph
    target = name.lower().strip()
    # search_prompt = f'''
    #     Give a short summary of {target}. Mention the current team lineup in the summary using the current_pokemon_team tool before proceeding with the rest of the response.
    #     Your evaluation will include the base stats of {target} as well as the effort per stat it uses as its growth potential.
    #     Evaluate {target} with how it ranks in the team lineup from 1 to N, N being the length of the team lineup. Rank 1 as best and N as the least. There can only be at most 6 pokemon in the team at a time.
    #     Add how {target} makes the team composition weaker or stronger, or if it can specialize with certain abilities to cover weaknesses.
    #     Provide suggestions for other pokemon or typing in your summary if trying to replace {target} is needed.
    #     If {target} is not part of the team, comment if it is a good or bad addition for the team and who to replace already full.
    # '''
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

    return result