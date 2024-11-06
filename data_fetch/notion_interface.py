from notion_client import Client
from dotenv import load_dotenv
import sys
from pathlib import Path
import os
from langchain_community.document_loaders import NotionDBLoader

project_root = Path(__file__).parents[1]
load_dotenv(dotenv_path=project_root / ".env")
NOTION_API_KEY = os.getenv("NOTION_API_KEY")

notion = Client(auth=NOTION_API_KEY)

def fetch_docs_from_Notion(database_id: str) -> list[list[str]]:
    '''
    Takes a notion database ID
    Returns a list of [fact, url] pairs
    '''
    formatted_docs = []
    has_more = True
    next_cursor = None
    raw_docs = []

    while has_more:
        response = notion.databases.query(database_id,
                                          start_cursor = next_cursor)
        raw_docs.extend(response['results'])
        has_more = response['has_more']
        next_cursor = response['next_cursor']

    for doc in raw_docs:
        fdoc = [doc['properties']['Name']['title'][0]['text']['content'], # Fact
                doc['properties']['URL']['url']] # URL
        formatted_docs.append(fdoc)

    return formatted_docs

    # Alright what's the way to do this. Relations are all done by object id, so if we want to compile
    # by object then we will need to page through all _other_ databases to make it meaningful. Which
    # is an absolute pain. Just take each title as a doc in its own right, and leave a wide k window?

        

if __name__ == "__main__":
    docs = fetch_docs_from_Notion("8d5dc8537d04457fa92a543a83ac397b")
    print(f"{len(docs)} documents retrieved.")
