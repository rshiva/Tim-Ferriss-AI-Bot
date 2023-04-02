## Run the app locally
- pip3 install -r requirements.txt
- python app.py


## Scrape Data
To scrape the data, run the `scraper.py` script and save it in the following CSV format:

`title, url, content`

## Split Data
As GPT-3.5 only supports 4k tokens, we need to split the data. To do this, run the `splitter.py` script.

## Create Embeddings
Run the `insert_emebedding.py` script to create embeddings for the data and insert to table in supabase

## Supabase Setup
For quick and easy to get started, Create a database in supabase and run the `schema.sql` script in Supabase. Enable vector extension 

## Environment Variables
Set the following environment variables in your `~/.bash_profile` or `~/.bashrc` file:

- `SUPABASE_FN_URL` (tim_search function URL)
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `OPENAI_API_KEY`


## Credits

Thanks to [@tferriss](https://twitter.com/tferriss) for all the podcast

It was his podcast I first ever listen almost 

If you have any questions, feel free to reach out to me on Twitter [@_rshiva](https://twitter.com/_rshiva)


I kept it as simple as possible for users to jump in OPENAI.