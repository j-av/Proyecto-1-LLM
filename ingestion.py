import os
from langchain_community.document_loaders import UnstructuredHTMLLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Pinecone
from langchain_text_splitters import RecursiveCharacterTextSplitter

from consts import INDEX_NAME

# Cargar embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

def ingest_docs():
    docs_path = r"C:\Users\USUARIO\PycharmProjects\doc-assistant\info"
    
    # Cargar documentos HTML usando UnstructuredHTMLLoader
    documents = []
    for filename in os.listdir(docs_path):
        if filename.endswith(".html"):
            file_path = os.path.join(docs_path, filename)
            loader = UnstructuredHTMLLoader(file_path)
            documents.extend(loader.load())

    print(f"Loaded {len(documents)} raw documents")
    
    # Dividir los documentos en trozos más pequeños
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50)
    documents = text_splitter.split_documents(documents)
    
    print(f"Split into {len(documents)} documents")

    # Actualizar las URLs de los metadatos de los documentos
    for doc in documents:
        new_url = doc.metadata["source"]
        new_url = new_url.replace("langchain-docs", "https:/")
        doc.metadata.update({"source": new_url})

    print(f"Going to add {len(documents)} to Pinecone")
    
    # Añadir documentos a Pinecone
    Pinecone.from_documents(documents, embeddings, index_name=INDEX_NAME)

if __name__ == "__main__":
    ingest_docs()
