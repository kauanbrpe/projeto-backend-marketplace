# 🛒 Marketplace API — Projeto Back-end

> Projeto desenvolvido para a disciplina de **Back-end** do Centro Universitário Tiradentes de Pernambuco (UNIT-PE), utilizando Python com Flask e SQLAlchemy.

---

## 📋 Sobre o Projeto

Este projeto consiste no desenvolvimento de uma **API RESTful** para um marketplace, aplicando conceitos de arquitetura de software, persistência de dados e autenticação de usuários. A API serve como camada de comunicação entre o front-end e o banco de dados, seguindo boas práticas de desenvolvimento web moderno.

> **O que é uma API?**  
> É um conjunto de regras e protocolos que permite que diferentes sistemas de software se comuniquem entre si. Funciona como uma ponte, facilitando a troca de dados e permitindo que aplicações utilizem funcionalidades externas sem precisar acessar o código-fonte original.

---

## 👥 Integrantes

| Nome |
|------|
| Kauan Henrique Silva de Lima |
| Jefferson Cláudio Veiga |
| Breno Nascimento Lima |
| Fábio Pereira da Sousa |
| Lucas Antônio da Silva |
| Isabela Inês Maria de Melo |

---

## 🚀 Tecnologias Utilizadas

### Linguagem & Framework

| Tecnologia | Descrição |
|------------|-----------|
| ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) **Python** | Linguagem de programação robusta e base do projeto |
| ![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white) **Flask** | Micro framework web leve, minimalista e flexível |
| **Flask-RESTX** | Conjunto de ferramentas open source para modelar, documentar e testar APIs RESTful |
| **Flask-Login** | Gerenciamento de sessão de usuários — login, logout e persistência de sessão |

### Banco de Dados

| Tecnologia | Descrição |
|------------|-----------|
| ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white) **PostgreSQL** | Banco de dados relacional robusto utilizado em produção (hospedado no Render) |
| **SQLite** | Banco de dados relacional embutido e serverless, utilizado em desenvolvimento |
| **SQLAlchemy** | Biblioteca ORM (Mapeador Objeto-Relacional) para abstração do banco de dados |

### Infraestrutura & Deploy

| Tecnologia | Descrição |
|------------|-----------|
| ![Render](https://img.shields.io/badge/Render-46E3B7?style=flat&logo=render&logoColor=white) **Render** | Plataforma de nuvem (PaaS) para hospedagem e escalabilidade da aplicação |
| **Gunicorn** | Servidor WSGI de alto desempenho para execução em produção |
| **Python-dotenv** | Gerenciamento de variáveis de ambiente para segurança de credenciais |

---

## 🏗️ Arquitetura

```
marketplace-api/
├── app/
│   ├── controller/    # Controladores — recebem requisições e retornam respostas
│   ├── models/        # Modelos do banco de dados (SQLAlchemy)
│   ├── repository/    # Acesso e consultas ao banco de dados
│   ├── service/       # Regras de negócio da aplicação
│   ├── __init__.py    # Inicialização da aplicação Flask
│   └── config.py      # Configurações da aplicação (banco, ambiente, etc.)
├── render.yaml        # Configuração de deploy na plataforma Render
├── requirements.txt   # Dependências do projeto
└── run.py             # Ponto de entrada da aplicação
```

---

## ⚙️ Como Executar o Projeto

### Pré-requisitos

- Python 3.14
- pip

### Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/marketplace-api.git
cd marketplace-api

# 2. Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate       # Linux/macOS
venv\Scripts\activate          # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env com suas credenciais

# 5. Execute a aplicação
python run.py
```

A API estará disponível em `http://localhost:5000`.  
A documentação interativa (Flask-RESTX) estará em `http://localhost:5000/docs`.

---

## 📄 Licença

Este projeto é de uso acadêmico, desenvolvido para fins educacionais na disciplina de Back-end — UNIT-PE.