from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("ibm-granite/granite-embedding-small-english-r2")

def embed_chunks(chunks: list[dict]):
    sentences = [c["text"] for c in chunks]
    embeddings = model.encode(sentences)
    norm_embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
    return norm_embeddings

def retrieve(query: str, chunks: list[dict], embeddings: np.ndarray, k: int):
    # embed the query using the same model as the embeded data
    query_embed = model.encode(query)
    
    # normalize the vector
    norm_query = query_embed / np.linalg.norm(query_embed)
    
    # compute the similarities
    scores = embeddings @ norm_query
    
    # get top-k scores
    top_indices = np.argsort(-scores)[:k]
    
    response = []
    
    for idx in top_indices:
        response.append(chunks[idx])
        
    return response