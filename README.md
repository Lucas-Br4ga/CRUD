# 📚 Documentação da API de Gerenciamento de Produtos

Bem-vindo à documentação da **API de Gerenciamento de Produtos**, uma aplicação web desenvolvida com **Flask** e **SQLite** para gerenciar produtos de forma eficiente. Esta API permite cadastrar, listar, editar e excluir produtos, armazenando informações como descrição, preço de compra, preço de venda e data de criação. Abaixo, você encontrará todos os detalhes necessários para entender e utilizar a API.

---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Pré-requisitos](#pré-requisitos)
3. [Estrutura do Projeto](#estrutura-do-projeto)
4. [Configuração do Banco de Dados](#configuração-do-banco-de-dados)
5. [Endpoints da API](#endpoints-da-api)
   - [Cadastrar Produto](#1-cadastrar-produto)
   - [Listar Produtos](#2-listar-produtos)
   - [Editar Produto](#3-editar-produto)
   - [Excluir Produto](#4-excluir-produto)
   - [Tratamento de Erros](#5-tratamento-de-erros)
6. [Templates HTML](#templates-html)
   - [Cadastrar Produto (cadastrar.html)](#cadastrarhtml)
   - [Listar Produtos (listar.html)](#listarhtml)
   - [Editar Produto (editar.html)](#editarhtml)
   - [Página de Erro (404.html)](#404html)
7. [Como Executar a Aplicação](#como-executar-a-aplicação)
8. [Exemplo de Uso](#exemplo-de-uso)
9. [Possíveis Melhorias](#possíveis-melhorias)
10. [Licença](#licença)

---

## 🌟 Visão Geral

A API de Gerenciamento de Produtos é uma aplicação web que permite o gerenciamento de um catálogo de produtos. Utiliza **Flask** como framework backend, **SQLite** como banco de dados e templates **Jinja2** para renderizar páginas HTML. A aplicação é ideal para pequenos sistemas de estoque ou lojas que precisam de uma interface simples para gerenciar produtos.

### Funcionalidades
- **Cadastrar**: Adicionar novos produtos com descrição, preço de compra, preço de venda e data de criação.
- **Listar**: Exibir todos os produtos cadastrados em uma tabela.
- **Editar**: Atualizar informações de um produto existente.
- **Excluir**: Remover um produto do banco de dados.
- **Tratamento de Erros**: Exibir mensagens de erro personalizadas, incluindo páginas 404.

---

## 🛠 Pré-requisitos

Para executar a aplicação, você precisa dos seguintes requisitos:

- **Python 3.6+** instalado.
- Bibliotecas Python:
  - `flask`
  - `sqlite3` (já incluído no Python)
- Um navegador web (Chrome, Firefox, etc.) para acessar a interface.
- Opcional: Um editor de código (VS Code, PyCharm, etc.) para modificar os arquivos.

Instale as dependências com o seguinte comando:
```bash
pip install flask
```

---

## 📂 Estrutura do Projeto

A estrutura de arquivos da aplicação é organizada da seguinte forma:

```
project/
├── database/
│   └── db-produtos.db  # Banco de dados SQLite
├── templates/
│   ├── cadastrar.html  # Template para cadastrar produtos
│   ├── listar.html     # Template para listar produtos
│   ├── editar.html     # Template para editar produtos
│   ├── 404.html        # Template para erros 404
├── API.py              # Código principal da API
└── README.md           # Documentação (este arquivo)
```

---

## 🗄 Configuração do Banco de Dados

A aplicação utiliza um banco de dados **SQLite** chamado `db-produtos.db`, armazenado no diretório `database/`. A tabela `produtos` possui a seguinte estrutura:

```sql
CREATE TABLE produtos (
    idproduto INTEGER PRIMARY KEY AUTOINCREMENT,
    descricao TEXT NOT NULL,
    precocompra REAL NOT NULL,
    precovenda REAL NOT NULL,
    datacriacao DATE NOT NULL
);
```

### Passos para Configurar o Banco
1. Crie o diretório `database/` na raiz do projeto, se não existir.
2. Execute o seguinte código Python para criar a tabela:

```python
import sqlite3

conn = sqlite3.connect('database/db-produtos.db')
cur = conn.cursor()
cur.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        idproduto INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao TEXT NOT NULL,
        precocompra REAL NOT NULL,
        precovenda REAL NOT NULL,
        datacriacao DATE NOT NULL
    )
''')
conn.commit()
conn.close()
```

3. Certifique-se de que o arquivo `db-produtos.db` está no diretório `database/`.

---

## 🚀 Endpoints da API

A API possui cinco endpoints principais, todos acessíveis via navegador ou ferramentas como Postman.

### 1. Cadastrar Produto
- **Rota**: `/produtos/cadastrar`
- **Métodos**: `GET`, `POST`
- **Descrição**: Exibe um formulário para cadastrar um novo produto (`GET`) ou processa os dados do formulário para inserir um produto no banco de dados (`POST`).
- **Parâmetros (POST)**:
  - `descricao` (string): Descrição do produto.
  - `precocompra` (float): Preço de compra do produto.
  - `precovenda` (float): Preço de venda do produto.
  - `datacriacao` (date): Data de criação (gerada automaticamente).
- **Resposta**:
  - **Sucesso**: Renderiza `cadastrar.html` com mensagem "Sucesso - cadastrado".
  - **Erro**: Renderiza `cadastrar.html` com mensagem "Erro - não cadastrado".
- **Exemplo**:
  ```http
  POST /produtos/cadastrar
  Content-Type: application/x-www-form-urlencoded

  descricao=Mouse&precocompra=50.00&precovenda=80.00
  ```

### 2. Listar Produtos
- **Rota**: `/produtos/listar`
- **Método**: `GET`
- **Descrição**: Exibe uma tabela com todos os produtos cadastrados.
- **Resposta**: Renderiza `listar.html` com a lista de produtos.
- **Exemplo**:
  ```http
  GET /produtos/listar
  ```

### 3. Editar Produto
- **Rota**: `/produtos/editar/<int:idproduto>`
- **Métodos**: `GET`, `POST`
- **Descrição**:
  - `GET`: Exibe o formulário de edição com os dados do produto especificado.
  - `POST`: Atualiza os dados do produto no banco de dados.
- **Parâmetros (POST)**:
  - `descricao` (string): Nova descrição do produto.
  - `precocompra` (float): Novo preço de compra.
  - `precovenda` (float): Novo preço de venda.
- **Resposta**:
  - **Sucesso (POST)**: Redireciona para `/produtos/listar`.
  - **Sucesso (GET)**: Renderiza `editar.html` com os dados do produto.
  - **Erro**: Renderiza `404.html` ou `erro.html` com mensagem apropriada.
- **Exemplo**:
  ```http
  GET /produtos/editar/1
  ```
  ```http
  POST /produtos/editar/1
  Content-Type: application/x-www-form-urlencoded

  descricao=Mouse Atualizado&precocompra=55.00&precovenda=85.00
  ```

### 4. Excluir Produto
- **Rota**: `/produtos/deletar/<int:idproduto>`
- **Método**: `GET`
- **Descrição**: Exclui o produto especificado do banco de dados.
- **Resposta**:
  - **Sucesso**: Redireciona para `/produtos/listar`.
  - **Erro**: Renderiza `erro.html` com mensagem "Erro ao excluir o produto.".
- **Exemplo**:
  ```http
  GET /produtos/deletar/1
  ```

### 5. Tratamento de Erros
- **Rota**: Qualquer rota não encontrada
- **Código**: 404
- **Descrição**: Exibe uma página de erro personalizada para rotas inválidas.
- **Resposta**: Renderiza `404.html` com mensagem padrão.
- **Exemplo**:
  ```http
  GET /pagina_inexistente
  ```

---

## 📄 Templates HTML

Os templates HTML são renderizados usando **Jinja2** e fornecem a interface visual da aplicação.

### cadastrar.html
- **Descrição**: Formulário para cadastrar novos produtos.
- **Campos**:
  - Descrição (texto)
  - Preço de Compra (número)
  - Preço de Venda (número)
- **Mensagem**: Exibe "Sucesso - cadastrado" ou "Erro - não cadastrado" após submissão.
- **Ação**: Envia dados para `/produtos/cadastrar` (POST).

### listar.html
- **Descrição**: Tabela com todos os produtos cadastrados.
- **Colunas**:
  - ID
  - Descrição
  - Preço de Compra
  - Preço de Venda
  - Ações (Editar | Deletar)
- **Links**:
  - Editar: Redireciona para `/produtos/editar/<idproduto>`.
  - Deletar: Redireciona para `/produtos/deletar/<idproduto>` com confirmação via JavaScript.
  - Cadastrar novo produto: Redireciona para `/produtos/cadastrar`.

### editar.html
- **Descrição**: Formulário para editar um produto existente.
- **Campos**: Mesmos de `cadastrar.html`, pré-preenchidos com os dados do produto.
- **Ação**: Envia dados para `/produtos/editar/<idproduto>` (POST).

### 404.html
- **Descrição**: Página de erro para rotas não encontradas ou produtos inexistentes.
- **Conteúdo**: Mensagem de erro e link para voltar à lista de produtos.

---

## 🏃 Como Executar a Aplicação

1. **Clone o Repositório** (se aplicável):
   ```bash
   git clone <url-do-repositorio>
   cd project
   ```

2. **Crie o Banco de Dados**:
   Execute o script SQL fornecido na seção [Configuração do Banco de Dados](#configuração-do-banco-de-dados).

3. **Instale as Dependências**:
   ```bash
   pip install flask
   ```

4. **Execute a Aplicação**:
   ```bash
   python API.py
   ```

5. **Acesse a Aplicação**:
   Abra um navegador e vá para `http://127.0.0.1:5000/produtos/listar`.

---

## 📖 Exemplo de Uso

1. **Cadastrar um Produto**:
   - Acesse `http://127.0.0.1:5000/produtos/cadastrar`.
   - Preencha o formulário com:
     - Descrição: "Teclado Mecânico"
     - Preço de Compra: 100.00
     - Preço de Venda: 150.00
   - Clique em "Cadastrar".
   - Veja a mensagem de sucesso.

2. **Listar Produtos**:
   - Acesse `http://127.0.0.1:5000/produtos/listar`.
   - Veja o produto "Teclado Mecânico" na tabela.

3. **Editar um Produto**:
   - Clique em "Editar" na linha do produto.
   - Altere o preço de venda para 160.00.
   - Clique em "Salvar alterações".
   - Verifique a atualização na lista.

4. **Excluir um Produto**:
   - Clique em "Deletar" na linha do produto.
   - Confirme a exclusão.
   - Verifique que o produto foi removido da lista.

---

## 🔧 Possíveis Melhorias

- **Validação de Entrada**: Adicionar validação para garantir que `precocompra` e `precovenda` sejam números positivos.
- **Estilização**: Melhorar o design dos templates com CSS ou frameworks como Bootstrap.
- **Autenticação**: Implementar login para restringir acesso à API.
- **API RESTful**: Adicionar endpoints JSON para integração com outras aplicações.
- **Testes**: Criar testes unitários para os endpoints e templates.
- **Paginação**: Implementar paginação na lista de produtos para grandes volumes de dados.

---

## 📜 Licença

Este projeto é distribuído sob a licença **MIT**. Sinta-se à vontade para usar, modificar e distribuir conforme necessário.

---

**Desenvolvido com 💻 e ☕ por [Seu Nome].**
