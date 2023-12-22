from llama_index import StorageContext, load_index_from_storage
import re

# load knowledge base from disk. you may want to move this outside of the answer question function to increase performance
index = load_index_from_storage(
  StorageContext.from_defaults(persist_dir="storage"))

# make the knowledge base into a query engine—an object that queries can be run on
query_engine = index.as_query_engine()

def extract_titles(text):
  # Find all occurrences of text following "Title —" up to the next newline character
  titles = re.findall(r"Title\s*—\s*([^\n]+)", text)
  # Remove duplicates by converting the list to a set, then back to a list
  unique_titles = list(set(titles))
  return unique_titles

def answer_question(query):
  # run a query on the query engine. this will:
  # find text chunks that are similar to the query we gave it
  # give the query + the text chunks to GPT-3, and then return the answer
  response = query_engine.query(query)

  # Extract titles from each TextNode in source_nodes
  
  titles = []
  if hasattr(response, 'source_nodes'):
    for node_with_score in response.source_nodes:
      node_text = node_with_score.node.text
      titles.extend(extract_titles(node_text))

  if not titles:
    titles = ["Unknown"]  # Default if no titles are extracted

  return response


def answer_questions():
  while True:
    query = input("Ask a question: ")
    if query == "quit":
      break
    response = answer_question(query)
    print(f"Answer: {response}\n\nSource Files: {', '.join(file_names)}\n")
