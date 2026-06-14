# Manual Completo - ERP Material de Construção

## Guia para Leigos - Passo a Passo Detalhado

---

## ÍNDICE

1. [Resumo do que foi feito](#1-resumo)
2. [Tecnologias utilizadas](#2-tecnologias)
3. [Extensões do VS Code](#3-extensoes)
4. [Como tudo funciona](#4-como-funciona)
5. [Configurar o VPS Google Cloud](#5-vps)
6. [GitHub - Enviar o código](#6-github)
7. [Clonar e instalar no VPS](#7-instalar)
8. [Variáveis de ambiente (.env)](#8-env)
9. [Cloudflare - HTTPS gratuito](#9-cloudflare)
10. [Testar se tudo está funcionando](#10-testar)
11. [Backup e migração para outro VPS](#11-migracao)
12. [Comandos úteis](#12-comandos)
13. [Solução de problemas](#13-problemas)
14. [Credenciais de acesso](#14-credenciais)

---

## 1. Resumo do Que Foi Feito

### O fluxo completo (do início ao fim):

```
PASSO 1: Você abriu o VS Code no Windows
    │
    ├── Instalou extensões necessárias
    │
PASSO 2: Você pediu para eu criar o sistema ERP
    │
    ├── Eu criei o código (backend + frontend + banco)
    ├── Você testou localmente com Docker
    │
PASSO 3: Você criou uma conta no GitHub
    │
    ├── Criou um repositório (pasta online)
    ├── Enviou o código do Windows para o GitHub
    │
PASSO 4: Você criou um VPS no Google Cloud
    │
    ├── Abriu o SSH pelo navegador (sem senha!)
    ├── Instalou o Docker no VPS
    │
PASSO 5: Você clonou o código do GitHub para o VPS
    │
    ├── Docker construiu tudo automaticamente
    └── Sistema rodando em http://34.133.77.209
```

### Por que funcionou sem configurar banco de dados?

Quando você roda `docker compose up`, o Docker:
1. Cria um PostgreSQL (banco de dados) do zero
2. Roda o arquivo `init.sql` automaticamente
3. Esse arquivo cria 23 tabelas e insere dados de exemplo
4. Cria o usuário admin: `admin@erp.com.br` / `admin123`

**Isso só acontece na PRIMEIRA VEZ.** Depois, os dados ficam salvos no volume do Docker.

### Por que não precisou da senha do VPS?

O Google Cloud usa **chaves SSH** (arquivos criptografados) em vez de senhas. Quando você clica no botão "SSH" no navegador do Google Cloud:
1. Ele verifica que é você (conta Google)
2. Cria automaticamente uma chave de acesso
3. Conecta sem pedir senha

Isso é mais seguro que senha porque não pode ser adivinhada por hackers.

---

## 2. Tecnologias Utilizadas

### Resumo de cada tecnologia:

| Tecnologia | O que é | Para que serve | Análogia |
|------------|---------|----------------|----------|
| **VS Code** | Editor de código | Escrever e editar o código | Como o Word, mas para programação |
| **React** | Biblioteca JavaScript | Criar a interface visual do site | Como o Photoshop, mas para sites |
| **TypeScript** | Linguagem de programação | Escrever o código com segurança | Como o JavaScript, mas com regras |
| **Tailwind CSS** | Biblioteca de estilos | Deixar o site bonito | Como um kit de design pronto |
| **FastAPI** | Framework Python | Criar a API (backend) | Como o "cérebro" do sistema |
| **Python** | Linguagem de programação | Escrever o backend | Linguagem popular e fácil |
| **PostgreSQL** | Banco de dados | Guardar clientes, produtos, vendas | Como uma planilha gigante e segura |
| **SQLAlchemy** | Biblioteca Python | Conectar o Python ao banco | Como um "tradutor" entre Python e SQL |
| **Pydantic** | Biblioteca Python | Validar dados | Como um " fiscal" que verifica informações |
| **Docker** | Plataforma de containers | Empacotar tudo junto | Como uma caixa com tudo dentro |
| **Docker Compose** | Ferramenta Docker | Criar vários containers | Como uma "receita de bolo" |
| **Nginx** | Servidor web | Entregar páginas e redirecionar API | Como um "porteiro" |
| **Node.js** | Runtime JavaScript | Rodar ferramentas do frontend | Como o motor do React |
| **Vite** | Ferramenta de build | Compilar o frontend rapidamente | Como uma "fábrica" de sites |
| **Git** | Controle de versão | Rastrear mudanças no código | Como um "histórico" do projeto |
| **GitHub** | Repositório online | Guardar o código na nuvem | Como o Google Drive para código |
| **SSH** | Protocolo de acesso | Conectar no VPS remotamente | Como um "controle remoto" seguro |
| **Cloudflare** | CDN e proxy | HTTPS gratuito e proteção | Como um "escudo" para o site |
| **Google Cloud** | Servidor na nuvem | Hospedar o sistema | Como um "computador alugado" |

### Versões utilizadas:

- Python 3.12
- Node.js 20
- PostgreSQL 16
- React 19
- Vite 8
- Docker + Docker Compose

---

## 3. Extensões do VS Code

### Extensões que você instalou:

| Extensão | O que faz | Por que precisa |
|----------|-----------|-----------------|
| **Python** (Microsoft) | Suporte a Python | Para escrever o backend |
| **Pylance** | Autocomplete Python | Para o VS Code entender o código Python |
| **ES7+ React/Redux/React-Native** | Snippets React | Para criar componentes React rápido |
| **Tailwind CSS IntelliSense** | Autocomplete Tailwind | Para usar classes CSS do Tailwind |
| **ESLint** | Verificar erros | Para encontrar bugs no código |
| **Prettier** | Formatador de código | Para o código ficar organizado |
| **Docker** | Suporte Docker | Para gerenciar containers |
| **Thunder Client** ou **Postman** | Testar API | Para testar se a API funciona |

### Como instalar extensões:

1. Abra o VS Code
2. Pressione `Ctrl + Shift + X` (abre a aba de extensões)
3. Digite o nome da extensão
4. Clique em "Install"

---

## 4. Como Tudo Funciona

### Arquitetura do sistema:

```
NAVEGADOR do usuário
    │
    │ http://seu-dominio.com (porta 80)
    │
    ▼
NGINX (servidor web)
    │
    ├── Se é página (HTML/CSS/JS) → Entrega o arquivo
    │
    ├── Se é API (/api/...) → Redireciona para o Backend
    │
    ▼
BACKEND FastAPI (porta 8000 internamente)
    │
    ├── Recebe a requisição
    ├── Valida os dados
    ├── Consulta o banco
    │
    ▼
POSTGRESQL (banco de dados)
    │
    ├── Retorna os dados
    └── Backend retorna JSON para o Nginx
```

### Como o login funciona:

```
1. Usuário digita email e senha
2. Frontend envia para /api/auth/login
3. Backend verifica no banco de dados
4. Se correto → retorna um "token" (crachá digital)
5. Frontend guarda o token no navegador
6. Toda requisição futura inclui o token
7. Backend verifica o token antes de processar
```

### O que é um container Docker?

Imagine que você tem um programa que precisa de 10 dependências para funcionar. Sem Docker, você precisaria instalar todas essas 10 dependências no seu computador, e pode dar conflito com outros programas.

Com Docker, você coloca tudo dentro de uma "caixa" (container) que:
- Tem tudo que o programa precisa
- Não conflita com outros programas
- Pode ser ligada/desligada facilmente
- Pode ser copiada para outro computador

```
SEU COMPUTADOR
├── Container 1: PostgreSQL (banco)
│   ├── Tem seu próprio Python
│   ├── Tem seu próprio PostgreSQL
│   └── Tem seus próprios dados
│
├── Container 2: Backend (API)
│   ├── Tem seu próprio Python
│   ├── Tem suas dependências
│   └── Roda o FastAPI
│
└── Container 3: Frontend (site)
    ├── Tem seu próprio Node.js
    ├── Tem seus arquivos HTML/CSS/JS
    └── Roda o Nginx
```

---

## 5. Configurar o VPS no Google Cloud

### 5.1 Criar a instância

1. Acesse https://console.cloud.google.com
2. Vá em **Compute Engine → VM instances**
3. Clique em **Create Instance**
4. Configure:
   - **Nome:** `erp-vps`
   - **Região:** Escolha a mais perto do Brasil
   - **Machine type:** `e2-medium` (2 vCPUs, 4GB RAM)
   - **Boot disk:** Ubuntu 22.04 LTS
   - **Firewall:** Marque "Allow HTTP traffic"
5. Clique em **Create**

### 5.2 Conectar via SSH

1. Na lista de instâncias, clique no botão **SSH**
2. Uma janela do navegador abre com o terminal
3. Você verá algo como: `ronokedas2020@instance-20260613-214636:~$`

**Por que não pede senha?**
O Google Cloud usa **chaves SSH** (arquivos criptografados):
- Uma chave **pública** fica no VPS
- Uma chave **privada** fica no seu navegador
- Quando conecta, ele verifica as chaves
- É como uma "senha mágica" que só funciona naquele computador

### 5.3 Liberar portas no firewall

No Google Cloud, acesse: **VPC Network → Firewall → Create firewall rule**

Crie uma regra:

| Campo | Valor | O que significa |
|-------|-------|-----------------|
| Name | `allow-http` | Nome da regra |
| Direction | Ingress | Tráfego entrando |
| Priority | 1000 | Prioridade (menor = mais importante) |
| Source IP ranges | `0.0.0.0/0` | Qualquer IP do mundo |
| Protocols and ports | `tcp:80` | Porta HTTP |

**Portas que você PRECISA liberar:**

| Porta | Protocolo | O que faz | Obrigatório? |
|-------|-----------|-----------|--------------|
| **22** | TCP | SSH (controle remoto) | Sim (já vem aberta) |
| **80** | TCP | HTTP (site) | Sim |
| **443** | TCP | HTTPS (site seguro) | Não (Cloudflare cuida) |

**Portas que NÃO precisa liberar:**

| Porta | O que é | Por que não liberar |
|-------|---------|---------------------|
| **5432** | PostgreSQL | Fica escondido dentro do Docker |
| **8000** | Backend API | Fica escondido atrás do Nginx |
| **5173** | Frontend dev | Só usa em desenvolvimento |

### 5.4 Instalar Docker no VPS

Cole estes comandos no terminal do SSH:

```bash
# Atualiza o sistema (instala atualizações de segurança)
sudo apt update && sudo apt upgrade -y
```
**O que faz:** Baixa e instala as últimas versões de todos os programas do sistema. É como atualizar o Windows.

```bash
# Instala dependências (programas que o Docker precisa)
sudo apt install -y curl git ufw
```
**O que faz:** Instala 3 programas:
- `curl`: Para baixar arquivos da internet
- `git`: Para controlar versões do código
- `ufw`: Para gerenciar o firewall

```bash
# Instala o Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```
**O que faz:** Baixa o instalador do Docker e executa. É como baixar um .exe e instalar.

```bash
# Adiciona seu usuário ao grupo docker (para usar sem sudo)
sudo usermod -aG docker $USER
newgrp docker
```
**O que faz:** Permite que você rode comandos Docker sem precisar de sudo (administrador). É como dar permissão de administrador para o Docker.

```bash
# Verifica se o Docker está instalado
docker --version
docker compose version
```
**O que faz:** Mostra a versão do Docker instalado. Se aparecer algo como "Docker version 24.x", está tudo certo.

---

## 6. GitHub - Enviar o Código

### 6.1 Criar conta no GitHub

1. Acesse https://github.com
2. Clique em **Sign up**
3. Preencha email, senha e nome de usuário
4. Confirme o email

### 6.2 Criar repositório

1. Clique no "+" no canto superior direito
2. Clique em **New repository**
3. Preencha:
   - **Repository name:** `erp-material-construcao`
   - **Description:** "Sistema ERP para loja de material de construção"
   - **Visibility:** Private (recomendado)
4. NÃO marque "Add a README file"
5. Clique em **Create repository**

### 6.3 Configurar Git no Windows

Abra o **PowerShell** como administrador:

```powershell
# Configura seu nome (aparece nos commits)
git config --global user.name "seu-nome"
```
**O que faz:** Salva seu nome para que o Git saiba quem fez cada mudança.

```powershell
# Configura seu email (aparece nos commits)
git config --global user.email "seu-email@gmail.com"
```
**O que faz:** Salva seu email para identificação.

### 6.4 Enviar o código

Navegue até a pasta do projeto no PowerShell:

```powershell
# Vá até a pasta do projeto
cd C:\material
```
**O que faz:** Entra na pasta onde está o código.

```powershell
# Inicializa o Git nesta pasta
git init
```
**O que faz:** Cria uma pasta oculta `.git` que controla versões. É como ligar o "controle remoto" para esta pasta.

```powershell
# Seleciona todos os arquivos para enviar
git add .
```
**O que faz:** Marca todos os arquivos para serem enviados. O "." significa "tudo aqui".

```powershell
# Salva uma "foto" do estado atual
git commit -m "Primeiro commit - ERP Material de Construcao"
```
**O que faz:** Salva uma cópia dos arquivos. É como salvar um jogo - você pode voltar a esse ponto depois. A mensagem descreve o que foi feito.

```powershell
# Conecta ao repositório do GitHub
git remote add origin https://github.com/SEU-USUARIO/erp-material-construcao.git
```
**O que faz:** Diz ao Git o endereço do repositório no GitHub. "origin" é o nome dado ao destino.

```powershell
# Envia o código para o GitHub
git push -u origin main
```
**O que faz:** Envia todos os arquivos para o GitHub. O "-u" faz o Git lembrar esse destino para futuros envios.

### 6.5 Senha de aplicativo do GitHub

Quando faz `git push`, o GitHub pode pedir uma "senha de aplicativo":

1. Acesse https://github.com/settings/tokens
2. Clique em **Generate new token (classic)**
3. Dê um nome (ex: "meu-pc")
4. Em **Expiration**, selecione "No expiration"
5. Marque a caixa **repo**
6. Clique em **Generate token**
7. **COPIE O TOKEN** (aparece só uma vez!)

**Por que não usa a senha normal?**
O GitHub não permite mais login com senha via terminal. A "senha de aplicativo" é uma senha específica que pode ser revogada sem mudar sua senha principal.

---

## 7. Clonar e Instalar no VPS

### 7.1 Conectar no VPS

Pelo console do Google Cloud, clique em **SSH** na instância.

### 7.2 Clonar o código

```bash
# Vá até a pasta do usuário
cd /home/ronokedas2020
```
**O que faz:** Entra na pasta pessoal do usuário.

```bash
# Baixa o código do GitHub
git clone https://github.com/SEU-USUARIO/erp-material-construcao.git
```
**O que faz:** Faz o download de todo o repositório do GitHub para o VPS. É como baixar uma pasta zipada.

```bash
# Entra na pasta do projeto
cd erp-material-construcao
```
**O que faz:** Muda para dentro da pasta do projeto.

### 7.3 Criar arquivo .env

```bash
# Entra na pasta do backend
cd sistema/backend

# Cria o arquivo .env
nano .env
```
**O que faz:** Abre o editor de texto nano para criar o arquivo de configuração.

Cole este conteúdo:
```env
APP_NAME=ERP Material de Construcao
APP_VERSION=1.0.0
DEBUG=true
SECRET_KEY=COLOQUE_UMA_CHAVE_FORTE_AQUI
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=480
CORS_ORIGINS=["http://localhost:5173","http://34.133.77.209"]
DB_HOST=db
DB_PORT=5432
DB_NAME=erp_material
DB_USER=erp_user
DB_PASSWORD=MINHA_SENHA_FORTE_123
```

Para salvar: Pressione `Ctrl + O`, depois `Enter`, depois `Ctrl + X`.

### 7.4 Gerar chave secreta

```bash
# Volte para a pasta do projeto
cd ..

# Gere uma chave secreta
python3 -c "import secrets; print(secrets.token_urlsafe(64))"
```
**O que faz:** Gera uma string aleatória segura. Copie a saída e cole no lugar de `COLOQUE_UMA_CHAVE_FORTE_AQUI` no arquivo `.env`.

### 7.5 Criar docker-compose.prod.yml

```bash
# Entra na pasta sistema
cd sistema

# Cria o arquivo de produção
nano docker-compose.prod.yml
```

Cole o conteúdo do arquivo (está no manual de deploy).

### 7.6 Criar nginx.conf

```bash
# Cria o arquivo de configuração do Nginx
nano nginx.conf
```

Cole o conteúdo do arquivo (está no manual de deploy).

### 7.7 Criar Dockerfile.prod

```bash
# Entra na pasta do backend
cd backend

# Cria o Dockerfile de produção
nano Dockerfile.prod
```

Cole o conteúdo do arquivo (está no manual de deploy).

### 7.8 Iniciar tudo

```bash
# Volte para a pasta sistema
cd ..

# Build e inicia todos os containers
docker compose -f docker-compose.prod.yml up --build -d
```

**O que cada parte significa:**

| Comando | O que faz |
|---------|-----------|
| `docker compose` | Comando do Docker Compose |
| `-f docker-compose.prod.yml` | Usa este arquivo de configuração |
| `up` | Liga os containers |
| `--build` | Reconstrói tudo (compila frontend e backend) |
| `-d` | Roda em segundo plano (pode fechar o terminal) |

**O que acontece quando roda esse comando:**

```
1. PostgreSQL
   ├── Baixa a imagem postgres:16-alpine
   ├── Cria o container
   ├── Cria o banco de dados
   ├── Executa init.sql (23 tabelas + dados)
   └── Pronto! Banco configurado automaticamente

2. Backend
   ├── Baixa a imagem python:3.12-slim
   ├── Instala dependências Python
   ├── Copia o código
   ├── Roda uvicorn (servidor da API)
   └── Pronto! API rodando na porta 8000

3. Frontend (build)
   ├── Baixa a imagem node:20-alpine
   ├── Instala dependências npm
   ├── Compila o frontend (npm run build)
   └── Pronto! Arquivos HTML/CSS/JS gerados

4. Frontend (nginx)
   ├── Baixa a imagem nginx:alpine
   ├── Copia os arquivos compilados
   ├── Configura o proxy reverso
   └── Pronto! Site rodando na porta 80
```

---

## 8. Variáveis de Ambiente (.env)

### O que é o arquivo .env?

O `.env` é como uma "ficha de cadastro" do sistema. Ele diz ao backend:
- Qual é o nome do banco de dados
- Qual é a senha do banco
- Qual é a chave de segurança

### Quando preciso alterar o .env?

| Situação | Precisa alterar? |
|----------|-----------------|
| Primeira instalação | Sim, configure as senhas |
| Mudar de domínio | Sim, atualize CORS_ORIGINS |
| Mudar senha do banco | Sim, atualize DB_PASSWORD |
| Migrar para outro VPS | Não, o .env vai junto |

### Se você não mudou nada além do SECRET_KEY

Se você só mudou o `SECRET_KEY` e deixou o resto igual ao exemplo:
- **DB_HOST=db** → Funciona porque o Docker cria um container chamado "db"
- **DB_NAME=erp_material** → Funciona porque o init.sql cria esse banco
- **DB_USER=erp_user** → Funciona porque o init.sql cria esse usuário
- **DB_PASSWORD=MINHA_SENHA_FORTE_123** → Funciona porque é a mesma do docker-compose

**Onde são usados esses dados:**
- `DB_HOST=db` → O Docker usa o nome "db" para encontrar o container do banco
- `DB_NAME=erp_material` → O init.sql cria esse banco automaticamente
- `DB_USER=erp_user` → O init.sql cria esse usuário automaticamente
- `DB_PASSWORD` → Deve ser igual à `POSTGRES_PASSWORD` do docker-compose

### Se você mudar o banco no VPS

Se você alterar `DB_NAME`, `DB_USER` ou `DB_PASSWORD` no `.env`:
1. O backend vai tentar conectar com os novos dados
2. Se o banco não existir, vai dar erro
3. Você precisaria criar o banco manualmente

**Recomendação:** Não altere esses valores. O `init.sql` já configura tudo automaticamente.

---

## 9. Cloudflare - HTTPS Gratuito

### O que é Cloudflare?

O Cloudflare é um serviço gratuito que:
- **Protege** seu site de ataques
- **Acelera** o carregamento
- **Fornece HTTPS** (cadeado verde) grátis
- **Esconde** o IP do seu VPS

### Como configurar:

1. Acesse https://cloudflare.com e crie uma conta
2. Adicione seu domínio (ex: `erpminhaloja.com.br`)
3. O Cloudflare vai pedir para mudar os nameservers do seu domínio
4. No painel do Cloudflare, vá em **DNS → Records**
5. Crie um registro:

| Type | Name | Content | Proxy |
|------|------|---------|-------|
| A | @ | 34.133.77.209 | DNS only (cinza) |

Ou para subdomínio:

| Type | Name | Content | Proxy |
|------|------|---------|-------|
| A | erp | 34.133.77.209 | DNS only (cinza) |

### SSL/HTTPS no Cloudflare

**Você NÃO precisa instalar SSL no Nginx!** O Cloudflare cuida disso:

```
Usuário → https://erp.com.br (HTTPS via Cloudflare)
              │
              │ Cloudflare descriptografa
              │
              ▼
         Nginx (porta 80, HTTP)
              │
              │ Nginx processa
              │
              ▼
         Backend (porta 8000)
```

**O que o Cloudflare faz:**
1. Usuário acessa `https://erp.com.br`
2. Cloudflare recebe a requisição (HTTPS)
3. Cloudflare descriptografa (HTTP)
4. Cloudflare envia para seu VPS (HTTP, porta 80)
5. Seu VPS responde
6. Cloudflare criptografa a resposta
7. Usuário recebe a resposta (HTTPS)

### O que o usuário vê no navegador?

O usuário vê **APENAS o domínio** que ele digitou:
- `https://erpminhaloja.com` ou
- `https://erp.com.br`

**NÃO aparece** o IP do VPS (34.133.77.209) no navegador.

Isso acontece porque:
1. O DNS traduz o domínio para o IP
2. O navegador mostra o domínio, não o IP
3. O Cloudflare esconde o IP real

---

## 10. Testar se Tudo Está Funcionando

### 10.1 Testar o Docker

```bash
# Lista os containers rodando
docker compose -f docker-compose.prod.yml ps
```
**Esperado:** Todos os containers com status "Up"

### 10.2 Testar o backend

```bash
# Testa se a API está respondendo
curl http://localhost:8000/
```
**Esperado:** JSON com nome e versão do sistema

### 10.3 Testar o banco de dados

```bash
# Lista os bancos de dados
docker exec erp_postgres psql -U erp_user -l
```
**Esperado:** Lista mostrando o banco "erp_material"

### 10.4 Testar as tabelas

```bash
# Lista as tabelas do banco
docker exec erp_postgres psql -U erp_user -d erp_material -c "\dt"
```
**Esperado:** Lista com 23 tabelas

### 10.5 Testar o usuário admin

```bash
# Verifica se o usuário admin existe
docker exec erp_postgres psql -U erp_user -d erp_material -c "SELECT email, nome FROM auth_usuarios;"
```
**Esperado:** Linha com `admin@erp.com.br` e `Administrador`

### 10.6 Testar o frontend

```bash
# Testa se o site está funcionando
curl http://localhost/
```
**Esperado:** HTML da página de login

### 10.7 Testar pelo navegador

1. Abra o navegador
2. Acesse `http://34.133.77.209` (ou seu domínio)
3. Deve aparecer a tela de login
4. Faça login com `admin@erp.com.br` / `admin123`

### 10.8 Testar a API pelo navegador

1. Abra `http://34.133.77.209/api/dashboard` no navegador
2. Deve retornar um JSON com métricas

---

## 11. Backup e Migração para Outro VPS

### 11.1 Fazer backup no VPS atual

```bash
# Backup do banco de dados
docker exec erp_postgres pg_dump -U erp_user erp_material > backup_banco.sql
```
**O que faz:** Extrai todos os dados do banco e salva em um arquivo .sql

```bash
# Backup dos arquivos do projeto
tar -czf backup_projeto.tar.gz erp-material-construcao/
```
**O que faz:** Compacta todos os arquivos do projeto em um arquivo .tar.gz

### 11.2 Baixar o backup para o Windows

No PowerShell do Windows:
```powershell
# Baixa o backup do banco
scp ronokedas2020@34.133.77.209:backup_banco.sql C:\backup\

# Baixa o backup dos arquivos
scp ronokedas2020@34.133.77.209:backup_projeto.tar.gz C:\backup\
```
**O que faz:** Copia os arquivos do VPS para o seu computador via SCP (Secure Copy).

### 11.3 Instalar no novo VPS

1. Siga os passos 5 e 6 deste manual (criar VPS, instalar Docker)
2. Antes de iniciar os containers, restaure o backup:

```bash
# Entra no projeto
cd /home/ronokedas2020

# Clone o projeto novamente
git clone https://github.com/ronokedas/erp-material-construcao.git
cd erp-material-construcao

# Restaure o backup do banco (deixe o VPS atual rodando)
scp ronokedas2020@34.133.77.209:/home/ronokedas2020/backup_banco.sql .

# Inicie os containers
docker compose -f docker-compose.prod.yml up --build -d

# Aguarde o banco inicializar (uns 30 segundos)
sleep 30

# Restaure o backup no novo banco
docker exec -i erp_postgres psql -U erp_user erp_material < backup_banco.sql
```

**O que acontece:**
1. O Docker cria o banco novo com as tabelas vazias
2. O comando `psql` importa os dados do backup
3. Todos os clientes, produtos, vendas e usuários são restaurados

### 11.4 Verificar se a migração funcionou

```bash
# Verifica se os dados foram restaurados
docker exec erp_postgres psql -U erp_user -d erp_material -c "SELECT COUNT(*) FROM cad_clientes;"
docker exec erp_postgres psql -U erp_user -d erp_material -c "SELECT COUNT(*) FROM cad_produtos;"
docker exec erp_postgres psql -U erp_user -d erp_material -c "SELECT COUNT(*) FROM mov_vendas;"
```

### 11.5 Parar o VPS antigo (depois de confirmar)

```bash
# No VPS antigo, pare os containers
docker compose -f docker-compose.prod.yml down
```

---

## 12. Comandos Úteis

### Gerenciamento de containers

| Comando | O que faz |
|---------|-----------|
| `docker compose -f docker-compose.prod.yml up -d` | Liga os containers |
| `docker compose -f docker-compose.prod.yml down` | Para e remove os containers |
| `docker compose -f docker-compose.prod.yml restart` | Reinicia os containers |
| `docker compose -f docker-compose.prod.yml ps` | Lista containers rodando |
| `docker compose -f docker-compose.prod.yml logs -f` | Mostra logs em tempo real |
| `docker compose -f docker-compose.prod.yml up --build -d` | Reconstrói e inicia |

### Gerenciamento de imagens Docker

| Comando | O que faz |
|---------|-----------|
| `docker images` | Lista imagens baixadas |
| `docker rmi NOME` | Remove uma imagem |
| `docker system prune` | Remove imagens não utilizadas |

### Gerenciamento de volumes

| Comando | O que faz |
|---------|-----------|
| `docker volume ls` | Lista volumes |
| `docker volume inspect NOME` | Mostra detalhes do volume |
| `docker volume rm NOME` | Remove um volume |

### Backup e restore

| Comando | O que faz |
|---------|-----------|
| `docker exec erp_postgres pg_dump -U erp_user erp_material > backup.sql` | Backup do banco |
| `docker exec -i erp_postgres psql -U erp_user erp_material < backup.sql` | Restore do banco |

### Git

| Comando | O que faz |
|---------|-----------|
| `git pull` | Baixa atualizações do GitHub |
| `git add .` | Seleciona todos os arquivos |
| `git commit -m "mensagem"` | Salva uma "foto" do código |
| `git push` | Envia para o GitHub |
| `git status` | Mostra o estado atual |

---

## 13. Solução de Problemas

### Erro: "Method Not Allowed"
**Causa:** O backend não está rodando
**Solução:** `docker logs erp_backend`

### Erro: "Connection refused"
**Causa:** O banco não está pronto
**Solução:** `docker compose -f docker-compose.prod.yml ps`

### Erro: "Página em branco"
**Causa:** Cache do navegador
**Solução:** Pressione `Ctrl + Shift + R`

### Erro: "CORS"
**Causa:** O frontend não está na lista de origens
**Solução:** Adicione o IP no `.env`:
```env
CORS_ORIGINS=["http://34.133.77.209"]
```

### Erro: "Banco de dados não encontrado"
**Causa:** O container do banco não está rodando
**Solução:**
```bash
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up --build -d
```

### Erro: "Permission denied"
**Causa:** Falta permissão para acessar arquivos
**Solução:**
```bash
sudo chmod -R 755 sistema/
```

### Erro: "No space left on device"
**Causa:** Disco cheio
**Solução:**
```bash
docker system prune -a
```

---

## 14. Credenciais de Acesso

### Usuário administrador

| Campo | Valor |
|-------|-------|
| **E-mail** | `admin@erp.com.br` |
| **Senha** | `admin123` |

### Banco de dados

| Campo | Valor |
|-------|-------|
| **Host** | `db` (nome do container) |
| **Porta** | `5432` |
| **Banco** | `erp_material` |
| **Usuário** | `erp_user` |
| **Senha** | `MINHA_SENHA_FORTE_123` |

### Empresa padrão

| Campo | Valor |
|-------|-------|
| **Nome** | Empresa Padrão Ltda |
| **Nome fantasia** | Minha Loja |
| **CNPJ** | 00.000.000/0001-00 |

---

## 15. Atualizar o Sistema (Windows → GitHub → VPS)

### O fluxo de atualização:

```
Seu Windows 10                    GitHub                    VPS Linux
(código local)                  (nuvem)                    (servidor)
     │                            │                            │
     ├── Edita o código ──────────►│                            │
     │                            │                            │
     ├── git add . ───────────────►│                            │
     ├── git commit ──────────────►│                            │
     ├── git push ────────────────►│                            │
     │                            │                            │
     │                            │◄── git pull ───────────────┤
     │                            │                            │
     │                            │                     docker compose up --build
     │                            │                     Sistema atualizado!
```

### Passo a passo completo:

#### 1. No Windows - Edite o código

Abra o VS Code e faça as alterações que quiser:
- Adicionar novos módulos
- Corrigir bugs
- Melhorar o design
- Adicionar novas funcionalidades

#### 2. No Windows - Envie para o GitHub

Abra o PowerShell na pasta do projeto:

```powershell
# 1. Veja o que mudou
git status
```
**O que faz:** Mostra quais arquivos foram alterados, criados ou deletados.

```powershell
# 2. Adicione todos os arquivos alterados
git add .
```
**O que faz:** Seleciona todos os arquivos que mudaram para serem enviados.

```powershell
# 3. Salve uma "foto" com descrição do que mudou
git commit -m "Adicionei módulo de relatórios"
```
**O que faz:** Salva uma cópia dos arquivos com uma mensagem descrevendo o que foi feito. Use mensagens claras como:
- `"Adicionei módulo de relatórios"`
- `"Corrigi bug no login"`
- `"Melhorei o design da página de clientes"`

```powershell
# 4. Envie para o GitHub
git push
```
**O que faz:** Envia as mudanças para o GitHub. O GitHub agora tem a versão mais recente do código.

#### 3. No VPS - Atualize o código

Conecte no VPS pelo SSH do Google Cloud:

```bash
# 1. Entre na pasta do projeto
cd /home/ronokedas2020/erp-material-construcao
```
**O que faz:** Entra na pasta onde o código está no VPS.

```bash
# 2. Baixe as atualizações do GitHub
git pull
```
**O que faz:** Baixa todas as mudanças que você fez no Windows e enviou para o GitHub. É como "sincronizar" o VPS com o GitHub.

```bash
# 3. Reconstrua e reinicie os containers
docker compose -f docker-compose.prod.yml up --build -d
```
**O que faz:** 
- `--build` = Reconstrói as imagens Docker com o código novo
- `up` = Liga os containers
- `-d` = Roda em segundo plano

**O que acontece:**
```
1. Docker baixa as novas imagens
2. Compila o frontend com o código novo
3. Reinicia o backend com o código novo
4. O banco de dados NÃO é afetado (os dados ficam salvos)
5. Sistema atualizado!
```

#### 4. Verifique se funcionou

```bash
# Verifique os logs
docker logs erp_backend -f
```

Abra o navegador e acesse `http://34.133.77.209` (ou seu domínio).

### Resumo rápido (copie e cole):

**No Windows (PowerShell):**
```powershell
git add .
git commit -m "Sua mensagem aqui"
git push
```

**No VPS (SSH):**
```bash
cd /home/ronokedas2020/erp-material-construcao
git pull
docker compose -f docker-compose.prod.yml up --build -d
```

### O que NÃO muda ao atualizar:

| O que muda | O que NÃO muda |
|------------|----------------|
| Código do frontend | Dados do banco (clientes, produtos, vendas) |
| Código do backend | Senhas dos usuários |
| Configurações novas | Configurações do .env |
| Novos módulos | Dados de exemplo |

### Se adicionar novas tabelas no banco:

Se você criar novas tabelas no banco de dados (ex: tabela de "notas fiscais"), você precisa:

1. Adicionar o script SQL no arquivo `init.sql`
2. Enviar para o GitHub (`git add . && git commit && git push`)
3. No VPS, execute o script SQL manualmente:

```bash
# Execute o script SQL no banco
docker exec -i erp_postgres psql -U erp_user -d erp_material < sistema/database/init.sql
```

**O que faz:** Executa o script SQL no banco de dados. Como o `init.sql` usa `CREATE TABLE IF NOT EXISTS`, ele só cria tabelas que não existem. As tabelas existentes não são afetadas.

### Se adicionar novos endpoints na API:

1. Crie o novo arquivo de rota (ex: `app/api/notas_fiscais.py`)
2. Registre a rota no `app/main.py`
3. Envie para o GitHub
4. No VPS, faça `git pull` e `docker compose up --build -d`

### Se adicionar novas páginas no frontend:

1. Crie o novo componente (ex: `src/pages/NotasFiscais.tsx`)
2. Adicione a rota no `App.tsx`
3. Adicione o item no menu do `Layout.tsx`
4. Envie para o GitHub
5. No VPS, faça `git pull` e `docker compose up --build -d`

---

## Resumo Final

### O que você fez:

1. **Instalou o VS Code** + extensões para programar
2. **Criou o sistema ERP** com React (frontend) + FastAPI (backend) + PostgreSQL (banco)
3. **Testou localmente** com Docker no Windows
4. **Enviou para o GitHub** (nuvem)
5. **Criou um VPS** no Google Cloud (servidor)
6. **Instalou o Docker** no VPS
7. **Clonou o código** do GitHub para o VPS
8. **Rodou o Docker** que criou tudo automaticamente
9. **Configurou o Cloudflare** para HTTPS gratuito
10. **Sistema rodando** em http://34.133.77.209

### Para criar novos sistemas no futuro:

1. Siga os mesmos passos deste manual
2. Troque o código do ERP pelo novo sistema
3. Mantenha a mesma estrutura (backend + frontend + banco)
4. Use Docker para facilitar a instalação
5. Use GitHub para versionar
6. Use Cloudflare para HTTPS gratuito