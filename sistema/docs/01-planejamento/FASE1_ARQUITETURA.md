# ERP PARA LOJA DE MATERIAL DE CONSTRUÇÃO
## FASE 1 - Planejamento Completo do Sistema

---

## 1. VISÃO GERAL DO SISTEMA

### 1.1 Objetivo
Criar um ERP profissional para lojas de materiais de construção, com:
- Gestão completa de vendas, estoque, financeiro
- Relatórios em PDF
- Integração com WhatsApp via Evolution API
- Sistema multiempresa
- Docker do início ao fim

### 1.2 Tecnologias Utilizadas

| Camada | Tecnologia | Versão | Motivo |
|--------|------------|--------|--------|
| Backend | Python + FastAPI | Python 3.12+ | Performance, tipagem forte, async |
| Banco | PostgreSQL | 16 | Robusto, relacional, gratuito |
| Frontend | React + Vite | React 19 | Velocidade, componentes, ecossistema |
| UI | Tailwind CSS + Shadcn/ui | Tailwind 4 | Design moderno, responsivo |
| Autenticação | JWT + OAuth2 | - | Segurança, padrão mercado |
| PDF | ReportLab / WeasyPrint | - | Geração nativa de PDFs |
| WhatsApp | Evolution API | 2.x | Open source, self-hosted |
| Container | Docker + Docker Compose | - | Portabilidade total |
| Proxy | Nginx | - | SSL, proxy reverso |
| SSL | Certbot + Let's Encrypt | - | HTTPS gratuito |

---

## 2. ARQUITETURA DO SISTEMA

```
┌─────────────────────────────────────────────────────────┐
│                     INTERNET                            │
└──────────┬────────────────────────────────────┬─────────┘
           │                                    │
    ┌──────▼──────┐                    ┌────────▼────────┐
    │   Nginx      │                    │  Evolution API  │
    │  Proxy SSL   │                    │   (WhatsApp)    │
    └──────┬──────┘                    └────────┬────────┘
           │                                    │
    ┌──────▼──────┐                             │
    │  Frontend   │                             │
    │  React +    │                             │
    │  Vite       │                             │
    └──────┬──────┘                             │
           │ HTTP/REST                          │
    ┌──────▼──────┐                             │
    │  Backend    │◄────────────────────────────┘
    │  FastAPI    │
    └──────┬──────┘
           │
    ┌──────▼──────┐
    │  PostgreSQL │
    └─────────────┘
```

### 2.1 Princípios da Arquitetura

1. **Docker First**: Tudo roda em containers desde o desenvolvimento
2. **API-First**: Frontend consome API REST
3. **JWT Stateless**: Autenticação sem sessão no servidor
4. **Multiempresa**: Tabelas com tenant_id para isolamento
5. **Auditoria**: Logs de todas as operações
6. **Modular**: Cada módulo é independente

---

## 3. ESTRUTURA DE PASTAS

```
/sistema/
├── backend/
│   ├── app/
│   │   ├── api/            # Rotas FastAPI
│   │   ├── core/           # Config central
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Lógica de negócio
│   │   ├── utils/          # Utilitários
│   │   └── migrations/     # Alembic
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── components/     # Componentes reutilizáveis
│   │   ├── pages/          # Páginas do sistema
│   │   ├── services/       # API calls
│   │   ├── hooks/          # Custom hooks
│   │   ├── contexts/       # Contextos React
│   │   └── lib/            # Bibliotecas auxiliares
│   ├── Dockerfile
│   └── package.json
│
├── database/
│   └── init.sql            # Script completo do banco
│
├── evolution_api/
│   └── docker-compose.yml  # Config Evolution API
│
├── nginx/
│   ├── default.conf        # Config proxy reverso
│   └── Dockerfile
│
├── scripts/
│   ├── install.sh          # Setup VPS
│   ├── deploy.sh           # Deploy automático
│   ├── backup.sh           # Backup automático
│   └── restore.sh          # Restore de backup
│
├── docs/                   # Documentação
├── docker-compose.yml      # Orquestração principal
└── README.md
```

---

## 4. MODELAGEM DO BANCO DE DADOS

### 4.1 Entidades Principais

```
┌────────────────────────────────────────────────────────────────────┐
│                        TABELAS DO SISTEMA                          │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  auth_usuarios        → Usuários do sistema                        │
│  auth_permissoes      → Permissões (CRUD por módulo)               │
│  auth_usuarios_permissoes → Relação usuário x permissão            │
│                                                                     │
│  cad_clientes         → Clientes (pessoa física/jurídica)          │
│  cad_fornecedores     → Fornecedores                               │
│  cad_produtos         → Produtos (com código, estoque, preço)     │
│  cad_categorias       → Categorias dos produtos                    │
│  cad_unidades         → Unidades (kg, m, un, pc, etc)              │
│                                                                     │
│  mov_estoque          → Movimentações de estoque                   │
│  mov_compras          → Compras (pedidos para fornecedores)        │
│  mov_compras_itens    → Itens da compra                            │
│  mov_vendas           → Vendas                                     │
│  mov_vendas_itens     → Itens da venda                             │
│  mov_orcamentos       → Orçamentos                                 │
│  mov_orcamentos_itens → Itens do orçamento                         │
│  mov_entregas         → Controle de entregas                       │
│                                                                     │
│  fin_contas_pagar     → Contas a pagar                             │
│  fin_contas_receber   → Contas a receber                           │
│  fin_caixa            → Fluxo de caixa (movimentações)             │
│  fin_categorias       → Categorias financeiras                     │
│                                                                     │
│  log_auditoria        → Logs de auditoria                          │
│  sys_empresas         → Empresas (multi-tenant)                    │
│  sys_config           → Configurações do sistema                   │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘
```

### 4.2 Relacionamentos Principais

```
empresa 1──N usuario
empresa 1──N cliente
empresa 1──N fornecedor
empresa 1──N produto
empresa 1──N venda
empresa 1──N compra
empresa 1──N financeiro

venda 1──N venda_itens
venda N──1 cliente

compra 1──N compra_itens
compra N──1 fornecedor

produto 1──N venda_itens
produto 1──N compra_itens
produto 1──N estoque
produto N──1 categoria
```

---

## 5. FLUXO DAS TELAS

### 5.1 Mapa de Navegação

```
Login
│
├── Dashboard (visão geral)
│
├── Módulo Cadastros
│   ├── Clientes ─→ Lista ─→ Formulário ─→ Detalhes
│   ├── Fornecedores ─→ Lista ─→ Formulário ─→ Detalhes
│   ├── Produtos ─→ Lista ─→ Formulário ─→ Detalhes
│   └── Categorias ─→ Lista ─→ Formulário
│
├── Módulo Movimentos
│   ├── Vendas ─→ Lista ─→ Nova Venda ─→ Finalizar
│   ├── Compras ─→ Lista ─→ Nova Compra ─→ Receber
│   ├── Orçamentos ─→ Lista ─→ Novo Orçamento ─→ Converter em Venda
│   ├── Estoque ─→ Lista ─→ Ajuste
│   └── Entregas ─→ Lista ─→ Agendar ─→ Concluir
│
├── Módulo Financeiro
│   ├── Contas a Pagar ─→ Lista ─→ Pagar ─→ Baixar
│   ├── Contas a Receber ─→ Lista ─→ Receber ─→ Baixar
│   ├── Fluxo de Caixa ─→ Extrato ─→ Relatório
│   └── Categorias Financeiras
│
├── Módulo Relatórios (PDF)
│   ├── Orçamento PDF
│   ├── Pedido PDF
│   ├── Venda PDF
│   ├── Estoque PDF
│   └── Financeiro PDF
│
├── Módulo WhatsApp
│   ├── Enviar Mensagem
│   ├── Enviar PDF
│   ├── Cobranças
│   └── Notificações
│
├── Módulo Administrativo
│   ├── Usuários ─→ Lista ─→ Formulário ─→ Permissões
│   ├── Minha Empresa
│   ├── Logs de Auditoria
│   └── Configurações
│
└── Logout
```

---

## 6. MÓDULOS FUNCIONAIS DETALHADOS

### Módulo 1: Login
- Tela de login com CPF/email e senha
- JWT Token (access + refresh)
- Recuperação de senha (opcional)
- Proteção contra bruteforce (rate limit)

### Módulo 2: Dashboard
- Cards com indicadores (faturamento hoje, mês, clientes, produtos)
- Gráfico de vendas (últimos 30 dias)
- Contas a pagar/receber próximas
- Estoque baixo (alertas)
- Últimas vendas

### Módulo 3: Clientes
- Cadastro completo (nome, CPF/CNPJ, telefone, email, endereço)
- Lista com busca e filtros
- Histórico de compras
- WhatsApp integrado

### Módulo 4: Produtos
- Código, descrição, unidade, categoria
- Preço de venda, custo, margem
- Controle de estoque (mínimo, máximo, atual)
- Multiplos preços (à vista, prazo)

### Módulo 5: Vendas
- Carrinho de compras
- Desconto por item e total
- Forma de pagamento (dinheiro, cartão, pix, boleto, prazo)
- Geração automática de contas a receber
- PDF da venda

### Módulo 6: Financeiro
- Contas a pagar/receber com vencimento
- Baixa manual ou automática
- Fluxo de caixa (entradas x saídas)
- Saldo diário

### Módulo 7: Relatórios PDF
- Layout profissional com logo
- Cabeçalho com dados da empresa
- Tabelas com itens
- Totais e formas de pagamento
- QR Code PIX (opcional)

### Módulo 8: WhatsApp
- Envio de mensagens via Evolution API
- Notificações de venda confirmada
- Cobranças de contas vencidas
- Avisos de entrega agendada

---

## 7. ROADMAP COMPLETO

### Fase 1 - Planejamento ✅ (ATUAL)
**Duração estimada**: 1 dia
- [x] Documento de arquitetura
- [x] Estrutura de pastas
- [x] Modelagem do banco
- [x] Fluxo das telas
- [x] Tecnologias definidas
- [x] Roadmap

### Fase 2 - Preparação do Ambiente
**Duração estimada**: 1-2 dias
- [ ] Verificar Python 3.12+
- [ ] Verificar Node.js 20+
- [ ] Verificar Docker Desktop
- [ ] Verificar PostgreSQL
- [ ] Verificar Git
- [ ] Verificar VS Code com extensões
- [ ] Criar conta Docker Hub (opcional)

### Fase 3 - Banco de Dados
**Duração estimada**: 2-3 dias
- [ ] Criar script SQL completo
- [ ] Criar tabelas com chaves estrangeiras
- [ ] Criar índices
- [ ] Criar procedures (se necessário)
- [ ] Popular dados de teste
- [ ] Testar conexão via container

### Fase 4 - Backend FastAPI
**Duração estimada**: 7-10 dias
- [ ] Estrutura do projeto com Docker
- [ ] Configuração (CORS, JWT, DB)
- [ ] Modelos SQLAlchemy
- [ ] Schemas Pydantic
- [ ] CRUD de usuários e autenticação
- [ ] CRUD de clientes
- [ ] CRUD de fornecedores
- [ ] CRUD de produtos
- [ ] CRUD de categorias
- [ ] Módulo de vendas
- [ ] Módulo de orçamentos
- [ ] Módulo de compras
- [ ] Módulo de estoque
- [ ] Módulo financeiro
- [ ] Relatórios PDF
- [ ] Integração WhatsApp
- [ ] Logs de auditoria
- [ ] Testes da API

### Fase 5 - Frontend React
**Duração estimada**: 10-14 dias
- [ ] Setup do projeto com Vite + Docker
- [ ] Layout admin (sidebar, header, footer)
- [ ] Tela de login
- [ ] Dashboard com gráficos
- [ ] CRUD Clientes (tabela + formulário)
- [ ] CRUD Fornecedores
- [ ] CRUD Produtos
- [ ] CRUD Categorias
- [ ] Tela de vendas (carrinho)
- [ ] Tela de orçamentos
- [ ] Tela de compras
- [ ] Tela de estoque
- [ ] Tela financeiro (pagar/receber/caixa)
- [ ] Tela de relatórios
- [ ] Tela de WhatsApp
- [ ] Tela de administração
- [ ] Responsividade
- [ ] Testes

### Fase 6 - Docker Completo
**Duração estimada**: 1-2 dias
- [ ] Dockerfile do backend (multistage)
- [ ] Dockerfile do frontend (Nginx)
- [ ] Docker Compose completo
- [ ] Volumes para dados persistentes
- [ ] Rede entre containers
- [ ] Variáveis de ambiente

### Fase 7 - Evolution API (WhatsApp)
**Duração estimada**: 1-2 dias
- [ ] Configurar container Evolution API
- [ ] Configurar webhooks
- [ ] Integrar com backend
- [ ] Testar envio de mensagens
- [ ] Testar envio de PDF

### Fase 8 - Preparação VPS
**Duração estimada**: 1-2 dias
- [ ] Script install.sh automatizado
- [ ] Docker na VPS
- [ ] Nginx + Certbot
- [ ] Firewall (UFW)
- [ ] SSL gratuito

### Fase 9 - Deploy
**Duração estimada**: 1 dia
- [ ] Script deploy.sh
- [ ] Script backup.sh
- [ ] Script restore.sh
- [ ] CI/CD básico
- [ ] Validação em produção

### Fase 10 - Segurança
**Duração estimada**: 1 dia
- [ ] Rate limiting
- [ ] Proteção contra força bruta
- [ ] Headers de segurança
- [ ] Logs de acesso
- [ ] Backup automático

### Fase 11 - Validação Final
**Duração estimada**: 1 dia
- [ ] Testar todas as funcionalidades
- [ ] Checklist de produção
- [ ] Documentação final
- [ ] Treinamento básico

---

## 8. DECISÕES TÉCNICAS IMPORTANTES

### Por que Docker desde o início?
- Ambiente idêntico em desenvolvimento e produção
- Elimina problemas de "funciona na minha máquina"
- Fácil de replicar em qualquer VPS
- Banco de dados isolado
- Rollback simplificado

### Por que PostgreSQL?
- Gratuito e robusto
- Suporte a JSON (útil para dados flexíveis)
- Performance excelente
- Transações ACID
- Amplamente suportado em cloud

### Por que FastAPI e não Django?
- Mais leve e rápido
- Async nativo
- Validação automática com Pydantic
- Documentação Swagger automática
- Melhor para APIs REST

### Por que React + Vite?
- Vite é mais rápido que Create React App
- Ecossistema maduro
- Componentização
- Hooks para estado
- Tailwind CSS para estilos rápidos

---

## 9. PRÓXIMOS PASSOS

Assim que você confirmar que entendeu o planejamento:

1. Vou gerar a **FASE 2** - Verificar seu ambiente Windows
2. Verificar se Python, Node.js, Docker, PostgreSQL estão instalados
3. Ensinar instalação do que faltar
4. Preparar tudo para começar a programar

---

### Documento gerado por: Mentor Técnico Sênior
### Data: 12/06/2026