# Desafio MBA Engenharia de Software com IA - Full Cycle

Sistema de **Ingestão e Busca (RAG)**: um PDF é dividido em chunks, convertido em embeddings via OpenAI e armazenado em um banco **PostgreSQL + pgvector**. Um chat via linha de comando busca os trechos mais relevantes do PDF e usa um LLM da OpenAI para responder **somente** com base no conteúdo encontrado.

## Pré-requisitos

- Python 3.12+
- Docker e Docker Compose
- Uma chave de API da OpenAI ([platform.openai.com](https://platform.openai.com))

## 1. Clonar o repositório

```bash
git clone <url-do-repositorio>
cd mba-ia-desafio-ingestao-busca
```

## 2. Configurar variáveis de ambiente

Copie o arquivo de exemplo e preencha os valores:

```bash
cp .env.example .env
```

| Variável                     | Descrição                                                             | Exemplo                                                     |
| ---------------------------- | ---------------------------------------------------------------------- | ------------------------------------------------------------ |
| `OPENAI_API_KEY`             | Chave de API da OpenAI                                                  | `sk-...`                                                      |
| `OPENAI_EMBEDDING_MODEL`     | Modelo usado para gerar os embeddings                                  | `text-embedding-3-small`                                      |
| `OPENAI_MODEL`               | Modelo usado para gerar as respostas do chat                           | `gpt-5`                                                       |
| `DATABASE_URL`               | String de conexão do Postgres (deve bater com o `docker-compose.yml`) | `postgresql+psycopg://postgres:postgres@localhost:5432/rag` |
| `PG_VECTOR_COLLECTION_NAME`  | Nome da coleção de vetores dentro do Postgres                          | `pdf_documents`                                               |
| `PDF_NAME`                   | Nome do arquivo PDF (na raiz do projeto) que será ingerido              | `document.pdf`                                                |

> O arquivo `document.pdf` incluído no repositório já é usado como padrão. Para usar outro PDF, coloque o arquivo na raiz do projeto e ajuste `PDF_NAME`.

## 3. Subir o banco de dados (PostgreSQL + pgvector)

```bash
docker compose up -d
```

Isso sobe o Postgres com a extensão `pgvector` já habilitada, na porta `5432`.

## 4. Criar o ambiente virtual e instalar as dependências

```bash
python3 -m venv venv
source venv/bin/activate 

pip install -r requirements.txt
```

## 5. Executar a ingestão do PDF

Gera os embeddings do PDF configurado e grava no banco de vetores:

```bash
cd src
python ingest.py
```

## 6. Rodar o chat de busca

Ainda dentro da pasta `src`:

```bash
python chat.py
```

Digite sua pergunta no prompt `PERGUNTA:` e receba a resposta baseada apenas no conteúdo do PDF ingerido. Digite `sair` (ou `exit`/`quit`) para encerrar.

Exemplo:

```
Faça sua pergunta (ou 'sair' para encerrar).
PERGUNTA: Qual o faturamento da empresa X?
RESPOSTA: RS 10.000.000,00

PERGUNTA: Qual é a capital da França?
RESPOSTA: Não tenho informações necessárias para responder sua pergunta.
```

## Estrutura do projeto

```
.
├── docker-compose.yml 
├── document.pdf    
├── requirements.txt
├── .env.example
└── src/
    ├── ingest.py 
    ├── search.py 
    └── chat.py    
```
