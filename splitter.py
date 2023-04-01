import pandas as pd
from transformers import GPT2TokenizerFast
tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
import re
import re

def split_text(content, chunk_size=500):
   
  podcast_contents = []

  if len(tokenizer.tokenize(content)) > chunk_size:
      split =content.split(". ");
      chunk_text = ""
      for i in range(0,len(split)):
          
          sentence = split[i]
          sentence_token_length = len(tokenizer.tokenize(sentence))
          chunk_token_length =  len(tokenizer.tokenize(chunk_text))

          if (chunk_token_length + sentence_token_length > chunk_size):
              podcast_contents.append(chunk_text)
              chunk_text = ""

          if re.match(r'\w$', sentence[len(sentence)- 1]):
              chunk_text += sentence + ". "
          else:
              chunk_text += sentence + " "
          
              podcast_contents.append(chunk_text.strip())
  else:
      podcast_contents.append(content.strip())

  return podcast_contents
    




# Load the original CSV file into a DataFrame
original = #'/Users/shiva/workspace/podcast_scraper/tim_ferriss_transcript/content-04-03-2023-13:08:00.csv'
df = pd.read_csv(original)

# Define the list of strings to search for
# famous_episodes = ["#576","#599","#582","#599","#561","#568","#600","#614","#641","#562","#633","#606","#565","#583",
# "#625","#620","#566","#593","#597","#616","#601","#594","#584","#585","#578""#621","#579","#628","#586","#567"]
famous_episodes = ["#576","#593","#601"]
pattern = r"#\d+"


def remove_newlines(serie):
    serie = serie.str.replace('\n', ' ')
    serie = serie.str.replace('\\n', ' ')
    serie = serie.str.replace('  ', ' ')
    return serie

# Create an empty DataFrame to hold the matching rows
matching_rows = pd.DataFrame(columns=['title', 'heading', 'content','tokens'])

# Iterate over the rows of the DataFrame
for i, row in df.iterrows():
  matches = re.findall(pattern, row["title"])
  common_matches = set(matches).intersection(set(famous_episodes))
  if common_matches:
      contents = split_text(row["content"])
      for content in contents:
        content = remove_newlines(content)
        token_count = len(tokenizer.tokenize(content))
        matching_rows.loc[len(matching_rows)] = {'title': row['title'], 
                                                'heading': row['url'], 
                                                'content': content,
                                                'tokens': token_count }

# Write the matching rows to a new CSV file
matching_rows.to_csv('matching.csv', index=False)
