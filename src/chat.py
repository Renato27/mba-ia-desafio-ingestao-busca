from search import search_prompt
from dotenv import load_dotenv

load_dotenv()

def main():
    print("Faça sua pergunta (ou 'sair' para encerrar).")
    while True:
        pergunta = input("PERGUNTA: ").strip()
        if pergunta.lower() in ("sair", "exit", "quit"):
            break
        if not pergunta:
            continue

        resposta = search_prompt(pergunta)
        print(f"RESPOSTA: {resposta}\n")

if __name__ == "__main__":
    main()