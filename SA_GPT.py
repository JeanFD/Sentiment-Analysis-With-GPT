import os
import json
import threading
from openai import OpenAI, APIError
from dotenv import load_dotenv
import pandas as pd

modelo = "gpt-4o"
datasets = pd.read_csv('./dataset/dataset_frases.csv', engine='c', sep=',')
linha_inicial = 0

load_dotenv()
cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
executando = True

def monitorar_entrada():
    global executando
    while executando:
        comando = input()
        if comando.lower() == "exit":
            print("Encerrando...")
            executando = False

def analisador_sentimentos(entrada):
    prompt_sistema = f"""
        You are a sentence sentiment analyzer.
        You will receive 100 separate sentences by "||" and must return the result as a list of exactly 100 values without spaces, where:

        1 means the sentiment is positive or good.
        0 means the sentiment is negative or bad.

        Do not provide any additional explanation, just return the list.

         # Format of input format

        I love this! || This is terrible. || What a great day! || I hate this.

        # Format of output format

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
            model=modelo,
            temperature=0
        )
        texto_resposta = resposta.choices[0].message.content
    except APIError as e:
        print(f"Erro de API: {e}")
    
    return texto_resposta, resposta

datasets.to_csv('./dataset/dataset_frases_backup.csv', index=False)

thread = threading.Thread(target=monitorar_entrada)
thread.daemon = True
thread.start()
print("Em execução, digite exit para encerrar")

linha_atual = linha_inicial
contador = 0

while executando:
    datasets.to_csv('./dataset/dataset_frases.csv', index=False)
    contador+=1
    entrada = ""
    tokens_da_entrada = 0

    for i in range(100):
        entrada += "'" + str(datasets['sentence'][linha_atual]) + "'||"
        linha_atual = linha_inicial + i     

    print(f"Efetuando a {contador} requisição...")
    resposta, completo = analisador_sentimentos(entrada)
    print(f"Requisição {contador} completa")

    try:
        lista_real = json.loads(resposta)
        datasets.log[(linha_inicial):(linha_inicial+len(lista_real)-1), 'sentiment'] = lista_real
    except:
        print(f"Erro na resposta: efeturando requisição novamente")
        contador -= 1
        linha_atual = linha_inicial
    linha_inicial = linha_atual + 1

print(f"Script finalizado na linha: {linha_atual}")

datasets.to_csv('./dataset/dataset_frases.csv', index=False)   