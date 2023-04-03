--  Run 1st
create extension vector;

-- Run 2nd 
create table tim (
  id int primary key,
  url text,
  title text,
  content text,
  content_tokens int,
  embedding vector (1536)
);

-- RUN 3rd 
create or replace function tim_search (
      query_embedding vector(1536),
      similarity_threshold float,
      match_count int
    )
    returns table (
      id int,
      title text,
      url text,
      content text,
      content_tokens integer,
      similarity float
    )
    language plpgsql
    as $$
    begin
      return query
      select
        tim.id,
        tim.title,
        tim.url,
        tim.content,
        tim.content_tokens,
        1 - (tim.embedding <=> query_embedding) as similarity
      from tim
      where 1 - (tim.embedding <=> query_embedding) > similarity_threshold
      order by tim.embedding <=> query_embedding
      limit match_count;
    end;
    $$

 