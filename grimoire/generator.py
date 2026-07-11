import ollama

def generate(query: str, top_chunks: list[dict]):
    context = build_context(top_chunks)
    prompt = f"YOUR ROLE: You are an rules expert for the dungeons and dragons \
                    5th edition SRD.  Your job is to answer questions using \
                    only the provided context.  If the answer isnt in the \
                    context just answer with 'I don't know'.  When you answer \
                    a question, cite the chunks you use with source + chunk_id at \
                    the end of your response.  Do not print the chunk's text.\
                     \
                    CONTEXT: {context} \
                    QUESTION: {query}"
    response = ollama.generate(model="llama3.2", prompt=prompt)
    return response["response"]

def build_context(top_chunks: list[dict]):
    context = ""
    for c in top_chunks:
        context += f"Source: {c["source"]} | Chunk ID: {c["chunk_id"]} | Text: {c["text"]} \n\n"
    return context