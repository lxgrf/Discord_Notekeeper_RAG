from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
import logging
from langchain.chains import RetrievalQA 
import os
import glob
import pandas as pd


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    '%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

file_handler = logging.FileHandler('myapp.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


logger.info(">-------====-------<")

embedding_model = OllamaEmbeddings(model="all-minilm:l6-v2")
answer_model = ChatOllama(model="llama3.1")
persist_directory = "chroma_db"

def preprocessCSV(folder="strahd/"):

    contents = os.listdir(folder)
    logger.info(f"Starting Pre-process check")
    
    for document in contents:
        if document.endswith('.csv'):
            df = pd.read_csv(folder + document)
            
            if 'activity' in df.columns:
                logger.info(f"Processing: {document}")

                # Keep only specified columns
                df = df[['id', 'channel_id', 'content', 'date']]
                
                # Add source column
                df['source'] = df.apply(lambda row: f"https://discord.com/channels/1189577519154864168/{row['channel_id']}/{row['id']}", axis=1)
                
                # Save modified CSV
                df.to_csv(folder + document, index=False)


def load_info(directory_path="strahd/",refresh=False):

    if refresh == True or not os.path.exists(persist_directory):
        # Create embeddings, store in persist_directory
        logger.info("VECTOR CREATION REQUIRED\nThis may take a few minutes.")
        preprocessCSV(directory_path)

        logger.info("Starting to load documents...")

        # Get all CSV files in the directory
        file_paths = glob.glob(os.path.join(directory_path, "*.csv"))
        logger.info(f"Found {len(file_paths)} files.")

        all_data = []

        # Iterate over each file and load data
        for file_path in file_paths:
            logger.info(f"---- Loading data from {file_path}")
            loader = CSVLoader(file_path=file_path, source_column='source')
            data = loader.load()
            all_data.extend(data)

        logger.info(f"Total documents loaded: {len(all_data)}")

        # Split the combined data
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=25)
        split_docs = text_splitter.split_documents(all_data)
        logger.info(f"Total documents after splitting: {len(split_docs)}")

        # Create the vector store with all documents
        logger.info("Creating embeddings...")
        vectors = Chroma.from_documents(persist_directory=persist_directory,
                                        documents=split_docs,
                                        embedding=embedding_model)
        logger.info("Vector store created and saved to disk.")
    else:
        vectors = Chroma(persist_directory=persist_directory,
                         embedding_function=embedding_model)
        logger.info("Vectors loaded from disk.")

    return vectors


def answer_question(question, vectors):
    retriever = vectors.as_retriever(search_type="mmr",
                                     search_kwargs={"k":6,
                                                    "alpha":0.7})
    qa_chain = RetrievalQA.from_chain_type(llm=answer_model, 
                                           chain_type="stuff", 
                                           retriever=retriever,
                                           return_source_documents=True)
    logger.info("Vectors retrieved")

    result = qa_chain.invoke(question)
    answer = result['result']
    logger.info("Answer formulated")
    logger.info(f"Query: {result['query']}")
    logger.info(f"Answer: {answer}")

    for i, doc in enumerate(result['source_documents']):
        source_url = doc.metadata.get('source', 'No source')
        logger.info(f"Document {i + 1} Source URL: {source_url}")


    return answer


if __name__ == "__main__":
    vectors = load_info(refresh=False)
    questions = [
                "Describe Caoimhe's appearance",
                "Describe Afton's appearance",
                "Describe Arien's appearance",
                "Describe Zalen's appearance",
                "Describe Xyrelle's appearance",
                "Describe Ismark's appearance",
                 ]
    for question in questions:
        answer = answer_question(question=question, vectors=vectors)



