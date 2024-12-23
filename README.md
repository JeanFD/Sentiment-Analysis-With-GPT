# Sentiment Analysis Automation Script

Este repositório contém um script Python para análise automatizada de sentimentos em sentenças, utilizando a API da OpenAI. O objetivo é processar frases contidas em um dataset e classificar o sentimento de cada uma como positivo (1) ou negativo (0).

## Funcionalidades

- **Análise de Sentimentos**: Processa até 100 frases por requisição, utilizando o modelo GPT-4.
- **Backup Automático**: Cria backups do dataset antes de iniciar o processamento.
- **Monitoramento e Controle**: Permite encerrar a execução com um comando via entrada do usuário.
- **Requisições Resilientes**: Reenvia requisições em caso de falha para garantir a continuidade do processamento.

## Pré-requisitos

- Python 3.7+
- Bibliotecas Python:
  - `os`
  - `json`
  - `openai`
  - `threading`
  - `dotenv`
  - `pandas`

## Estrutura do Dataset

O dataset de entrada deve estar localizado em `./dataset/dataset_frases.csv` e conter uma coluna chamada `sentence`, com as frases a serem analisadas. O script adicionará uma coluna `sentiment` para armazenar os resultados.

## Como Usar

1. Clone este repositório e navegue até o diretório do projeto:

```bash
git clone <url_do_repositorio>
cd <nome_do_repositorio>
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Adicione sua chave de API da OpenAI no arquivo `.env`.

```env
OPENAI_API_KEY=your_api_key_here
```

5. Execute o script:

```bash
python script.py
```

5. Para encerrar o processamento, digite `exit` no terminal.

## Funcionamento do Script

- **Entrada**: O script lê frases do dataset e as processa em lotes de 100 sentenças.
- **API OpenAI**: Envia os lotes para o modelo GPT-4 e obtém uma lista de resultados binários indicando o sentimento.
- **Saída**: Atualiza o dataset com os resultados e salva as alterações em tempo real.

## Tratamento de Erros

- Em caso de erro na resposta da API, o script reenvia a requisição automaticamente para evitar perda de dados.
- Todos os resultados são salvos em um backup antes do início da execução.
> [!Caution]
> **Atenção:** Caso um erro persista, o script continuará tentando enviar a requisição indefinidamente, o que pode gerar altos custos de API. É importante monitorar a execução para evitar gastos inesperados.

## Limitações

- **Custo de API**: O uso do modelo GPT-4 pode ser caro dependendo do volume de dados processados.
- **Dependência de Conexão**: Requer uma conexão estável com a internet para acessar a API da OpenAI.
- **Escalabilidade**: O processamento é feito sequencialmente, o que pode limitar o desempenho em datasets muito grandes.
- **Formato do Dataset**: O script depende de um formato específico para o dataset e pode falhar se houver inconsistências.

## Possíveis Melhorias Futuras

- Adicionar suporte para modelos alternativos.
- Implementar paralelismo para melhorar o desempenho.
- Criar um sistema de logs detalhados para análise de falhas.
- Otimizar o tratamento de erros para identificar e corrigir problemas específicos.
- Melhorar a interface de entrada para permitir configurações personalizáveis, como tamanho dos lotes e modelo a ser usado.

## Estrutura do Repositório

```plaintext
/
├── dataset/
│   ├── dataset_frases.csv           # Dataset de entrada
│   ├── dataset_frases_backup.csv    # Backup do dataset original
├── .env                             # Arquivo de configuração da chave API
├── script.py                        # Script principal
├── README.md                        # Este arquivo
└── requirements.txt                 # Dependências do projeto
```

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
