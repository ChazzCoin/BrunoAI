import requests
import chromadb
from chromadb.config import Settings


# Set up ChromaDB
client = chromadb.Client(Settings(chroma_server_host="192.168.1.6", chroma_server_http_port=8000))

def generate_embeddings(model: str, text: str) -> list:
    response = requests.post(
        "http://192.168.1.6:11434/api/embeddings",
        json={
            "model": model,
            "prompt": text
        }
    )
    if response.status_code == 200:
        embeddings = response.json()
        return embeddings
    else:
        raise Exception("Failed to generate embeddings")

def add_embeddings_to_chromadb(model: str, text_id: str, text: str):
    model_clean = model.replace(":", "_")
    collection_name = f"{model_clean}_embeddings"
    collection = client.get_or_create_collection(collection_name)
    embeddings = generate_embeddings(model, text)
    collection.add(
        ids=["one"],
        embeddings=embeddings["embedding"],
        documents=[text]
    )

def query_chromadb(model: str, query_text: str, top_k: int = 5):
    model_clean = model.replace(":", "_")
    collection_name = f"{model_clean}_embeddings"
    collection = client.get_collection(collection_name)
    query_embeddings = generate_embeddings(model, query_text)
    results = collection.query(
        query_embeddings=query_embeddings["embedding"],
        n_results=top_k
    )
    return results


# Example usage
if __name__ == "__main__":
    add_embeddings_to_chromadb("llama3:latest", "example", "This is a sample code snippet.")
    results = query_chromadb("llama3:latest", "How can I improve this sample code?")
    print(results)

