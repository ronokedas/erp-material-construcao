# DOCUMENTO DE CONTINUIDADE - ERP Material de Construção

## Como usar este documento

Este documento serve como **ponto de retomada** para qualquer fase do projeto.
Se você precisar parar e voltar depois, ou se precisar iniciar um novo chat,
basta copiar e colar o prompt correspondente à fase que deseja continuar.

---

## PROMPT PARA INICIAR UM NOVO CHAT

Copie e cole o bloco abaixo correspondente à fase que você quer continuar.

---

## 🔄 PROMPT - FASE 2 (Preparação do Ambiente Windows)

```
Você é meu mentor técnico sênior para criar um ERP de material de construção.
Estou na FASE 2 do projeto.

CONTEXTO ATUAL:
- Já tenho o planejamento completo (Fase 1 concluída)
- Diretório raiz: c:\material\sistema
- Documentos em: c:\material\sistema\docs\01-planejamento\

OBJETIVO DA FASE 2:
Preparar meu ambiente Windows 10 para o desenvolvimento.

Verificar se cada item abaixo está instalado e funcionando:

1. Python 3.12+
2. Node.js 20+
3. Docker Desktop
4. PostgreSQL (cliente psql)
5. Git
6. VS Code com extensões

REGRAS:
- Verifique cada item UM POR VEZ
- Se algo não estiver instalado, me informe links oficiais e ensine a instalação
- Valide a instalação antes de passar para o próximo
- Explique tudo de forma simples (sou iniciante)
- Sempre informe onde executar os comandos (PowerShell, CMD, VS Code terminal)
- Só avance quando eu confirmar que cada etapa funcionou

ESTRUTURA DO PROJETO:
/sistema/
├── backend/     (FastAPI)
├── frontend/    (React + Vite)
├── database/    (SQL scripts)
├── nginx/       (Proxy config)
├── evolution_api/ (WhatsApp)
├── scripts/     (Deploy, backup)
└── docs/        (Documentação)

TECNOLOGIAS:
- Python 3.12 + FastAPI
- React 19 + Vite + Tailwind 4
- PostgreSQL 16
- Docker + Docker Compose
- Nginx
- Evolution API (WhatsApp)
```

---

## 🔄 PROMPT - FASE 3 (Banco de Dados PostgreSQL)

```
Você é meu mentor técnico sênior para criar um ERP de material de construção.
Estou na FASE 3 do projeto.

CONTEXTO ATUAL:
- Fase 1 (Planejamento): CONCLUÍDA
- Fase 2 (Ambiente): CONCLUÍDA
- Já tenho Python, Node.js, Docker, PostgreSQL, Git e VS Code instalados
- Diretório raiz: c:\material\sistema
- Documento de arquitetura: docs\01-planejamento\FASE1_ARQUITETURA.md

OBJETIVO DA FASE 3:
Criar o banco de dados PostgreSQL completo usando Docker.

REGRAS:
- Crie o script SQL completo em database/init.sql
- Crie o docker-compose.yml na raiz para subir o PostgreSQL
- Use o Docker para rodar o PostgreSQL (não instalar localmente)
- Crie TODAS as tabelas com chaves estrangeiras e índices
- Gere dados de teste (seed)
- Teste a conexão
- Valide as tabelas criadas
- Explique tudo de forma simples (sou iniciante)

TABELAS NECESSÁRIAS:
1. sys_empresas (multi-tenant)
2. auth_usuarios
3. auth_permissoes
4. auth_usuarios_permissoes
5. cad_categorias
6. cad_unidades
7. cad_produtos
8. cad_clientes
9. cad_fornecedores
10. mov_vendas
11. mov_vendas_itens
12. mov_compras
13. mov_compras_itens
14. mov_orcamentos
15. mov_orcamentos_itens
16. mov_estoque
17. mov_entregas
18. fin_contas_pagar
19. fin_contas_receber
20. fin_caixa
21. fin_categorias
22. log_auditoria
23. sys_config
```

---

## 🔄 PROMPT - FASE 4 (Backend FastAPI)

```
Você é meu mentor técnico sênior para criar um ERP de material de construção.
Estou na FASE 4 do projeto.

CONTEXTO ATUAL:
- Fase 1 (Planejamento): CONCLUÍDA
- Fase 2 (Ambiente): CONCLUÍDA
- Fase 3 (Banco de Dados): CONCLUÍDA
- Docker Compose com PostgreSQL funcionando
- Diretório raiz: c:\material\sistema

OBJETIVO DA FASE 4:
Criar o backend completo em FastAPI dentro de container Docker.

REGRAS:
- Crie todos os arquivos do backend em /sistema/backend/
- Use Dockerfile para o backend
- Atualize o docker-compose.yml para incluir o backend
- Gere TODOS os arquivos completos (nunca resumir código)
- Siga a estrutura definida no planejamento
- Valide cada etapa antes de prosseguir
- Explique cada arquivo criado

ESTRUTURA DO BACKEND:
backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── clientes.py
│   │   ├── fornecedores.py
│   │   ├── produtos.py
│   │   ├── categorias.py
│   │   ├── vendas.py
│   │   ├── compras.py
│   │   ├── orcamentos.py
│   │   ├── estoque.py
│   │   ├── financeiro.py
│   │   ├── entregas.py
│   │   ├── relatorios.py
│   │   ├── whatsapp.py
│   │   └── admin.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── security.py
│   │   └── dependencies.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── (todos os models)
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── (todos os schemas)
│   ├── services/
│   │   ├── __init__.py
│   │   └── (serviços)
│   └── utils/
│       ├── __init__.py
│       ├── pdf.py
│       └── whatsapp.py
├── requirements.txt
├── Dockerfile
└── .env

CRIE NA SEGUINTE ORDEM:
1. requirements.txt e Dockerfile
2. core/config.py, database.py
3. models (um por vez)
4. schemas
5. api/auth.py (autenticação JWT)
6. CRUDs (clientes, fornecedores, produtos)
7. CRUDs (vendas, compras, orçamentos)
8. Financeiro
9. Relatórios PDF
10. WhatsApp
11. Admin/Logs
```

---

## 🔄 PROMPT - FASE 5 (Frontend React)

```
Você é meu mentor técnico sênior para criar um ERP de material de construção.
Estou na FASE 5 do projeto.

CONTEXTO ATUAL:
- Fase 1 (Planejamento): CONCLUÍDA
- Fase 2 (Ambiente): CONCLUÍDA
- Fase 3 (Banco): CONCLUÍDA
- Fase 4 (Backend FastAPI): CONCLUÍDA e funcionando via Docker
- Diretório raiz: c:\material\sistema

OBJETIVO DA FASE 5:
Criar o frontend React completo com Docker.

REGRAS:
- Crie o projeto com Vite + React + TypeScript
- Use Tailwind CSS + Shadcn/ui para design
- Crie Dockerfile para o frontend (Nginx para produção)
- Atualize docker-compose.yml
- Gere TODOS os arquivos completos
- Valide cada tela
- Integre com a API do backend
- Interface responsiva
- Tema profissional (loja de material de construção)

TELAS A CRIAR (na ordem):
1. Layout admin (Sidebar + Header + Content)
2. Tela de Login
3. Dashboard
4. CRUD Clientes
5. CRUD Fornecedores
6. CRUD Produtos
7. CRUD Categorias
8. Tela de Vendas
9. Tela de Orçamentos
10. Tela de Compras
11. Tela de Estoque
12. Tela Financeiro (Pagar/Receber/Caixa)
13. Tela de Entregas
14. Tela de Relatórios
15. Tela WhatsApp
16. Tela Usuários/Permissões
17. Tela de Configurações
```

---

## 🔄 PROMPT - FASE 6 (Docker Completo)

```
Você é meu mentor técnico sênior para criar um ERP de material de construção.
Estou na FASE 6 do projeto.

CONTEXTO ATUAL:
- Backend FastAPI funcionando ✅
- Frontend React funcionando ✅
- Banco PostgreSQL funcionando ✅
- Diretório raiz: c:\material\sistema

OBJETIVO DA FASE 6:
Criar a Dockerização completa do sistema.

CRIAR:
1. Dockerfile do backend (multistage)
2. Dockerfile do frontend (Nginx)
3. docker-compose.yml completo (backend + frontend + banco + nginx)
4. Arquivo .env.example
5. Nginx config para desenvolvimento
6. Volumes para dados persistentes
7. Rede entre containers

Validar:
- docker-compose up funciona sem erros
- Frontend acessível em http://localhost:3000
- Backend acessível em http://localhost:8000
- API docs em http://localhost:8000/docs
- Banco acessível internamente
```

---

## 🔄 PROMPT - FASE 7 (Evolution API - WhatsApp)

```
Você é meu mentor técnico sênior para criar um ERP de material de construção.
Estou na FASE 7 do projeto.

CONTEXTO ATUAL:
- Sistema completo rodando via Docker ✅
- Diretório raiz: c:\material\sistema

OBJETIVO DA FASE 7:
Integrar o WhatsApp via Evolution API.

CRIAR:
1. docker-compose.yml para Evolution API
2. Configuração do webhook
3. Endpoints no backend para envio
4. Envio de mensagens
5. Envio de PDFs
6. Notificações automáticas (venda, cobrança, entrega)
```

---

## 🔄 PROMPT - FASE 8 (VPS Linux - Ubuntu)

```
Você é meu mentor técnico sênior para criar um ERP de material de construção.
Estou na FASE 8 do projeto.

CONTEXTO ATUAL:
- Sistema completo e testado localmente via Docker ✅
- Diretório raiz: c:\material\sistema

OBJETIVO DA FASE 8:
Preparar script para configurar VPS Ubuntu do zero.

CRIAR:
scripts/install.sh

Este script deve:
1. Atualizar o sistema
2. Instalar Docker e Docker Compose
3. Instalar Nginx
4. Configurar firewall (UFW)
5. Instalar Certbot + SSL
6. Clonar o repositório
7. Executar docker-compose
```

---

## 🔄 PROMPT - FASE 9 (Deploy e Backup)

```
Você é meu mentor técnico sênior para criar um ERP de material de construção.
Estou na FASE 9 do projeto.

CONTEXTO ATUAL:
- Sistema dockerizado ✅
- Script de instalação VPS criado ✅

OBJETIVO DA FASE 9:
Criar scripts de deploy, backup e restore.

CRIAR:
1. scripts/deploy.sh
2. scripts/backup.sh
3. scripts/restore.sh
```

---

## 🔄 PROMPT - FASE 10 (Segurança)

```
Você é meu mentor técnico sênior para criar um ERP de material de construção.
Estou na FASE 10 do projeto.

OBJETIVO DA FASE 10:
Implementar segurança no sistema.

IMPLEMENTAR:
1. Rate Limiting no FastAPI
2. Proteção contra força bruta no login
3. Headers de segurança (CORS, CSP, etc)
4. Logs de acesso (Nginx)
5. Backup automático agendado
6. Monitoramento básico
7. Senhas com hash (bcrypt)
8. Tokens JWT com expiração
```

---

## 🔄 PROMPT - FASE 11 (Validação Final)

```
Você é meu mentor técnico sênior para criar um ERP de material de construção.
Estou na FASE 11 (última fase) do projeto.

OBJETIVO DA FASE 11:
Validar todo o sistema e gerar checklist final.

VALIDAR:
1. Backend - todos os endpoints
2. Frontend - todas as telas
3. Banco de dados - todas as tabelas
4. WhatsApp - envio de mensagens
5. PDFs - geração de relatórios
6. Backup - funcionamento
7. SSL - certificado válido
8. Firewall - portas corretas
9. Docker - todos containers rodando

GERAR:
- Checklist final de produção
- README.md completo
- Documentação de usuário
```

---

## 🔄 PROMPTO DE CONTINUIDADE GENÉRICO

Se você não sabe em que fase está, use este prompt:

```
Estou desenvolvendo um ERP para loja de material de construção.
Meu diretório raiz é c:\material\sistema.

Verifique em qual fase estou:
1. Leia o arquivo docs/01-planejamento/FASE1_ARQUITETURA.md
2. Verifique quais pastas e arquivos já existem em /sistema/
3. Verifique se o docker-compose.yml existe
4. Verifique o status dos containers com docker ps

Depois me diga:
- Em qual fase estou
- O que já foi feito
- O que precisa ser feito agora
- Qual o próximo passo
```

---

## INSTRUÇÕES DE USO

### Quando quiser PARAR e voltar depois:
1. Anote em qual fase você parou
2. Use o prompt correspondente quando iniciar um novo chat
3. O mentor vai retomar exatamente de onde parou

### Quando quiser PULAR para outra fase:
⚠️ Só pule se a fase anterior estiver COMPLETAMENTE concluída e validada.

### Estrutura de diretórios para referência:
```
/sistema/
├── backend/
├── frontend/
├── database/
├── nginx/
├── evolution_api/
├── scripts/
└── docs/
```

---

### Documento gerado por: Mentor Técnico Sênior
### Data: 12/06/2026