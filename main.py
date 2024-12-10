import os
import json
import openai
import tiktoken
import threading
import time
from openai import OpenAI
from dotenv import load_dotenv
import pandas as pd

modelo = "gpt-3.5-turbo-0125"
quantidade_tokens_aceitos = 4096
datasets = pd.read_csv('./dataset/dataset_frases.csv', engine='c', sep=',')
linha_inicial = 0


load_dotenv()
cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
executando = True
registro = []

def monitorar_entrada():
    global executando
    while executando:
        comando = input()
        if comando.lower() == "exit":
            print("Encerrando...")
            executando = False

thread = threading.Thread(target=monitorar_entrada)
thread.daemon = True
thread.start()


def analisador_sentimentos(entrada):
    prompt_sistema = f"""
        You are a sentence sentiment analyzer.
        You will receive 200 separate sentences by "||" and must return the result as a list of values, where:

        1 means the sentiment is positive or good.
        0 means the sentiment is negative or bad.
        2 means the sentiment is is neutral.

        Do not provide any additional explanation, just return the list.

        # Example of input format

        I love this! || This is terrible. || What a great day! || I hate this.

        # Example of output format

        [1,0,1,0]

        """
    
    prompt_usuario = entrada

    lista_mensagens = [
        {
            "role": "system",
            "content": prompt_sistema
        },
        {
            "role": "user",
            "content": prompt_usuario
        }
    ]

    try:
        resposta = cliente.chat.completions.create(
            messages = lista_mensagens,
            model=modelo
        )
        texto_resposta = resposta.choices[0].message.content
    except openai.APIError as e:
        print(f"Erro de API: {e}")
    
    return texto_resposta


def contador_tokens(frases):
    codificador = tiktoken.encoding_for_model(modelo)
    lista_tokens = codificador.encode(frases)
    # print(f"Esse conjunto de frase tem {len(lista_tokens)} tokens")
    # print(f"Custo para o modelo {modelo} é de ${(len(lista_tokens)/1000) * 0.005}")
    return len(lista_tokens)



linha_atual = 0
contador = 0

while executando:
    contador+=1
    str = ""
    tokens_prompt_sistema = 125
    tokens_da_entrada = 0
    tokens_da_saída = 2
    while((tokens_prompt_sistema+tokens_da_entrada+tokens_da_saída)<quantidade_tokens_aceitos-100):
        str += datasets['sentence'][linha_atual] + "||"
        linha_atual+=1
        tokens_da_entrada += contador_tokens(datasets['sentence'][linha_atual])
        tokens_da_saída+= 3
    analise = f"""
    ----------------------------------------
    {contador}° requisição:
    {tokens_prompt_sistema+tokens_da_entrada} tokens enviados;
    {linha_atual - linha_inicial} linhas analisadas.
    ----------------------------------------
    """
    registro.append(analise)
    print(f"Efetuando a {contador} requisição...")
    resposta = analisador_sentimentos(str)
    lista_real = json.loads(resposta)
    
    for i in range(len(lista_real)):
        datasets['sentiment'][(linha_atual-linha_inicial)+i] = lista_real[i]

    linha_inicial = linha_atual
    
registro.append(f"""
    ----------------------------------------
    Finalizado na linha: {linha_atual}.
    ----------------------------------------
    """)

with open("registro.txt", "w") as arquivo:
    for linha in registro:
        arquivo.write(linha + "\n")
print("As informações foram salvas no arquivo 'registro.txt'.")

datasets.to_csv('./dataset/dataset_frases_backup.csv', index=False)
datasets.to_csv('./dataset/dataset_frases.csv', index=False)   