export interface User {
  id: number;
  nome: string;
  email: string;
  tipo: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  usuario: User;
}

export interface Cliente {
  id?: number;
  nome: string;
  cpf_cnpj: string;
  telefone: string;
  email: string;
  endereco: string;
  cidade: string;
  estado: string;
  cep: string;
  ativo: boolean;
  created_at?: string;
}

export interface Fornecedor {
  id?: number;
  nome: string;
  cpf_cnpj: string;
  telefone: string;
  email: string;
  endereco: string;
  cidade: string;
  estado: string;
  cep: string;
  contato_nome: string;
  ativo: boolean;
  created_at?: string;
}

export interface Categoria {
  id?: number;
  nome: string;
  descricao: string;
  ativo: boolean;
}

export interface Produto {
  id?: number;
  codigo: string;
  descricao: string;
  codigo_barras?: string;
  preco_custo: number;
  preco_venda: number;
  estoque_atual: number;
  estoque_minimo: number;
  unidade_id?: number;
  categoria_id?: number;
  categoria_nome?: string;
  fornecedor_id?: number;
  fornecedor_nome?: string;
  ativo: boolean;
  created_at?: string;
}

export interface Venda {
  id?: number;
  cliente_id: number;
  cliente_nome?: string;
  usuario_id?: number;
  numero_pedido?: string;
  data_venda?: string;
  tipo_pagamento?: string;
  total: number;
  status: string;
  observacao?: string;
  subtotal?: number;
  desconto?: number;
  itens: VendaItem[];
}

export interface VendaItem {
  id?: number;
  produto_id: number;
  produto_nome?: string;
  quantidade: number;
  preco_unitario: number;
  subtotal: number;
}

export interface ItemVenda {
  produto_id: number;
  produto_nome: string;
  quantidade: number;
  preco_unitario: number;
  subtotal: number;
}

export interface DashboardData {
  total_clientes: number;
  total_produtos: number;
  total_fornecedores: number;
  total_vendas: number;
  valor_total_vendas: number;
  vendas_hoje: number;
  valor_vendas_hoje: number;
  produtos_estoque_baixo: number;
}