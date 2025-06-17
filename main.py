from agent import agent
from schemas import Pergunta, Resposta

def main():
    print("Agente de Consulta de Notas Fiscais\n")
    while True:
        pergunta = input("Pergunta (ou 'sair'): ")
        if pergunta.lower() == "sair":
            break
        entrada = Pergunta(pergunta=pergunta)
        resposta = Resposta(resposta=agent.run_sync(entrada.pergunta).output)
        print("Resposta:", resposta.resposta)

if __name__ == "__main__":
    main()