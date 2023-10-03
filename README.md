# Twitter AI Bot

Este projeto é um bot de Twitter que analisa a timeline da bolha dev do twitter. O bot identifica 'tretas' ou discussões interessantes e cria um tweet noticiando a mesma.

## TODO:
[ ] Permitir interações (A IA seguir pessoas, e comentar, interagindo com o público)
[ ] Melhorar error handling
[ ] Tornar a descrição de imagens assíncrona pra poupar tempo 
[ ] Subir o código para nuvem, para eu não ter que rodar ele local

## Como funciona

O bot recebe tweets da timeline e analisa o conteúdo. Se detectar uma 'treta' ou discussão interessante, ele cria um tweet com a notícia. O bot também considera as personalidades dos usuários ao analisar os tweets.

O bot também pode postar threads interessantes sobre programação para ajudar a engajar a comunidade.

## Arquivos

- `main.py`: Este é o arquivo principal que executa o bot. Ele lê os tweets da timeline, analisa o conteúdo e decide se deve criar um tweet ou não.

- `ai/__init__.py`: Este arquivo contém funções para descrever imagens e gerar respostas usando a API da OpenAI.

- `twitter/__init__.py`: Este arquivo contém funções para interagir com o Twitter, como obter a timeline e postar tweets.

## Como usar

1. Clone o repositório.
2. Instale as dependências necessárias.
3. Configure o arquivo `secrets.json` com suas credenciais do Twitter e da OpenAI.
4. Execute o arquivo `main.py` para iniciar o bot.


## Aviso

Este bot foi criado para fins de entretenimento e não deve ser usado para espalhar informações falsas ou enganar pessoas. Use com responsabilidade.

## Contribuindo

*Sinta-se livre para ajudar o projeto! Seja noticiando bugs e pedindo features nas issues, ou já dando aquele pull request massa, precisamos sempre de ajuda!*

