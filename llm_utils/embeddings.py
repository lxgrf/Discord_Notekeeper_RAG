from langchain_ollama import OllamaEmbeddings, ChatOllama
from pathlib import Path
from langchain.schema import Document
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
import os
import sys

sys.path.append(str(Path(__file__).parents[1]))
from data_fetch import fetch_docs_from_Notion


"""
Utility module for managing embeddings and question-answering functionality using LangChain and Ollama.
This module handles document embedding storage and retrieval for a question-answering system.
"""

project_root = Path(__file__).parents[1]
persist_directory_root = project_root / "chroma_db"

embedding_model = OllamaEmbeddings(model="all-minilm:l6-v2")
answer_model = ChatOllama(model="llama3.1")

def get_embeddings(guild: int, force_refresh=False):
    """
    Retrieve or create document embeddings for a specific guild.

    Args:
        guild (int): The guild ID to fetch embeddings for
        force_refresh (bool, optional): Force regeneration of embeddings. Defaults to False.

    Returns:
        Chroma: A Chroma vector store instance containing the document embeddings

    Note:
        Documents are fetched from Notion if embeddings don't exist or force_refresh is True.
        Embeddings are persisted to disk in the chroma_db directory.
    """
    persist_directory = f"{persist_directory_root}/{guild}"
    if not os.path.exists(persist_directory) or force_refresh == True:
        documents = []
        for content, source in fetch_docs_from_Notion(guild):
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

def get_answer(question:str,guild:int) -> str:
    """
    Generate an answer to a question using the guild's document embeddings.

    Args:
        question (str): The question to answer
        guild (int): The guild ID to use for context

    Returns:
        str: The generated answer based on relevant document context

    Note:
        Uses Maximum Marginal Relevance (MMR) for document retrieval and
        the 'stuff' chain type for question answering.
    """
    vectors = get_embeddings(guild)
    retriever = vectors.as_retriever(search_type="mmr",
                                     search_kwargs={"k":15,
                                                    "alpha":0.7})
    qa_chain = RetrievalQA.from_chain_type(llm=answer_model,
                                           chain_type="stuff",
                                           retriever=retriever)
    result = qa_chain.invoke(question)
    return result['result']

if __name__ == "__main__":
    vectors = get_embeddings(guild="8d5dc8537d04457fa92a543a83ac397b",force_refresh=True)
    print(vectors)