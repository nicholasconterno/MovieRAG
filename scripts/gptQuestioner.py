import requests
import json
import os
import dotenv
from queryAnalysis import get_top_5_similar_chunks
dotenv.load_dotenv()
OPEN_AI_KEY = os.getenv('OPEN_AI_KEY')
def query_gpt_turbo(context, question):
    """Query GPT-3.5-turbo model with context and question."""
    prompt = f"Context: {context}\nQuestion: {question}\n If the answer is not found in the context, please respond with the exact strings 'I don't know' or 'not found' ."

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {OPEN_AI_KEY}"},
        json={"model": 'gpt-3.5-turbo', "max_tokens": 150,
              "messages": [{"role": "user", "content": prompt},]}
    )
    if response.status_code == 200:
        return json.loads(response.text)["choices"][0]["message"]["content"]
    else:
        print("Error:", response.text)
        return None

def main(question):
    chunks = get_top_5_similar_chunks(question)
    """Iteratively query GPT-3.5-turbo using top chunks and find an answer."""
    for chunk in chunks:
        answer = query_gpt_turbo(chunk, question)
        print(f"Chunk: {chunk}, Answer: {answer}")
        if answer and "I don't know" not in answer and "not found" not in answer:
            return answer
    return answer


# question = "what's the deal with mary lamb"
# top_chunks=get_top_5_similar_chunks(question)
# answer = get_answer_based_on_chunks(top_chunks, question)
# print(answer)
