# Back-end
Backend do MVP de Desenvolvimento Full Stack

# Backend da API de produtos com SQLite e Flask

## Descrição

Esta é uma API RESTful simples para gerenciar produtos, construída com Flask, um microframework web em Python. A API utiliza SQLite como banco de dados para armazenar informações dos usuários e Flasgger para gerar documentação interativa da API com Swagger UI.

## Funcionalidades

- **Cadastro de produtos**: Permite adicionar novos produtos ao sistema.
- **Busca de produto por ID**: Retorna as informações de um produto específico pelo seu ID.
- **Busca de todos os produtos**: Retorna uma lista com todos os produtos cadastrados.
- **Deleção de produto por ID**: Remove um produto do sistema pelo seu ID.

## Tecnologias Utilizadas

- **Flask**: Microframework web em Python para desenvolvimento rápido de APIs.
- **SQLite**: Banco de dados relacional leve e embutido, ideal para projetos pequenos e desenvolvimento.
- **Flasgger**: Extensão do Flask que integra a documentação Swagger UI à API.

## Instalação e Execução

## Clone o repositório:

```bash
git clone https://github.com/Mariferrersz/backend.git

## Crie e ative o ambiente virtual:

python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows

## Instale as dependências:

pip install -r requirements.txt

## Execute a aplicação:

python app.py

A API estará disponível em http://127.0.0.1:5000/.

Acesse a documentação da API em http://127.0.0.1:5000/apidocs/.

## Rotas da API
Método	Endpoint	Descrição
POST	/cadastrar_usuario	Cadastra um novo usuário
GET	/buscar_usuario/<id>	Busca um usuário pelo ID
GET	/buscar_usuario	Busca todos os usuários
DELETE	/deletar_usuario/<id>	Deleta um usuário pelo ID

Estrutura do Projeto
backend/
├── app.py
├── banco.db
└── requirements.txt
