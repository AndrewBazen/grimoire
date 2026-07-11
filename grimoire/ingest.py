
from grimoire import retriever, generator


def chunk_text(text: str, source: str, chunk_size: int, overlap: int) -> list[dict]:
    if overlap >= chunk_size: raise ValueError("overlap must be smaller than chunk_size")
    
    chunks = []
    
    step = chunk_size - overlap
    
    for i in range(0, len(text), step):
        chunk = text[i:i + chunk_size]
        chunk_id = len(chunks)
        chunks.append({
            "text": chunk, "source": source, "chunk_id": chunk_id
        })
    
    return chunks


if __name__ == "__main__":
    from pathlib import Path
    
    # load the data from a specific path
    def load(path) -> str:
        return Path(path).read_text()
     
    chunks = []
    
    # loop over the markdown files in the data folder and chunk them
    for path in Path("data").glob("*.md"):
        chunks += chunk_text(load(path), path.name, 500, 50)
    
    # embed the chunks
    embeddings = retriever.embed_chunks(chunks)
    
    query = "What is grappling"
    
    # embed the query (will come from input later on.)
    retrieved_chunks = retriever.retrieve(query, chunks, embeddings, 3)
    
    
    response = generator.generate(query, retrieved_chunks)
    
    print(response)
    
    