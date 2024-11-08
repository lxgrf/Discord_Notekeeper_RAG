from notion_client import Client
from dotenv import load_dotenv
from pathlib import Path
import os
from functools import reduce

project_root = Path(__file__).parents[1]
load_dotenv(dotenv_path=project_root / ".env")
NOTION_API_KEY = os.getenv("NOTION_API_KEY")

notion = Client(auth=NOTION_API_KEY)

GUILD_DATABASES = {1114617197931790376:{"facts":"8d5dc8537d04457fa92a543a83ac397b",
                                        "objectives":"050c74f590074074a7a12dac13634fd2", 
                                        "mysteries":"110015bedb97808489dad017c1583991", 
                                        }}

def get_nested(dictionary: dict, keys: list, default=None):
    """Safely retrieves nested values from a dictionary using a sequence of keys.

    Args:
        dictionary (dict): The dictionary to traverse.
        keys (list): A sequence of keys to access nested values.
        default (Any, optional): Value to return if the path doesn't exist. Defaults to None.

    Returns:
        Any: The value at the specified nested path, or the default value if not found.
    """
    try:
        return reduce(lambda d, key: d[key] if d else default, keys, dictionary)
    except (KeyError, IndexError, TypeError):
        return default
    
def query_database(database_id: str) -> list[dict]:
    """Queries a Notion database with pagination support.

    Args:
        database_id (str): The ID of the Notion database to query.

    Returns:
        list[dict]: A list of all records from the database, with each record as a dictionary.
    """
    results = []
    next_cursor = None
    
    while True:
        response = notion.databases.query(database_id, start_cursor=next_cursor)
        results.extend(response.get('results',None))
        if not response.get('has_more',False):
            break
        next_cursor = response.get('next_cursor',None)
    
    return results

def format_objective(status: str, name: str) -> str:
    """Formats an objective's display string based on its status.

    Args:
        status (str): The current status of the objective ("Not started", "In progress", "Failed", or "Done").
        name (str): The name or description of the objective.

    Returns:
        str: A formatted string combining the status prefix and objective name.
    """
    status_prefixes = {
        "Not started": "Unstarted Objective: ",
        "In progress": "In-progress Objective: ",
        "Failed": "Objective failed: ",
        "Done": "Objective complete: "
    }
    return f"{status_prefixes.get(status, '')} {name}"

def fetch_docs_from_Notion(guild_id: int) -> list[list[str]]:
    """Fetches and formats documents from various Notion databases associated with a Discord guild.

    This function retrieves records from facts, mysteries, and objectives databases linked to a specific
    Discord guild. It processes each record type differently:
    - Facts: Returns the fact name and its URL
    - Mysteries: Returns the question and URL, prefixed with "Solved Mystery: " if answered
    - Objectives: Returns a status-prefixed objective name and an empty URL string

    Args:
        guild_id (int): The Discord guild ID to fetch documents for.

    Returns:
        list[list[str]]: A list of [content, url] pairs where:
            - content (str): The formatted text content of the document
            - url (str): The associated URL (if any, empty string if none)

    Note:
        The function requires a valid NOTION_API_KEY environment variable and proper database
        configuration in GUILD_DATABASES.
    """

    formatted_docs = []
    databases = GUILD_DATABASES.get(guild_id, {})

    for db_type, db_id in databases.items():
        if not db_id:
            continue

        raw_docs = query_database(db_id)
        
        for doc in raw_docs:
            formatted_doc = None
            
            if db_type == "facts":
                title = get_nested(doc, ['properties', 'Name', 'title', 0, 'text', 'content'])
                url = get_nested(doc,['properties','URL','url'],default="")
                if title:
                    formatted_doc = [title,url]

            elif db_type == "mysteries":
                answer = get_nested(doc, ['properties', 'Answer', 'relation'])
                question = get_nested(doc, ['properties', 'Question', 'title', 0, 'text', 'content'])
                url = get_nested(doc,['properties','URL','url'],default="")
                if question and not answer:
                    formatted_doc = [question, url]
                elif question and answer:
                    formatted_doc = ["Solved Mystery: " + question,url]

            elif db_type == "objectives":
                status = get_nested(doc, ['properties', 'Status', 'status', 'name'])
                name = get_nested(doc, ['properties', 'Name', 'title', 0, 'text', 'content'])
                if status and name:
                    formatted_doc = [format_objective(status, name),""]

            if formatted_doc:
                formatted_docs.append(formatted_doc)

    return formatted_docs

if __name__ == "__main__":
    docs = fetch_docs_from_Notion("8d5dc8537d04457fa92a543a83ac397b")
    print(f"{len(docs)} documents retrieved.")
