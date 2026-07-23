import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def search_vector_store(query: str):
    embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL"))
    store = PGVector(
        embeddings=embeddings,
        connection=os.getenv("DATABASE_URL"), 
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        use_jsonb=True
    )
    
    return store.similarity_search_with_score(query, k=10)  

def search_prompt(question=None):
  resultados = search_vector_store(question)
  context = "\n\n".join(doc.page_content for doc, score in resultados)
  
  prompt_template = PromptTemplate.from_template(PROMPT_TEMPLATE)
  prompt = prompt_template.invoke({"contexto": context, "pergunta": question})
  
  llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL"), temperature=0.9)

  return llm.invoke(prompt).content
  