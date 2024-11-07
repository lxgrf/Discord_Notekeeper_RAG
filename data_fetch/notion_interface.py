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

def fetch_docs_from_Notion(guild_id: int) -> list[list[str]]:
    """
    Fetches documents from various Notion databases associated with a guild.
    
    Args:
        guild_id: The Discord guild ID
    Returns:
        A list of [content, url] pairs from the databases
    """
    # ... existing imports and setup ...

    def query_database(database_id: str) -> list[dict]:
        """Helper function to handle pagination"""
        results = []
        next_cursor = None
        
        while True:
            response = notion.databases.query(database_id, start_cursor=next_cursor)
            results.extend(response['results'])
            if not response['has_more']:
                break
            next_cursor = response['next_cursor']
        
        return results

    def format_objective(status: str, name: str) -> str:
        """Helper function to format objective strings"""
        status_prefixes = {
            "Not started": "Unstarted Objective: ",
            "In progress": "In-progress Objective: ",
            "Failed": "Objective failed: ",
            "Done": "Objective complete: "
        }
        return f"{status_prefixes.get(status, '')} {name}"

    formatted_docs = []
    databases = GUILD_DATABASES.get(guild_id, {})

    for db_type, db_id in databases.items():
        if not db_id:
            continue

        raw_docs = query_database(db_id)
        
        for doc in raw_docs:
            formatted_doc = None
            
            if db_type == "lore":
                formatted_doc = [
                    f"Setting Lore {doc['properties']['Name']['title'][0]['text']['content']}", 
                    ""  # URL placeholder
                ]
            elif db_type == "facts":
                formatted_doc = [
                    doc['properties']['Name']['title'][0]['text']['content'],
                    ""  # URL placeholder
                ]
            elif db_type == "mysteries":
                if not doc['properties']['Answer']['relation']:  # If unanswered
                    formatted_doc = [
                        doc['properties']['Question']['title'][0]['text']['content'],
                        ""  # URL placeholder
                    ]
            elif db_type == "objectives":
                status = doc['properties']['Status']['status']['name']
                name = doc['properties']['Name']['title'][0]['text']['content']
                formatted_doc = [
                    format_objective(status, name),
                    ""  # URL placeholder
                ]

            if formatted_doc:
                formatted_docs.append(formatted_doc)

    return formatted_docs

if __name__ == "__main__":
    docs = fetch_docs_from_Notion("8d5dc8537d04457fa92a543a83ac397b")
    print(f"{len(docs)} documents retrieved.")
