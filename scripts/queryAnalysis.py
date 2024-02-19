import numpy as np

def cosine_similarity(vec_a, vec_b):
    """Calculate the cosine similarity between two vectors."""
    dot_product = np.dot(vec_a, vec_b)
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    return dot_product / (norm_a * norm_b)

import requests
import json
import sqlite3
import os
import dotenv
dotenv.load_dotenv()

OPEN_AI_KEY = os.getenv('OPEN_AI_KEY')

def get_query_embedding(query):
    """Get the embedding of a query string."""
    response = requests.post(
        "https://api.openai.com/v1/embeddings",
        headers={"Authorization": f"Bearer {OPEN_AI_KEY}"},
        json={"input": query, "model": "text-embedding-3-small"}
    )
    if response.status_code == 200:
        return json.loads(response.text)["data"][0]["embedding"]
    else:
        print("Error:", response.text)
        return None

def get_top_5_similar_chunks(query):
    """Get the top 5 similar chunks based on cosine similarity."""
    query_embedding = get_query_embedding(query)
    if query_embedding is None:
        return []

    conn = sqlite3.connect('movies.db')
    cur = conn.cursor()
    cur.execute("SELECT chunk_text, embedding FROM movie_text")
    rows = cur.fetchall()

    similarities = []
    for row in rows:
        chunk_text, embedding_blob = row
        embedding = json.loads(embedding_blob)
        similarity = cosine_similarity(query_embedding, embedding)
        similarities.append((chunk_text, similarity))

    # Sort by similarity and get top 5
    top_5_chunks = sorted(similarities, key=lambda x: x[1], reverse=True)[:5]

    conn.close()
    return top_5_chunks

# Example usage
top_chunks = get_top_5_similar_chunks("what is Thelonius's book called which he writes")
# for chunk, similarity in top_chunks:
    # print(f"Chunk: {chunk}, Similarity: {similarity}")
