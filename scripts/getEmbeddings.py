import sqlite3
import requests
import json
import os
import dotenv
import numpy as np

dotenv.load_dotenv()

OPEN_AI_KEY = os.getenv('OPEN_AI_KEY')

def get_embeddings(text):
    response = requests.post(
        "https://api.openai.com/v1/embeddings",
        headers={"Authorization": f"Bearer {OPEN_AI_KEY}"},
        json={"input": text, "model": "text-embedding-3-small"}
    )
    if response.status_code == 200:
        embedding_data=json.loads(response.text)["data"]
        # print(embedding_data[0]['embedding'])
        return np.array(embedding_data[0]['embedding'])
    else:
        print("Error:", response.text)
        return None

def setup_movies_database():
    conn = sqlite3.connect('movies.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS movie_text
                   (chunk_text TEXT, embedding BLOB)''')
    conn.commit()
    conn.close()

def update_chunk_with_embedding(text_chunk, embedding):
    conn = sqlite3.connect('movies.db')
    cur = conn.cursor()
    embedding = embedding.tolist()
    embedding_blob = sqlite3.Binary(json.dumps(embedding).encode('utf-8'))
    cur.execute("UPDATE movie_text SET embedding = ? WHERE chunk_text = ?", (embedding_blob, text_chunk))
    conn.commit()
    conn.close()

def generate_and_update_embeddings():
    conn = sqlite3.connect('movies.db')
    cur = conn.cursor()
    cur.execute("SELECT chunk_text FROM movie_text WHERE embedding IS NULL")
    rows = cur.fetchall()

    for count, (text_chunk,) in enumerate(rows, 1):
        embedding = get_embeddings(text_chunk)
        if len(embedding)>0:
            update_chunk_with_embedding(text_chunk, embedding)

        if count % 10 == 0:
            print(f"Processed {count} records")

    conn.close()

# Setup database
setup_movies_database()

# Generate embeddings and update the database
generate_and_update_embeddings()



