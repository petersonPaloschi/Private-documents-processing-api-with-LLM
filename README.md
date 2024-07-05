# Motor LLM para Busca em Documentos Privados

Este projeto é um motor LLM que permite anexar diversos documentos privados e utilizar um modelo de indexação para efetuar buscas nas referências.

## Instalação

Para rodar o projeto, siga os passos abaixo:

1. Instale as dependências necessárias:
   ```sh
   pip install -r ./requirements.txt
   ```

2. Execute o arquivo main.py:
   ```sh
   python main.py
   ```

## Uso da API
Endpoint: Seu_IP/chat
Use o método POST com os seguintes parâmetros:
 ```js
 {
 "departament": "CDC",
 "query": "O que é o CDC?"
 }
 ```
## Criar Novas Pastas e Gerar Novos Dados
```sh
python ingest.py
```







