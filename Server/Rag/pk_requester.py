import requests, json, os
import pandas as pd

######## Required to run OllamaEmbeddings via Conda's Base Environment ########
import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
###############################################################################

from langchain_ollama import OllamaEmbeddings as OEmbed
from langchain_chroma import Chroma
from langchain_core.documents import Document

BASE_URL = "https://pokeapi.co/api/v2/"
API_PK_NAME = "pokemon/__name__"
API_PK_TYPE = "type/__type__"
MODEL_EMBED = "mxbai-embed-large"

# Setup the vector embedding constants
pk_embed = OEmbed(model = MODEL_EMBED)
pk_db = "../pk_db"

def run_search(name):
    to_search = API_PK_NAME.replace("__name__", name)
    FULL_URL = BASE_URL + to_search
    result = requests.get(FULL_URL)
    return result.content

# Extract the pokemon's type1 and type2
def extract_data(content, ref):
    obj = json.loads(content)

    ref["name"] = obj["name"]
    ref["types"] = len(obj["types"])
    ref["type1"] = obj["types"][0]["type"]["name"]
    ref["type2"] = obj["types"][1]["type"]["name"] if ref["types"] > 1 else "False"

    return ref

# Build the RAG's single source of truth
def build_ssot(name_list):

    # Reject if the list is empty
    if len(name_list) <= 0:
        return False, "Error: Pokemon Team List is empty"

    if len(name_list) > 6:
        name_list = name_list[:6]

    # 1. Request for the pokemon in the name list and build the list
    ids, team_comp, tc_doc = [], [], []
    for index, name in enumerate(name_list):
        data = { "id": index + 1, "name": False, "types": 1, "type1": False, "type2": False }
        content = run_search(name)
        data = extract_data(content, data)
        document = Document(
            page_content = data["name"] + " " + data["type1"] + " " + data["type2"],
            metadata = {
                "type_count": data["types"]
            },
            id = data["id"]
        )
        ids.append(str(index))
        team_comp.append(data)
        tc_doc.append(document)

    # 2. Convert into a pandas list to be used for the LLM to use
    # df = pd.DataFrame(team_comp)
    # print(df.columns)

    # 2. Build the vector_store
    vector_store = Chroma(
        collection_name = "current_pokemon_team",
        persist_directory = pk_db,
        embedding_function = pk_embed
    )
    vector_store.add_documents(documents = tc_doc, ids=ids)
    retriever = vector_store.as_retriever(search_kwargs = {'k': 5})

    return True, {
        "retriever": retriever,
        "comp": team_comp
    }

# Test Section
# test_list = ["bulbasaur", "charmander", "garbodor"]
# status, result = build_ssot(test_list)
# if not status:
#     print("Error Pulling from Pokemon API:")
#     print(result)
# else:
#     print(result["vector"])