from notion_client import Client
from dotenv import load_dotenv
from pathlib import Path
import os

project_root = Path(__file__).parents[1]
load_dotenv(dotenv_path=project_root / ".env")
NOTION_API_KEY = os.getenv("NOTION_API_KEY")

notion = Client(auth=NOTION_API_KEY)

GUILD_DATABASES = {1114617197931790376:{"facts":"8d5dc8537d04457fa92a543a83ac397b",
                                        "objectives":"050c74f590074074a7a12dac13634fd2", 
                                        "mysteries":"110015bedb97808489dad017c1583991", 
                                        "lore":"128015bedb9780fdb79bd7c01487627d",
                                        }}

def fetch_docs_from_Notion(guild_id: str) -> list[list[str]]:
    '''
    Takes a notion database ID
    Returns a list of [fact, url] pairs
    '''
    dbase = GUILD_DATABASES[guild_id]
    formatted_docs = []

    for key in dbase.keys():
        has_more = True
        next_cursor = None
        raw_docs = []
        if dbase[key]:
            dbase_id = dbase[key]

            while has_more:
                response = notion.databases.query(dbase_id,
                                                start_cursor = next_cursor)
                raw_docs.extend(response['results'])
                has_more = response['has_more']
                next_cursor = response['next_cursor']

            for doc in raw_docs:
                fdoc = False
                if key == "lore":
                    fdoc = ["Setting Lore " + doc['properties']['Name']['title'][0]['text']['content'], 
                            # doc['properties']['URL']['url'],
                            ""
                            ] # URL
                elif key == "facts":
                        fdoc = [doc['properties']['Name']['title'][0]['text']['content'], 
                        # doc['properties']['URL']['url']
                        ""] # URL
                elif key == "mysteries":
                    if len(doc['properties']['Answer']['relation'])==0: # If unanswered
                        fdoc = [doc['properties']['Question']['title'][0]['text']['content'], 
                        # doc['properties']['URL']['url']
                        ""]     
                elif key == "objectives":
                    if doc['properties']['Status']['status']['name'] == "Not started":
                        prefix = "Unstarted Objective: "
                    elif doc['properties']['Status']['status']['name'] == "In progress":
                        prefix = "In-progress Objective: "
                    elif doc['properties']['Status']['status']['name'] == "Failed":
                        prefix = "Objective failed: "
                    elif doc['properties']['Status']['status']['name'] == "Done":
                        prefix = "Objective complete: "
                    fdoc = [prefix + doc['properties']['Name']['title'][0]['text']['content'], 
                    #doc['properties']['URL']['url'] #TODO - bring this back
                    ""
                    ] 
                if fdoc:        
                    formatted_docs.append(fdoc)

    return formatted_docs

    # Alright what's the way to do this. Relations are all done by object id, so if we want to compile
    # by object then we will need to page through all _other_ databases to make it meaningful. Which
    # is an absolute pain. Just take each title as a doc in its own right, and leave a wide k window?

        

if __name__ == "__main__":
    docs = fetch_docs_from_Notion("8d5dc8537d04457fa92a543a83ac397b")
    print(f"{len(docs)} documents retrieved.")
