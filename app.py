from flask import Flask, render_template, request
from flask import Flask, Response, stream_with_context
import openai
import os, json, requests

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
  return render_template('index.html')

@app.route("/query",methods = ['POST'])       
def result():
  if request.method == 'POST':
    query = request.form['question']
    response = answer_completion(query)
    return render_template('index.html', **locals())



def search_context(query):
  embedding = get_embedding(query)
  return fetch_tim_podcast_query(embedding)


def answer_completion(query):
  res = search_context(query)
  context_str = res[0]['content']
  query = "Please provide the answer only from the above context. Keep your answer under 5 sentences. Be accurate, helpful, concise, and clear. If you can't find the answer from the context provide to you say 'Sorry, I don't know '"+ query
  prompt = f'{context_str}\n {query}'
  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    # prompt= prompt,
    messages=[{"role": "system", "content": prompt}],
    temperature=0.0,
    max_tokens=500,
    top_p=1,
    n=1,
  ) 
  return response


def get_embedding(text: str, model: str='text-embedding-ada-002') -> list[float]:
  result = openai.Embedding.create(
    model=model,
    input=text
  )
  return result["data"][0]["embedding"]

def fetch_tim_podcast_query(embedding,threshold=0.01,matches=2):
  url = os.environ.get("SUPABASE_FN_URL")

  payload = json.dumps({
    "match_count": matches,
    "query_embedding": embedding,
    "similarity_threshold": threshold
  })
  headers = {
    'Content-Type': 'application/json',
    'apikey': os.environ.get("SUPABASE_KEY"),
    'Authorization': os.environ.get("SUPABASE_KEY")
  }

  response = requests.request("POST", url, headers=headers, data=payload)

  print(response)
  return response.json()


if __name__ == "__main__":
    app.run(port=8000,debug=True)