# Manual de Implantação - VPS Linux

## Pré-requisitos

- Ubuntu 22.04/24.04 LTS ou Debian 12+
- Mínimo 2GB RAM, 2 vCPUs, 20GB disco
- Docker + Docker Compose
- Git

---

## Passo 1: Preparar o Servidor

```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependências
sudo apt install -y curl git ufw

# Configurar firewall
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker

# Verificar
docker --version
docker compose version
```

---

## Passo 2: Enviar o Código para o GitHub

> **Etapa feita no seu COMPUTADOR LOCAL, não no VPS.**

### 2.1 Criar repositório no GitHub

1. Acesse https://github.com
2. Clique no "+" no canto superior direito → "New repository"
3. Nome: `erp-material-construcao`
4. Selecione **Private** (recomendado)
5. NÃO marque "Add a README file"
6. Clique em "Create repository"

### 2.2 Enviar o código (no seu computador local)

Abra o terminal no seu computador (pasta onde está o projeto `sistema/`):

```bash
# Navegue até a pasta do projeto
cd caminho/para/sistema

# Inicialize o git
git init

# Adicione todos os arquivos
git add .

# Faça o primeiro commit
git commit -m "Primeiro commit - ERP Material de Construção"

# Defina o branch principal
git branch -M main

# Conecte ao repositório que você criou no GitHub
git remote add origin https://github.com/SEU_USUARIO/erp-material-construcao.git

# Envie o código
git push -u origin main
```

> **Substitua `SEU_USUARIO` pelo seu nome de usuário do GitHub.**
> Se pedir login, use seu email e uma **senha de aplicativo** (não a senha normal):
> GitHub → Settings → Developer settings → Personal access tokens → Generate new token

### 2.3 Clonar no VPS

Agora sim, conecte no VPS e clone:

```bash
ssh usuario@IP_DO_SEU_VPS
cd /home/usuario
git clone https://github.com/SEU_USUARIO/erp-material-construcao.git
cd erp-material-construcao
```

---

## Passo 3: Configurar Variáveis de Ambiente

```bash
cd sistema/backend
nano .env
```

Conteúdo do `.env`:
```env
APP_NAME=ERP Material de Construção
APP_VERSION=1.0.0
DEBUG=true
SECRET_KEY=CHAVE_SECRETA_AQUI_MUDE
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=480
CORS_ORIGINS=["http://localhost:5173","http://SEU_IP:5173","http://SEU_IP"]
DB_HOST=db
DB_PORT=5432
DB_NAME=erp_material
DB_USER=erp_user
DB_PASSWORD=SENHA_FORTE_BANCO_MUDE
```

Gerar chave secreta:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(64))"
```

---

## Passo 4: Criar docker-compose.prod.yml

```bash
cd sistema
nano docker-compose.prod.yml
```

Conteúdo:
```yaml
services:
  db:
    image: postgres:16-alpine
    container_name: erp_postgres
    restart: unless-stopped
    environment:
      POSTGRES_DB: erp_material
      POSTGRES_USER: erp_user
      POSTGRES_PASSWORD: ${DB_PASSWORD:-erp_pass_123}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./database/init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - erp_network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U erp_user -d erp_material"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
    container_name: erp_backend
    restart: unless-stopped
    ports:
      - "8000:8000"
    env_file:
      - ./backend/.env
    depends_on:
      db:
        condition: service_healthy
    networks:
      - erp_network

  frontend-build:
    image: node:20-alpine
    container_name: erp_frontend_build
    working_dir: /app
    volumes:
      - ./frontend:/app
      - frontend_dist:/app/dist
    command: sh -c "npm install && npm run build"

  frontend:
    image: nginx:alpine
    container_name: erp_frontend
    restart: unless-stopped
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - frontend_dist:/usr/share/nginx/html
    depends_on:
      - frontend-build
      - backend
    networks:
      - erp_network

volumes:
  postgres_data:
    driver: local
  frontend_dist:
    driver: local

networks:
  erp_network:
    driver: bridge
```

---

## Passo 5: Criar nginx.conf

```bash
nano nginx.conf
```

Conteúdo:
```nginx
server {
    listen 80;
    server_name _;

    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;
        proxy_connect_timeout 300s;
    }

    location /docs {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
    }

    location /openapi.json {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
    }

    location /redoc {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
    }

    client_max_body_size 50M;
}
```

---

## Passo 6: Criar Dockerfile.prod para o Backend

```bash
cd sistema/backend
nano Dockerfile.prod
```

Conteúdo:
```dockerfile
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
```

---

## Passo 7: Iniciar os Serviços

```bash
cd sistema

# Build e iniciar
docker compose -f docker-compose.prod.yml up --build -d

# Verificar se está rodando
docker compose -f docker-compose.prod.yml ps

# Ver logs
docker compose -f docker-compose.prod.yml logs -f
```

---

## Passo 8: Verificar o Funcionamento

```bash
# Testar backend
curl http://localhost:8000/

# Testar frontend
curl http://localhost/

# Testar API
curl http://localhost/api/dashboard
```

---

## Passo 9: Configurar SSL (HTTPS) - Opcional

### 9.1 Instalar Certbot
```bash
sudo apt install -y certbot python3-certbot-nginx
```

### 9.2 Obter certificado SSL
```bash
sudo certbot --nginx -d seu-dominio.com
```

### 9.3 Auto-renovação
```bash
sudo certbot renew --dry-run
```

---

## Comandos Úteis

```bash
# Parar tudo
docker compose -f docker-compose.prod.yml down

# Reiniciar
docker compose -f docker-compose.prod.yml restart

# Ver logs do backend
docker logs erp_backend -f

# Ver logs do frontend
docker logs erp_frontend -f

# Ver logs do banco
docker logs erp_postgres -f

# Backup do banco
docker exec erp_postgres pg_dump -U erp_user erp_material > backup.sql

# Restaurar banco
docker exec -i erp_postgres psql -U erp_user erp_material < backup.sql

# Atualizar código
git pull
docker compose -f docker-compose.prod.yml up --build -d
```

---

## Solução de Problemas

### Erro: "Method Not Allowed"
- Verifique se o backend está rodando: `docker logs erp_backend`

### Erro: "Connection refused"
- Verifique se o banco está saudável: `docker compose -f docker-compose.prod.yml ps`
- Verifique se o backend está rodando: `docker logs erp_backend`

### Erro: "Página em branco"
- Limpe o cache do navegador (Ctrl+Shift+R)
- Verifique se o frontend foi compilado: `docker logs erp_frontend_build`

### Erro: "CORS"
- Verifique o arquivo `.env` do backend, specifically `CORS_ORIGINS`
- Adicione o domínio/IP do frontend na lista

### Erro: "Banco de dados não encontrado"
- Verifique se o container do banco está rodando: `docker compose -f docker-compose.prod.yml ps`
- Verifique os logs: `docker logs erp_postgres`