# Prompt para Criar um Novo Sistema do Zero

> **Instrução:** Copie tudo que está dentro do bloco abaixo e cole em um novo chat (Claude, ChatGPT, etc.)

---

## COPIE A PARTIR DAQUI:

```
# CONTEXTO

Eu tenho um Windows 10 e quero criar um sistema completo para a internet.
Não tenho nada instalado - nem VS Code, nem Git, nem Docker, nada.
Quero que você me guie passo a passo, desde instalar as ferramentas até o sistema rodando num VPS Linux.

# O QUE QUERO CRIAR

[CRIE AQUI UMA DESCRIÇÃO DO SISTEMA QUE VOCÊ QUER]

Exemplo de como descrever:
"Criar um sistema de controle de estoque para uma loja de materiais de construção.
Preciso de:
- Tela de login
- Cadastro de produtos (nome, descrição, código, preço de custo, preço de venda, estoque)
- Cadastro de clientes (nome, CPF/CNPJ, telefone, email, endereço)
- Controle de estoque (entrada e saída de produtos)
- Tela de vendas (selecionar produto, quantidade, cliente, forma de pagamento)
- Dashboard com métricas (total de produtos, estoque baixo, últimas vendas)
- Usuário admin padrão: admin@email.com / admin123"

# STACK QUE DEVO USAR

Use exatamente estas tecnologias:
- Frontend: React + TypeScript + Tailwind CSS + Vite
- Backend: Python + FastAPI + SQLAlchemy + Pydantic
- Banco: PostgreSQL 16
- Container: Docker + Docker Compose
- Versão: Git + GitHub
- Hospedagem: VPS Linux (Ubuntu) com Docker
- HTTPS: Cloudflare (gratuito)

# COMO EU QUERO QUE FUNCIONE

1. PRIMEIRO: Me diga exatamente quais extensões do VS Code instalar
2. SEGUNDO: Crie todo o código do projeto (backend + frontend + banco)
3. TERCEIRO: Crie os arquivos Docker para rodar localmente no Windows
4. QUARTO: Me teste localmente antes de mandar para o VPS
5. QUINTO: Me dê os comandos para enviar para o GitHub
6. SEXTO: Me dê os comandos para instalar no VPS Linux
7. SÉTIMO: Crie um manual completo em português para eu consultar depois

# REGRAS IMPORTANTES

- Tudo em português (comentários do código, mensagens de erro, etc.)
- Use o init.sql para criar o banco com tabelas e dados de exemplo
- O banco deve ser criado automaticamente pelo Docker (sem configuração manual)
- O frontend deve usar o estilo clean com Tailwind CSS (cores escuras, cards, etc.)
- Cada tela deve ter: listar, adicionar, editar, excluir
- Trate todos os erros (API error, validação, etc.)
- O DELETE deve retornar 204 No Content (sem corpo JSON)
- Todas as rotas devem aceitar com e sem trailing slash (GET "", GET "/")
- POST e PUT devem aceitar com e sem trailing slash também

# ESTRUTURA DO PROJETO

exemplo Crie a seguinte estrutura de pastas:

meu-projeto/
├── frontend/
│   ├── src/
│   │   ├── components/    (componentes reutilizáveis: DataTable, Modal, Layout)
│   │   ├── pages/         (páginas: Login, Dashboard, [módulos do sistema])
│   │   ├── services/      (api.ts - chamadas HTTP)
│   │   ├── types/         (interfaces TypeScript)
│   │   └── contexts/      (AuthContext - autenticação)
│   ├── Dockerfile
│   └── vite.config.ts
├── backend/
│   ├── app/
│   │   ├── api/           (rotas: auth.py, [módulos].py)
│   │   ├── core/          (config.py, database.py, security.py)
│   │   ├── models/        (modelos SQLAlchemy)
│   │   ├── schemas/       (schemas Pydantic)
│   │   └── main.py        (app FastAPI)
│   ├── Dockerfile
│   └── requirements.txt
├── database/
│   └── init.sql           (criação das tabelas + dados de exemplo)
├── docker-compose.yml     (desenvolvimento)
├── docker-compose.prod.yml (produção)
├── nginx.conf             (proxy reverso para produção)
└── docs/
    └── MANUAL_COMPLETO.md (manual para leigos)
```

---

## COMO USAR ESTE PROMPT

### Passo 1: Abra um novo chat
- Claude: https://claude.ai
- ChatGPT: https://chat.opengpt.com

### Passo 2: Cole o prompt
- Copie tudo que está dentro do bloco de código acima
- Cole no chat
- **IMPORTANTE:** Substitua a seção `[CRIE AQUI UMA DESCRIÇÃO DO SISTEMA QUE VOCÊ QUER]` com a descrição do seu sistema

### Passo 3: Siga as instruções
- O chat vai criar todo o código
- Siga os passos que ele der
- Teste localmente antes de enviar para o VPS

### Exemplo de descrição para o prompt:

**Sistema de Biblioteca:**
```
Criar um sistema de gerenciamento de biblioteca.
Preciso de:
- Tela de login
- Cadastro de livros (título, autor, ISBN, editora, ano, quantidade)
- Cadastro de usuários da biblioteca (nome, CPF, email, telefone)
- Empréstimo de livros (usuário, livro, data empréstimo, data devolução)
- Devolução de livros
- Dashboard (livros disponíveis, empréstimos ativos, atrasados)
- Usuário admin: admin@biblioteca.com / admin123
```

**Sistema de Clínica:**
```
Criar um sistema de gerenciamento de clínica médica.
Preciso de:
- Tela de login
- Cadastro de pacientes (nome, CPF, data nascimento, telefone, email, endereço)
- Cadastro de médicos (nome, CRM, especialidade, telefone)
- Agendamento de consultas (paciente, médico, data, horário, status)
- Prontuário básico (observações da consulta)
- Dashboard (consultas do dia, pacientes ativos, faturamento)
- Usuário admin: admin@clinica.com / admin123
```

**Sistema de Academia:**
```
Criar um sistema de gerenciamento de academia.
Preciso de:
- Tela de login
- Cadastro de alunos (nome, CPF, data nascimento, telefone, email, plano)
- Controle de presença (check-in/check-out)
- Dashboard (alunos ativos, presença hoje, faturamento mensal)
- Usuário admin: admin@academia.com / admin123