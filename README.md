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
python ingest_documents.py
```
## Obs:.
Este projeto é uma prova de conceito desenvolvida para estudar sua viabilidade. Mostrou-se altamente viável, então estou compartilhando o código dos meus estudos. A partir de agora, irei focar na implementação de melhorias de desempenho e segurança, mas não planejo atualizar este código.

Atualize o config.py e o restante está totalmente funcional para ser hospedado em um servidor.







