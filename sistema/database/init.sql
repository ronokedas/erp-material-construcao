-- =====================================================
-- ERP MATERIAL DE CONSTRUÇÃO
-- Script de inicialização do banco de dados PostgreSQL
-- Versão: 1.0
-- =====================================================

-- Criar banco de dados (executar manualmente se necessário)
-- CREATE DATABASE erp_material;

-- =====================================================
-- MÓDULO: SISTEMA / MULTI-EMPRESA
-- =====================================================

-- Tabela de empresas (multi-tenant)
CREATE TABLE IF NOT EXISTS sys_empresas (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(200) NOT NULL,
    nome_fantasia VARCHAR(200),
    cnpj VARCHAR(18) UNIQUE NOT NULL,
    ie VARCHAR(20),
    telefone VARCHAR(20),
    email VARCHAR(200),
    endereco VARCHAR(255),
    numero VARCHAR(20),
    complemento VARCHAR(100),
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    estado VARCHAR(2),
    cep VARCHAR(10),
    logo TEXT,
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Configurações do sistema
CREATE TABLE IF NOT EXISTS sys_config (
    id SERIAL PRIMARY KEY,
    empresa_id INTEGER REFERENCES sys_empresas(id) ON DELETE CASCADE,
    chave VARCHAR(100) NOT NULL,
    valor TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(empresa_id, chave)
);

-- =====================================================
-- MÓDULO: AUTENTICAÇÃO E PERMISSÕES
-- =====================================================

-- Usuários do sistema
CREATE TABLE IF NOT EXISTS auth_usuarios (
    id SERIAL PRIMARY KEY,
    empresa_id INTEGER REFERENCES sys_empresas(id) ON DELETE CASCADE,
    nome VARCHAR(200) NOT NULL,
    email VARCHAR(200) UNIQUE NOT NULL,
    cpf VARCHAR(14) UNIQUE,
    telefone VARCHAR(20),
    senha_hash VARCHAR(255) NOT NULL,
    ativo BOOLEAN DEFAULT TRUE,
    admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Permissões disponíveis
CREATE TABLE IF NOT EXISTS auth_permissoes (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    modulo VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Relação usuário x permissão
CREATE TABLE IF NOT EXISTS auth_usuarios_permissoes (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL REFERENCES auth_usuarios(id) ON DELETE CASCADE,
    permissao_id INTEGER NOT NULL REFERENCES auth_permissoes(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(usuario_id, permissao_id)
);

-- =====================================================
-- MÓDULO: CADASTROS BÁSICOS
-- =====================================================

-- Categorias de produtos
CREATE TABLE IF NOT EXISTS cad_categorias (
    id SERIAL PRIMARY KEY,
    empresa_id INTEGER REFERENCES sys_empresas(id) ON DELETE CASCADE,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Unidades de medida
CREATE TABLE IF NOT EXISTS cad_unidades (
    id SERIAL PRIMARY KEY,
    sigla VARCHAR(10) UNIQUE NOT NULL,
    nome VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Produtos
CREATE TABLE IF NOT EXISTS cad_produtos (
    id SERIAL PRIMARY KEY,
    empresa_id INTEGER REFERENCES sys_empresas(id) ON DELETE CASCADE,
    codigo VARCHAR(50) NOT NULL,
    codigo_barras VARCHAR(50),
    descricao VARCHAR(255) NOT NULL,
    categoria_id INTEGER REFERENCES cad_categorias(id) ON DELETE SET NULL,
    unidade_id INTEGER REFERENCES cad_unidades(id) ON DELETE SET NULL,
    preco_custo DECIMAL(12,2) DEFAULT 0,
    preco_venda DECIMAL(12,2) DEFAULT 0,
    preco_prazo DECIMAL(12,2) DEFAULT 0,
    estoque_minimo DECIMAL(12,3) DEFAULT 0,
    estoque_atual DECIMAL(12,3) DEFAULT 0,
    ncm VARCHAR(10),
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(empresa_id, codigo)
);

-- Clientes
CREATE TABLE IF NOT EXISTS cad_clientes (
    id SERIAL PRIMARY KEY,
    empresa_id INTEGER REFERENCES sys_empresas(id) ON DELETE CASCADE,
    nome VARCHAR(200) NOT NULL,
    tipo_pessoa CHAR(1) DEFAULT 'F', -- F=Física, J=Jurídica
    cpf_cnpj VARCHAR(18) UNIQUE,
    rg_ie VARCHAR(20),
    telefone VARCHAR(20),
    telefone2 VARCHAR(20),
    email VARCHAR(200),
    endereco VARCHAR(255),
    numero VARCHAR(20),
    complemento VARCHAR(100),
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    estado VARCHAR(2),
    cep VARCHAR(10),
    whatsapp VARCHAR(20),
    limite_credito DECIMAL(12,2) DEFAULT 0,
    observacao TEXT,
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Fornecedores
CREATE TABLE IF NOT EXISTS cad_fornecedores (
    id SERIAL PRIMARY KEY,
    empresa_id INTEGER REFERENCES sys_empresas(id) ON DELETE CASCADE,
    nome VARCHAR(200) NOT NULL,
    tipo_pessoa CHAR(1) DEFAULT 'J',
    cpf_cnpj VARCHAR(18) UNIQUE,
    ie VARCHAR(20),
    telefone VARCHAR(20),
    email VARCHAR(200),
    endereco VARCHAR(255),
    numero VARCHAR(20),
    complemento VARCHAR(100),
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    estado VARCHAR(2),
    cep VARCHAR(10),
    contato_nome VARCHAR(100),
    contato_telefone VARCHAR(20),
    observacao TEXT,
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- MÓDULO: MOVIMENTOS (VENDAS, COMPRAS, ORÇAMENTOS)
-- =====================================================

-- Vendas
CREATE TABLE IF NOT EXISTS mov_vendas (
    id SERIAL PRIMARY KEY,
    empresa_id INTEGER REFERENCES sys_empresas(id) ON DELETE CASCADE,
    cliente_id INTEGER REFERENCES cad_clientes(id) ON DELETE SET NULL,
    usuario_id INTEGER REFERENCES auth_usuarios(id) ON DELETE SET NULL,
    numero_pedido VARCHAR(20) UNIQUE NOT NULL,
    data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tipo_pagamento VARCHAR(30), -- dinheiro, cartao_credito, cartao_debito, pix, boleto, prazo
    status VARCHAR(20) DEFAULT 'pendente', -- pendente, confirmada, cancelada, entregue
    subtotal DECIMAL(12,2) DEFAULT 0,
    desconto DECIMAL(12,2) DEFAULT 0,
    total DECIMAL(12,2) DEFAULT 0,
    observacao TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Itens da venda
CREATE TABLE IF NOT EXISTS mov_vendas_itens (
    id SERIAL PRIMARY KEY,
    venda_id INTEGER NOT NULL REFERENCES mov_vendas(id) ON DELETE CASCADE,
    produto_id INTEGER REFERENCES cad_produtos(id) ON DELETE SET NULL,
    quantidade DECIMAL(12,3) NOT NULL,
    preco_unitario DECIMAL(12,2) NOT NULL,
    desconto_item DECIMAL(12,2) DEFAULT 0,
    subtotal_item DECIMAL(12,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Compras
CREATE TABLE IF NOT EXISTS mov_compras (
    id SERIAL PRIMARY KEY,
    empresa_id INTEGER REFERENCES sys_empresas(id) ON DELETE CASCADE,
    fornecedor_id INTEGER REFERENCES cad_fornecedores(id) ON DELETE SET NULL,
    usuario_id INTEGER REFERENCES auth_usuarios(id) ON DELETE SET NULL,
    numero_pedido VARCHAR(20) UNIQUE NOT NULL,
    data_compra TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pendente', -- pendente, recebida, cancelada
    subtotal DECIMAL(12,2) DEFAULT 0,
    desconto DECIMAL(12,2) DEFAULT 0,
    total DECIMAL(12,2) DEFAULT 0,
    observacao TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Itens da compra
CREATE TABLE IF NOT EXISTS mov_compras_itens (
    id SERIAL PRIMARY KEY,
    compra_id INTEGER NOT NULL REFERENCES mov_compras(id) ON DELETE CASCADE,
    produto_id INTEGER REFERENCES cad_produtos(id) ON DELETE SET NULL,
    quantidade DECIMAL(12,3) NOT NULL,
    preco_unitario DECIMAL(12,2) NOT NULL,
    desconto_item DECIMAL(12,2) DEFAULT 0,
    subtotal_item DECIMAL(12,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orçamentos
CREATE TABLE IF NOT EXISTS mov_orcamentos (
    id SERIAL PRIMARY KEY,
    empresa_id INTEGER REFERENCES sys_empresas(id) ON DELETE CASCADE,
    cliente_id INTEGER REFERENCES cad_clientes(id) ON DELETE SET NULL,
    usuario_id INTEGER REFERENCES auth_usuarios(id) ON DELETE SET NULL,
    numero_orcamento VARCHAR(20) UNIQUE NOT NULL,
    data_orcamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_validade DATE,
    status VARCHAR(20) DEFAULT 'ativo', -- ativo, convertido, vencido, cancelado
    subtotal DECIMAL(12,2) DEFAULT 0,
    desconto DECIMAL(12,2) DEFAULT 0,
    total DECIMAL(12,2) DEFAULT 0,
    observacao TEXT,
    venda_id INTEGER REFERENCES mov_vendas(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Itens do orçamento
CREATE TABLE IF NOT EXISTS mov_orcamentos_itens (
    id SERIAL PRIMARY KEY,
    orcamento_id INTEGER NOT NULL REFERENCES mov_orcamentos(id) ON DELETE CASCADE,
    produto_id INTEGER REFERENCES cad_produtos(id) ON DELETE SET NULL,
    quantidade DECIMAL(12,3) NOT NULL,
    preco_unitario DECIMAL(12,2) NOT NULL,
    desconto_item DECIMAL(12,2) DEFAULT 0,
    subtotal_item DECIMAL(12,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- MÓDULO: ESTOQUE
-- =====================================================

-- Movimentações de estoque
CREATE TABLE IF NOT EXISTS mov_estoque (
    id SERIAL PRIMARY KEY,
    empresa_id INTEGER REFERENCES sys_empresas(id) ON DELETE CASCADE,
    produto_id INTEGER NOT NULL REFERENCES cad_produtos(id) ON DELETE CASCADE,
    tipo VARCHAR(10) NOT NULL, -- 'entrada', 'saida', 'ajuste'
    quantidade DECIMAL(12,3) NOT NULL,
    saldo_anterior DECIMAL(12,3) DEFAULT 0,
    saldo_atual DECIMAL(12,3) DEFAULT 0,
    documento_tipo VARCHAR(30), -- venda, compra, ajuste
    documento_id INTEGER,
    observacao TEXT,
    usuario_id INTEGER REFERENCES auth_usuarios(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- MÓDULO: ENTREGAS
-- =====================================================

-- Controle de entregas
CREATE TABLE IF NOT EXISTS mov_entregas (
    id SERIAL PRIMARY KEY,
    empresa_id INTEGER REFERENCES sys_empresas(id) ON DELETE CASCADE,
    venda_id INTEGER REFERENCES mov_vendas(id) ON DELETE SET NULL,
    cliente_id INTEGER REFERENCES cad_clientes(id) ON DELETE SET NULL,
    endereco_entrega VARCHAR(255),
    data_agendada DATE,
    data_entrega TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pendente', -- pendente, agendada, entregue, cancelada
    observacao TEXT,
    usuario_id INTEGER REFERENCES auth_usuarios(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- MÓDULO: FINANCEIRO
-- =====================================================

-- Categorias financeiras
CREATE TABLE IF NOT EXISTS fin_categorias (
    id SERIAL PRIMARY KEY,
    empresa_id INTEGER REFERENCES sys_empresas(id) ON DELETE CASCADE,
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(10) NOT NULL, -- 'receita', 'despesa'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Contas a pagar
CREATE TABLE IF NOT EXISTS fin_contas_pagar (
    id SERIAL PRIMARY KEY,
    empresa_id INTEGER REFERENCES sys_empresas(id) ON DELETE CASCADE,
    fornecedor_id INTEGER REFERENCES cad_fornecedores(id) ON DELETE SET NULL,
    categoria_id INTEGER REFERENCES fin_categorias(id) ON DELETE SET NULL,
    descricao VARCHAR(255) NOT NULL,
    valor DECIMAL(12,2) NOT NULL,
    data_vencimento DATE NOT NULL,
    data_pagamento TIMESTAMP,
    valor_pago DECIMAL(12,2),
    status VARCHAR(20) DEFAULT 'pendente', -- pendente, paga, atrasada, cancelada
    documento_tipo VARCHAR(30),
    documento_id INTEGER,
    observacao TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Contas a receber
CREATE TABLE IF NOT EXISTS fin_contas_receber (
    id SERIAL PRIMARY KEY,
    empresa_id INTEGER REFERENCES sys_empresas(id) ON DELETE CASCADE,
    cliente_id INTEGER REFERENCES cad_clientes(id) ON DELETE SET NULL,
    categoria_id INTEGER REFERENCES fin_categorias(id) ON DELETE SET NULL,
    descricao VARCHAR(255) NOT NULL,
    valor DECIMAL(12,2) NOT NULL,
    data_vencimento DATE NOT NULL,
    data_recebimento TIMESTAMP,
    valor_recebido DECIMAL(12,2),
    status VARCHAR(20) DEFAULT 'pendente', -- pendente, recebida, atrasada, cancelada
    documento_tipo VARCHAR(30),
    documento_id INTEGER,
    observacao TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Fluxo de caixa
CREATE TABLE IF NOT EXISTS fin_caixa (
    id SERIAL PRIMARY KEY,
    empresa_id INTEGER REFERENCES sys_empresas(id) ON DELETE CASCADE,
    tipo VARCHAR(10) NOT NULL, -- 'entrada', 'saida'
    descricao VARCHAR(255) NOT NULL,
    valor DECIMAL(12,2) NOT NULL,
    data_movimento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    conta_pagar_id INTEGER REFERENCES fin_contas_pagar(id) ON DELETE SET NULL,
    conta_receber_id INTEGER REFERENCES fin_contas_receber(id) ON DELETE SET NULL,
    forma_pagamento VARCHAR(30),
    observacao TEXT,
    usuario_id INTEGER REFERENCES auth_usuarios(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- MÓDULO: AUDITORIA
-- =====================================================

-- Logs de auditoria
CREATE TABLE IF NOT EXISTS log_auditoria (
    id SERIAL PRIMARY KEY,
    empresa_id INTEGER REFERENCES sys_empresas(id) ON DELETE CASCADE,
    usuario_id INTEGER REFERENCES auth_usuarios(id) ON DELETE SET NULL,
    acao VARCHAR(50) NOT NULL, -- create, update, delete, login, logout
    entidade VARCHAR(50) NOT NULL,
    entidade_id INTEGER,
    valores_antigos JSONB,
    valores_novos JSONB,
    ip VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- ÍNDICES
-- =====================================================

-- Índices para performance
CREATE INDEX IF NOT EXISTS idx_usuarios_empresa ON auth_usuarios(empresa_id);
CREATE INDEX IF NOT EXISTS idx_usuarios_email ON auth_usuarios(email);
CREATE INDEX IF NOT EXISTS idx_usuarios_permissoes_usuario ON auth_usuarios_permissoes(usuario_id);
CREATE INDEX IF NOT EXISTS idx_produtos_empresa ON cad_produtos(empresa_id);
CREATE INDEX IF NOT EXISTS idx_produtos_categoria ON cad_produtos(categoria_id);
CREATE INDEX IF NOT EXISTS idx_produtos_descricao ON cad_produtos(descricao);
CREATE INDEX IF NOT EXISTS idx_clientes_empresa ON cad_clientes(empresa_id);
CREATE INDEX IF NOT EXISTS idx_clientes_cpf_cnpj ON cad_clientes(cpf_cnpj);
CREATE INDEX IF NOT EXISTS idx_clientes_telefone ON cad_clientes(telefone);
CREATE INDEX IF NOT EXISTS idx_fornecedores_empresa ON cad_fornecedores(empresa_id);
CREATE INDEX IF NOT EXISTS idx_vendas_empresa ON mov_vendas(empresa_id);
CREATE INDEX IF NOT EXISTS idx_vendas_cliente ON mov_vendas(cliente_id);
CREATE INDEX IF NOT EXISTS idx_vendas_data ON mov_vendas(data_venda);
CREATE INDEX IF NOT EXISTS idx_vendas_status ON mov_vendas(status);
CREATE INDEX IF NOT EXISTS idx_vendas_itens_venda ON mov_vendas_itens(venda_id);
CREATE INDEX IF NOT EXISTS idx_compras_empresa ON mov_compras(empresa_id);
CREATE INDEX IF NOT EXISTS idx_compras_fornecedor ON mov_compras(fornecedor_id);
CREATE INDEX IF NOT EXISTS idx_orcamentos_empresa ON mov_orcamentos(empresa_id);
CREATE INDEX IF NOT EXISTS idx_orcamentos_cliente ON mov_orcamentos(cliente_id);
CREATE INDEX IF NOT EXISTS idx_estoque_produto ON mov_estoque(produto_id);
CREATE INDEX IF NOT EXISTS idx_estoque_data ON mov_estoque(created_at);
CREATE INDEX IF NOT EXISTS idx_entregas_venda ON mov_entregas(venda_id);
CREATE INDEX IF NOT EXISTS idx_entregas_status ON mov_entregas(status);
CREATE INDEX IF NOT EXISTS idx_contas_pagar_empresa ON fin_contas_pagar(empresa_id);
CREATE INDEX IF NOT EXISTS idx_contas_pagar_vencimento ON fin_contas_pagar(data_vencimento);
CREATE INDEX IF NOT EXISTS idx_contas_pagar_status ON fin_contas_pagar(status);
CREATE INDEX IF NOT EXISTS idx_contas_receber_empresa ON fin_contas_receber(empresa_id);
CREATE INDEX IF NOT EXISTS idx_contas_receber_vencimento ON fin_contas_receber(data_vencimento);
CREATE INDEX IF NOT EXISTS idx_contas_receber_status ON fin_contas_receber(status);
CREATE INDEX IF NOT EXISTS idx_caixa_data ON fin_caixa(data_movimento);
CREATE INDEX IF NOT EXISTS idx_auditoria_entidade ON log_auditoria(entidade, entidade_id);
CREATE INDEX IF NOT EXISTS idx_auditoria_data ON log_auditoria(created_at);
CREATE INDEX IF NOT EXISTS idx_auditoria_usuario ON log_auditoria(usuario_id);

-- =====================================================
-- DADOS INICIAIS (SEED)
-- =====================================================

-- Inserir empresa padrão
INSERT INTO sys_empresas (nome, nome_fantasia, cnpj, telefone, email, cidade, estado)
VALUES ('Empresa Padrão Ltda', 'Minha Loja', '00.000.000/0001-00', '(11) 99999-9999', 'contato@minhaloja.com.br', 'São Paulo', 'SP');

-- Inserir unidades de medida
INSERT INTO cad_unidades (sigla, nome) VALUES
('UN', 'Unidade'),
('KG', 'Quilograma'),
('G', 'Grama'),
('M', 'Metro'),
('CM', 'Centímetro'),
('M2', 'Metro Quadrado'),
('M3', 'Metro Cúbico'),
('L', 'Litro'),
('ML', 'Mililitro'),
('PC', 'Peça'),
('CX', 'Caixa'),
('PT', 'Pote'),
('SC', 'Saco'),
('GL', 'Galão'),
('TB', 'Tambor');

-- Inserir permissões padrão
INSERT INTO auth_permissoes (codigo, nome, descricao, modulo) VALUES
('dashboard_view', 'Visualizar Dashboard', 'Acesso ao dashboard', 'Dashboard'),
('clientes_create', 'Criar Clientes', 'Criar novos clientes', 'Clientes'),
('clientes_read', 'Listar Clientes', 'Visualizar lista de clientes', 'Clientes'),
('clientes_update', 'Editar Clientes', 'Editar dados dos clientes', 'Clientes'),
('clientes_delete', 'Excluir Clientes', 'Excluir clientes', 'Clientes'),
('fornecedores_create', 'Criar Fornecedores', 'Criar novos fornecedores', 'Fornecedores'),
('fornecedores_read', 'Listar Fornecedores', 'Visualizar fornecedores', 'Fornecedores'),
('fornecedores_update', 'Editar Fornecedores', 'Editar fornecedores', 'Fornecedores'),
('fornecedores_delete', 'Excluir Fornecedores', 'Excluir fornecedores', 'Fornecedores'),
('produtos_create', 'Criar Produtos', 'Criar novos produtos', 'Produtos'),
('produtos_read', 'Listar Produtos', 'Visualizar produtos', 'Produtos'),
('produtos_update', 'Editar Produtos', 'Editar produtos', 'Produtos'),
('produtos_delete', 'Excluir Produtos', 'Excluir produtos', 'Produtos'),
('vendas_create', 'Criar Vendas', 'Realizar vendas', 'Vendas'),
('vendas_read', 'Listar Vendas', 'Visualizar vendas', 'Vendas'),
('vendas_update', 'Editar Vendas', 'Editar vendas', 'Vendas'),
('vendas_delete', 'Excluir Vendas', 'Excluir vendas', 'Vendas'),
('compras_create', 'Criar Compras', 'Criar compras', 'Compras'),
('compras_read', 'Listar Compras', 'Visualizar compras', 'Compras'),
('orcamentos_create', 'Criar Orçamentos', 'Criar orçamentos', 'Orçamentos'),
('orcamentos_read', 'Listar Orçamentos', 'Visualizar orçamentos', 'Orçamentos'),
('orcamentos_convert', 'Converter Orçamento', 'Converter orçamento em venda', 'Orçamentos'),
('financeiro_read', 'Visualizar Financeiro', 'Acessar módulo financeiro', 'Financeiro'),
('financeiro_pagar', 'Pagar Contas', 'Baixar contas a pagar', 'Financeiro'),
('financeiro_receber', 'Receber Contas', 'Baixar contas a receber', 'Financeiro'),
('relatorios_read', 'Gerar Relatórios', 'Gerar relatórios PDF', 'Relatórios'),
('whatsapp_send', 'Enviar WhatsApp', 'Enviar mensagens WhatsApp', 'WhatsApp'),
('usuarios_create', 'Gerenciar Usuários', 'Criar/editar usuários', 'Admin'),
('usuarios_read', 'Listar Usuários', 'Visualizar usuários', 'Admin'),
('config_view', 'Configurações', 'Acessar configurações', 'Admin'),
('auditoria_view', 'Ver Logs', 'Visualizar logs de auditoria', 'Admin');

-- Inserir usuário admin padrão (senha: admin123)
-- O hash abaixo é bcrypt de 'admin123'
INSERT INTO auth_usuarios (empresa_id, nome, email, cpf, telefone, senha_hash, admin, ativo)
VALUES (
    1,
    'Administrador',
    'admin@erp.com.br',
    '000.000.000-00',
    '(11) 99999-9999',
    '$2b$12$xUeJERfB02N8tam5lDeXuepLS.4k9WqWRHQ88XiUKYUcvZ6jzmMoy',
    TRUE,
    TRUE
);

-- Inserir categorias de exemplo
INSERT INTO cad_categorias (empresa_id, nome, descricao) VALUES
(1, 'Cimento e Argamassas', 'Cimento, argamassa, rejunte e adesivos'),
(1, 'Tijolos e Blocos', 'Tijolos cerâmicos, blocos de concreto'),
(1, 'Areia e Pedra', 'Areia fina, grossa, pedra britada'),
(1, 'Ferragens', 'Ferro, aço, telas, vergalhões'),
(1, 'Tintas', 'Tintas, vernizes, solventes'),
(1, 'Hidráulica', 'Tubos, conexões, registros'),
(1, 'Elétrica', 'Fios, cabos, interruptores'),
(1, 'Madeiras', 'Madeiras, compensados, ripas'),
(1, 'Telhados', 'Telhas, calhas, rufos'),
(1, 'Acabamentos', 'Pisos, revestimentos, porcelanatos');

-- Inserir produtos de exemplo
INSERT INTO cad_produtos (empresa_id, codigo, descricao, categoria_id, unidade_id, preco_custo, preco_venda, estoque_minimo, estoque_atual) VALUES
(1, 'CIM001', 'Cimento CP-II 50kg', 1, 4, 25.00, 42.90, 10, 50),
(1, 'CIM002', 'Argamassa AC-III 20kg', 1, 4, 12.00, 22.90, 10, 30),
(1, 'TEL001', 'Telha Colonial 50x20cm', 9, 10, 2.50, 6.90, 50, 200),
(1, 'TEL002', 'Telha Fibrocimento 6mm 2.44m', 9, 10, 35.00, 59.90, 5, 20),
(1, 'TIN001', 'Tinta Acrílica Branco 18L', 5, 13, 80.00, 149.90, 3, 15),
(1, 'TIN002', 'Verniz Poliuretano 1L', 5, 8, 25.00, 49.90, 5, 10),
(1, 'TUB001', 'Tubo PVC 50mm 3m', 6, 10, 8.00, 16.90, 10, 40),
(1, 'TUB002', 'Conexão PVC 50mm', 6, 10, 1.50, 4.90, 20, 100),
(1, 'FIO001', 'Cabo 2.5mm 100m', 7, 10, 45.00, 89.90, 3, 10),
(1, 'FIO002', 'Interruptor Simples', 7, 10, 3.00, 8.90, 10, 30),
(1, 'ARE001', 'Areia Fina 1m³', 3, 7, 60.00, 99.90, 2, 5),
(1, 'PED001', 'Pedra Britada 1m³', 3, 7, 70.00, 119.90, 2, 5);

-- Inserir clientes de exemplo
INSERT INTO cad_clientes (empresa_id, nome, tipo_pessoa, cpf_cnpj, telefone, email, cidade, estado) VALUES
(1, 'João Silva', 'F', '111.111.111-11', '(11) 98888-8888', 'joao@email.com', 'São Paulo', 'SP'),
(1, 'Maria Santos', 'F', '222.222.222-22', '(11) 97777-7777', 'maria@email.com', 'São Paulo', 'SP'),
(1, 'Construtora ABC Ltda', 'J', '33.333.333/0001-33', '(11) 96666-6666', 'construtora@email.com', 'São Paulo', 'SP'),
(1, 'Pedro Oliveira', 'F', '444.444.444-44', '(11) 95555-5555', 'pedro@email.com', 'Guarulhos', 'SP');

-- Inserir fornecedores de exemplo
INSERT INTO cad_fornecedores (empresa_id, nome, tipo_pessoa, cpf_cnpj, telefone, email, cidade, estado) VALUES
(1, 'Cimenteira Nacional S.A.', 'J', '10.000.000/0001-10', '(11) 3333-3333', 'vendas@cimenteira.com.br', 'São Paulo', 'SP'),
(1, 'Telhas Brasil Indústria', 'J', '20.000.000/0001-20', '(11) 4444-4444', 'vendas@telhasbrasil.com.br', 'São Bernardo', 'SP'),
(1, 'Tintas Color Ltda', 'J', '30.000.000/0001-30', '(11) 5555-5555', 'vendas@tintascolor.com.br', 'São Paulo', 'SP'),
(1, 'Hidrotubos Comércio', 'J', '40.000.000/0001-40', '(11) 6666-6666', 'vendas@hidrotubos.com.br', 'Osasco', 'SP');

-- Inserir categorias financeiras
INSERT INTO fin_categorias (empresa_id, nome, tipo) VALUES
(1, 'Vendas', 'receita'),
(1, 'Serviços', 'receita'),
(1, 'Receitas Diversas', 'receita'),
(1, 'Compras de Mercadorias', 'despesa'),
(1, 'Salários', 'despesa'),
(1, 'Água/Luz/Telefone', 'despesa'),
(1, 'Aluguel', 'despesa'),
(1, 'Impostos', 'despesa'),
(1, 'Despesas Diversas', 'despesa');

-- Mensagem de conclusão
DO $$
BEGIN
    RAISE NOTICE '✅ Banco de dados ERP Material de Construção inicializado com sucesso!';
    RAISE NOTICE '📊 Tabelas criadas: 23';
    RAISE NOTICE '👤 Usuário admin: admin@erp.com.br / admin123';
    RAISE NOTICE '🏢 Empresa padrão: Minha Loja (CNPJ: 00.000.000/0001-00)';
END $$;