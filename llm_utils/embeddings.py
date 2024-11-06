from langchain_ollama import OllamaEmbeddings
from pathlib import Path
from langchain.schema import Document
from langchain_chroma import Chroma
import os
import sys

sys.path.append(str(Path(__file__).parents[1]))
from data_fetch import fetch_docs_from_Notion

project_root = Path(__file__).parents[1]
persist_directory_root = project_root / "chroma_db"
embedding_model = OllamaEmbeddings(model="all-minilm:l6-v2")

def get_embeddings(dbase: str, force_refresh=False):
    persist_directory = f"{persist_directory_root}/{dbase}"

    if not os.path.exists(persist_directory) or force_refresh == True:
        documents = []
        for content, source in fetch_docs_from_Notion(dbase):
            doc = Document(page_content=content,
                        metadata={"source":source if source else ""})
            documents.append(doc)
        
        vectors = Chroma.from_documents(documents=documents,
                                        persist_directory=persist_directory,
                                        embedding=embedding_model)
    else:
        vectors = Chroma(persist_directory=persist_directory,
                         embedding_function=embedding_model)
        
    return vectors

if __name__ == "__main__":
    vectors = get_embeddings(dbase="8d5dc8537d04457fa92a543a83ac397b",force_refresh=True)
    print(vectors)