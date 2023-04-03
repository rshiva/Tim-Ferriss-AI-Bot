import numpy as np
import openai
import pandas as pd
import pickle
import asyncio
from datetime import datetime
import requests
import json
import os
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
openai_key: str = os.environ.get("OPENAI_API_KEY")
supabase: Client = create_client(url, key)

COMPLETIONS_MODEL = "text-davinci-003"
EMBEDDING_MODEL = "text-embedding-ada-002"


df = pd.read_csv('matching.csv',index_col=False)
df.sample(2)

def get_embedding(text: str, model: str=EMBEDDING_MODEL) -> list[float]:
  result = openai.Embedding.create(
    model=model,
    input=text
  )
  return result["data"][0]["embedding"]

def compute_doc_embeddings(df: pd.DataFrame) -> dict[tuple[str, str], list[float]]:
   for idx, row in df.iterrows():
      embedding = get_embedding(row["content"])
      data, count = supabase.table('tim').insert({"title": row["title"], "url": row["heading"], "content": row["content"], "content_tokens": row["tokens"], "embedding": embedding}).execute()
      print("data, count",data, count)

compute_doc_embeddings(df)
