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

def get_example_entry(dbase_id: str):
    '''
    Takes a notion database ID
    Returns a list of [fact, url] pairs
    '''

    raw_docs = []

    response = notion.databases.query(dbase_id)
    raw_docs.extend(response['results'])
    return raw_docs[0]


if __name__ == "__main__":
    print(get_example_entry(dbase_id="050c74f590074074a7a12dac13634fd2"))