# Teste para vaga de Engenheiro de Dados Pleno (Mercos)

Etapas para execução da aplicação:

## Configuração

Rode o comando abaixo no terminal (Linux ou MacOs)

```
$ make setup
```

## Build e Execução

Requisitos: Docker e docker-compose instalados

para a primeira execução da aplicação ao baixar o projeto, insira o comando:

```
$ make build
```

Esse comando faz o build das imagens e cria os conteineres docker

## Comandos utilitários

make kill -> para todas os containeres docker e remove a imagem criada \
make stop -> encerra a execução dos containeres \
make start -> inicia todos os conteineres \
make format -> executa o lint e formata o código


## Dashboard

Para visualização dos resultados, após rodar a aplicação acesse o link abaixo:

http://localhost:8501