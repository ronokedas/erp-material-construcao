const API_URL = import.meta.env.VITE_API_URL || '';

class ApiService {
  private token: string | null = null;

  constructor() {
    this.token = localStorage.getItem('access_token');
  }

  setToken(token: string | null) {
    this.token = token;
    if (token) {
      localStorage.setItem('access_token', token);
    } else {
      localStorage.removeItem('access_token');
    }
  }

  getToken(): string | null {
    return this.token;
  }

  private async request(endpoint: string, options: RequestInit = {}) {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...(options.headers as Record<string, string>),
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    const response = await fetch(`${API_URL}${endpoint}`, {
      ...options,
      headers,
    });

    if (response.status === 401) {
      this.setToken(null);
      window.location.href = '/login';
      throw new Error('Não autorizado');
    }

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Erro na requisição' }));
      throw new Error(error.detail || 'Erro na requisição');
    }

    // Respostas 204 Não Conteúdo (DELETE) não têm corpo JSON
    if (response.status === 204 || response.headers.get('content-length') === '0') {
      return null;
    }

    return response.json();
  }

  // Auth
  async login(email: string, senha: string) {
    const response = await fetch(`${API_URL}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, senha }),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Erro ao fazer login' }));
      throw new Error(error.detail || 'Erro ao fazer login');
    }

    const data = await response.json();
    this.setToken(data.access_token);
    return data;
  }

  // Clientes
  async getClientes(params?: string) {
    return this.request(`/api/clientes${params ? `?${params}` : ''}`);
  }

  async getCliente(id: number) {
    return this.request(`/api/clientes/${id}`);
  }

  async createCliente(data: any) {
    return this.request('/api/clientes', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async updateCliente(id: number, data: any) {
    return this.request(`/api/clientes/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async deleteCliente(id: number) {
    return this.request(`/api/clientes/${id}`, {
      method: 'DELETE',
    });
  }

  // Fornecedores
  async getFornecedores(params?: string) {
    return this.request(`/api/fornecedores${params ? `?${params}` : ''}`);
  }

  async getFornecedor(id: number) {
    return this.request(`/api/fornecedores/${id}`);
  }

  async createFornecedor(data: any) {
    return this.request('/api/fornecedores', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async updateFornecedor(id: number, data: any) {
    return this.request(`/api/fornecedores/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async deleteFornecedor(id: number) {
    return this.request(`/api/fornecedores/${id}`, {
      method: 'DELETE',
    });
  }

  // Categorias
  async getCategorias(params?: string) {
    return this.request(`/api/categorias${params ? `?${params}` : ''}`);
  }

  async getCategoria(id: number) {
    return this.request(`/api/categorias/${id}`);
  }

  async createCategoria(data: any) {
    return this.request('/api/categorias', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async updateCategoria(id: number, data: any) {
    return this.request(`/api/categorias/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async deleteCategoria(id: number) {
    return this.request(`/api/categorias/${id}`, {
      method: 'DELETE',
    });
  }

  // Produtos
  async getProdutos(params?: string) {
    return this.request(`/api/produtos${params ? `?${params}` : ''}`);
  }

  async getProduto(id: number) {
    return this.request(`/api/produtos/${id}`);
  }

  async createProduto(data: any) {
    return this.request('/api/produtos', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async updateProduto(id: number, data: any) {
    return this.request(`/api/produtos/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async deleteProduto(id: number) {
    return this.request(`/api/produtos/${id}`, {
      method: 'DELETE',
    });
  }

  // Vendas
  async getVendas(params?: string) {
    return this.request(`/api/vendas${params ? `?${params}` : ''}`);
  }

  async getVenda(id: number) {
    return this.request(`/api/vendas/${id}`);
  }

  async createVenda(data: any) {
    return this.request('/api/vendas', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Dashboard
  async getDashboard() {
    return this.request('/api/dashboard');
  }
}

export const api = new ApiService();