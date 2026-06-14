import { useState, useEffect } from 'react';
import { api } from '../services/api';
import type { Produto, Cliente, Orcamento } from '../types';

interface ItemOrcamento {
  produto_id: number;
  produto_nome: string;
  quantidade: number;
  preco_unitario: number;
  desconto_item: number;
  subtotal: number;
}

function toNumber(val: any): number {
  if (val === null || val === undefined) return 0;
  const n = Number(val);
  return isNaN(n) ? 0 : n;
}

export default function Orcamentos() {
  const [orcamentos, setOrcamentos] = useState<Orcamento[]>([]);
  const [produtos, setProdutos] = useState<Produto[]>([]);
  const [clientes, setClientes] = useState<Cliente[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [search, setSearch] = useState('');

  // Form state
  const [clienteId, setClienteId] = useState<number>(0);
  const [dataValidade, setDataValidade] = useState('');
  const [desconto, setDesconto] = useState(0);
  const [observacao, setObservacao] = useState('');
  const [carrinho, setCarrinho] = useState<ItemOrcamento[]>([]);
  const [produtoSearch, setProdutoSearch] = useState('');
  const [quantidade, setQuantidade] = useState(1);
  const [saving, setSaving] = useState(false);
  const [success, setSuccess] = useState('');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [orcData, prodData, cliData] = await Promise.all([
        api.getOrcamentos(),
        api.getProdutos(),
        api.getClientes(),
      ]);
      setOrcamentos(Array.isArray(orcData) ? orcData : []);
      setProdutos(Array.isArray(prodData) ? prodData : []);
      setClientes(Array.isArray(cliData) ? cliData : []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async (value: string) => {
    setSearch(value);
    try {
      const result = await api.getOrcamentos(value ? `search=${value}` : '');
      setOrcamentos(Array.isArray(result) ? result : []);
    } catch (err) {
      console.error(err);
    }
  };

  const produtosFiltrados = produtos.filter(p =>
    p.ativo && (p.descricao.toLowerCase().includes(produtoSearch.toLowerCase()) ||
    (p.codigo_barras && p.codigo_barras.toLowerCase().includes(produtoSearch.toLowerCase())))
  );

  const adicionarItem = (produto: Produto) => {
    const pid = toNumber(produto.id);
    if (!pid) return;
    const preco = toNumber(produto.preco_venda);
    if (preco <= 0) return;
    const qtd = quantidade <= 0 ? 1 : quantidade;

    setCarrinho(prev => {
      const existente = prev.find(item => item.produto_id === pid);
      if (existente) {
        return prev.map(item =>
          item.produto_id === pid
            ? { ...item, quantidade: item.quantidade + qtd, subtotal: (item.quantidade + qtd) * item.preco_unitario - item.desconto_item }
            : item
        );
      }
      return [...prev, {
        produto_id: pid,
        produto_nome: produto.descricao,
        quantidade: qtd,
        preco_unitario: preco,
        desconto_item: 0,
        subtotal: qtd * preco,
      }];
    });

    setProdutoSearch('');
    setQuantidade(1);
  };

  const removerItem = (produtoId: number) => {
    setCarrinho(prev => prev.filter(item => item.produto_id !== produtoId));
  };

  const alterarQuantidade = (produtoId: number, qtd: number) => {
    if (qtd <= 0) return removerItem(produtoId);
    setCarrinho(prev => prev.map(item =>
      item.produto_id === produtoId
        ? { ...item, quantidade: qtd, subtotal: qtd * item.preco_unitario - item.desconto_item }
        : item
    ));
  };

  const alterarDescontoItem = (produtoId: number, desc: number) => {
    const d = toNumber(desc);
    setCarrinho(prev => prev.map(item =>
      item.produto_id === produtoId
        ? { ...item, desconto_item: d, subtotal: item.quantidade * item.preco_unitario - d }
        : item
    ));
  };

  const subtotalCarrinho = carrinho.reduce((acc, item) => acc + toNumber(item.subtotal), 0);
  const totalCarrinho = subtotalCarrinho - toNumber(desconto);

  const handleCriarOrcamento = async () => {
    if (!clienteId) { alert('Selecione um cliente'); return; }
    if (carrinho.length === 0) { alert('Adicione produtos ao carrinho'); return; }

    setSaving(true);
    try {
      const result = await api.createOrcamento({
        cliente_id: clienteId,
        data_validade: dataValidade || null,
        desconto: toNumber(desconto),
        observacao,
        itens: carrinho.map(item => ({
          produto_id: item.produto_id,
          quantidade: item.quantidade,
          preco_unitario: item.preco_unitario,
          desconto_item: item.desconto_item,
        })),
      });
      setSuccess(`Orçamento ${result.numero_orcamento} criado com sucesso!`);
      setShowModal(false);
      resetForm();
      loadData();
      setTimeout(() => setSuccess(''), 4000);
    } catch (err: any) {
      alert(err.message);
    } finally {
      setSaving(false);
    }
  };

  const resetForm = () => {
    setClienteId(0);
    setDataValidade('');
    setDesconto(0);
    setObservacao('');
    setCarrinho([]);
  };

  const handleConverter = async (id: number) => {
    if (!confirm('Converter este orçamento em venda? O estoque será baixado.')) return;
    try {
      const result = await api.converterOrcamentoEmVenda(id);
      setSuccess(`Orçamento convertido! Venda ${result.numero_pedido} criada.`);
      loadData();
      setTimeout(() => setSuccess(''), 4000);
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleCancelar = async (id: number) => {
    if (!confirm('Cancelar este orçamento?')) return;
    try {
      await api.cancelarOrcamento(id);
      setSuccess('Orçamento cancelado.');
      loadData();
      setTimeout(() => setSuccess(''), 4000);
    } catch (err: any) {
      alert(err.message);
    }
  };

  const statusBadge = (status: string) => {
    const colors: Record<string, string> = {
      ativo: 'bg-green-100 text-green-700',
      convertido: 'bg-blue-100 text-blue-700',
      vencido: 'bg-yellow-100 text-yellow-700',
      cancelado: 'bg-red-100 text-red-700',
    };
    const labels: Record<string, string> = {
      ativo: 'Ativo',
      convertido: 'Convertido',
      vencido: 'Vencido',
      cancelado: 'Cancelado',
    };
    return (
      <span className={`px-2 py-1 rounded-full text-xs font-medium ${colors[status] || 'bg-gray-100 text-gray-700'}`}>
        {labels[status] || status}
      </span>
    );
  };

  if (loading) {
    return <div className="flex items-center justify-center h-64 text-gray-400">Carregando...</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-800">Orçamentos</h1>
        <button
          onClick={() => setShowModal(true)}
          className="bg-slate-800 hover:bg-slate-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
        >
          + Novo Orçamento
        </button>
      </div>

      {success && (
        <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg">
          {success}
        </div>
      )}

      {/* Search */}
      <div className="relative">
        <input
          type="text"
          value={search}
          onChange={(e) => handleSearch(e.target.value)}
          placeholder="Buscar por cliente..."
          className="w-full border rounded-lg px-4 py-2.5 text-sm pl-10"
        />
        <span className="absolute left-3 top-2.5 text-gray-400">🔍</span>
      </div>

      {/* Lista */}
      <div className="bg-white rounded-xl shadow-sm overflow-hidden">
        <table className="w-full">
          <thead>
            <tr className="bg-gray-50 text-left text-sm text-gray-500">
              <th className="p-4">Nº</th>
              <th className="p-4">Cliente</th>
              <th className="p-4">Data</th>
              <th className="p-4">Validade</th>
              <th className="p-4 text-right">Valor</th>
              <th className="p-4">Status</th>
              <th className="p-4 text-right">Ações</th>
            </tr>
          </thead>
          <tbody>
            {orcamentos.length === 0 ? (
              <tr>
                <td colSpan={7} className="p-8 text-center text-gray-400">
                  Nenhum orçamento encontrado
                </td>
              </tr>
            ) : (
              orcamentos.map((orc) => (
                <tr key={orc.id} className="border-t border-gray-100 hover:bg-gray-50">
                  <td className="p-4 font-medium text-sm">{orc.numero_orcamento}</td>
                  <td className="p-4 text-sm">{orc.cliente_nome || '-'}</td>
                  <td className="p-4 text-sm text-gray-500">
                    {orc.data_orcamento ? new Date(orc.data_orcamento).toLocaleDateString() : '-'}
                  </td>
                  <td className="p-4 text-sm text-gray-500">
                    {orc.data_validade ? new Date(orc.data_validade).toLocaleDateString() : '-'}
                  </td>
                  <td className="p-4 text-sm text-right font-semibold">
                    R$ {toNumber(orc.total).toFixed(2)}
                  </td>
                  <td className="p-4">{statusBadge(orc.status)}</td>
                  <td className="p-4 text-right">
                    <div className="flex justify-end gap-2">
                      <button
                        onClick={() => api.downloadPdfOrcamento(orc.id!)}
                        className="text-slate-600 hover:text-slate-800 text-sm px-2 py-1"
                        title="Baixar PDF"
                      >
                        📄
                      </button>
                      {orc.status === 'ativo' && (
                        <>
                          <button
                            onClick={() => handleConverter(orc.id!)}
                            className="text-blue-600 hover:text-blue-800 text-sm px-2 py-1"
                            title="Converter em Venda"
                          >
                            💳
                          </button>
                          <button
                            onClick={() => handleCancelar(orc.id!)}
                            className="text-red-500 hover:text-red-700 text-sm px-2 py-1"
                            title="Cancelar"
                          >
                            ❌
                          </button>
                        </>
                      )}
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Modal Novo Orçamento */}
      {showModal && (
        <div className="fixed inset-0 bg-black/40 flex items-start justify-center z-50 pt-10 overflow-y-auto">
          <div className="bg-white rounded-xl shadow-xl w-full max-w-5xl mx-4 mb-10">
            <div className="p-6 border-b border-gray-200 flex justify-between items-center">
              <h2 className="text-xl font-bold text-gray-800">Novo Orçamento</h2>
              <button onClick={() => { setShowModal(false); resetForm(); }} className="text-gray-400 hover:text-gray-600 text-xl">✕</button>
            </div>

            <div className="p-6 grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Seleção de Produtos */}
              <div className="lg:col-span-2 space-y-4">
                <div className="bg-white border rounded-lg p-4">
                  <h3 className="text-lg font-semibold text-gray-800 mb-4">Adicionar Produtos</h3>
                  
                  <div className="flex gap-4 mb-4">
                    <div className="flex-1">
                      <label className="block text-sm font-medium text-gray-700 mb-1">Buscar Produto</label>
                      <input
                        type="text"
                        value={produtoSearch}
                        onChange={(e) => setProdutoSearch(e.target.value)}
                        className="w-full border rounded-lg px-3 py-2 text-sm"
                        placeholder="Digite o nome ou código de barras..."
                      />
                    </div>
                    <div className="w-24">
                      <label className="block text-sm font-medium text-gray-700 mb-1">Qtd</label>
                      <input
                        type="number"
                        value={quantidade}
                        onChange={(e) => setQuantidade(Number(e.target.value))}
                        className="w-full border rounded-lg px-3 py-2 text-sm"
                        min={1}
                      />
                    </div>
                  </div>

                  {produtoSearch && (
                    <div className="max-h-60 overflow-y-auto border rounded-lg">
                      {produtosFiltrados.length === 0 ? (
                        <p className="text-gray-400 text-sm p-4">Nenhum produto encontrado</p>
                      ) : (
                        produtosFiltrados.map(prod => (
                          <button
                            key={prod.id}
                            onClick={() => adicionarItem(prod)}
                            className="w-full text-left px-4 py-3 hover:bg-gray-50 border-b last:border-0 flex justify-between"
                          >
                            <div>
                              <p className="text-sm font-medium text-gray-800">{prod.descricao}</p>
                              <p className="text-xs text-gray-500">Estoque: {toNumber(prod.estoque_atual)}</p>
                            </div>
                            <p className="text-sm font-semibold text-slate-700">R$ {toNumber(prod.preco_venda).toFixed(2)}</p>
                          </button>
                        ))
                      )}
                    </div>
                  )}
                </div>

                {/* Carrinho */}
                <div className="bg-white border rounded-lg">
                  <div className="p-4 border-b border-gray-200">
                    <h3 className="text-lg font-semibold text-gray-800">Itens do Orçamento</h3>
                  </div>
                  <div className="p-4">
                    {carrinho.length === 0 ? (
                      <p className="text-gray-400 text-center py-8">Nenhum item adicionado</p>
                    ) : (
                      <table className="w-full">
                        <thead>
                          <tr className="text-left text-sm text-gray-500">
                            <th className="pb-2">Produto</th>
                            <th className="pb-2">Qtd</th>
                            <th className="pb-2">Preço</th>
                            <th className="pb-2">Desc. Item</th>
                            <th className="pb-2 text-right">Subtotal</th>
                            <th className="pb-2"></th>
                          </tr>
                        </thead>
                        <tbody>
                          {carrinho.map((item) => (
                            <tr key={item.produto_id} className="border-t border-gray-100">
                              <td className="py-2 text-sm">{item.produto_nome}</td>
                              <td className="py-2">
                                <input
                                  type="number"
                                  value={item.quantidade}
                                  onChange={(e) => alterarQuantidade(item.produto_id, Number(e.target.value))}
                                  className="w-16 border rounded px-2 py-1 text-sm"
                                  min={1}
                                />
                              </td>
                              <td className="py-2 text-sm">R$ {toNumber(item.preco_unitario).toFixed(2)}</td>
                              <td className="py-2">
                                <input
                                  type="number"
                                  value={item.desconto_item}
                                  onChange={(e) => alterarDescontoItem(item.produto_id, Number(e.target.value))}
                                  className="w-20 border rounded px-2 py-1 text-sm"
                                  min={0}
                                  step={0.01}
                                />
                              </td>
                              <td className="py-2 text-sm text-right">R$ {toNumber(item.subtotal).toFixed(2)}</td>
                              <td className="py-2 text-right">
                                <button onClick={() => removerItem(item.produto_id)} className="text-red-500 text-sm hover:text-red-700">
                                  Remover
                                </button>
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    )}
                  </div>
                </div>
              </div>

              {/* Finalização */}
              <div className="space-y-4">
                <div className="bg-white border rounded-lg p-4">
                  <h3 className="text-lg font-semibold text-gray-800 mb-4">Dados do Orçamento</h3>
                  
                  <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700 mb-1">Cliente *</label>
                    <select
                      value={clienteId}
                      onChange={(e) => setClienteId(Number(e.target.value))}
                      className="w-full border rounded-lg px-3 py-2 text-sm"
                    >
                      <option value={0}>Selecione...</option>
                      {clientes.filter(c => c.ativo).map(cli => (
                        <option key={cli.id} value={cli.id}>{cli.nome}</option>
                      ))}
                    </select>
                  </div>

                  <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700 mb-1">Validade</label>
                    <input
                      type="date"
                      value={dataValidade}
                      onChange={(e) => setDataValidade(e.target.value)}
                      className="w-full border rounded-lg px-3 py-2 text-sm"
                    />
                  </div>

                  <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700 mb-1">Desconto (R$)</label>
                    <input
                      type="number"
                      value={desconto}
                      onChange={(e) => setDesconto(Number(e.target.value))}
                      className="w-full border rounded-lg px-3 py-2 text-sm"
                      min={0}
                      step={0.01}
                    />
                  </div>

                  <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700 mb-1">Observação</label>
                    <textarea
                      value={observacao}
                      onChange={(e) => setObservacao(e.target.value)}
                      className="w-full border rounded-lg px-3 py-2 text-sm"
                      rows={3}
                    />
                  </div>

                  <div className="border-t pt-4 space-y-2">
                    <div className="flex justify-between text-sm text-gray-600">
                      <span>Subtotal:</span>
                      <span>R$ {subtotalCarrinho.toFixed(2)}</span>
                    </div>
                    <div className="flex justify-between text-sm text-gray-600">
                      <span>Desconto:</span>
                      <span>R$ {toNumber(desconto).toFixed(2)}</span>
                    </div>
                    <div className="flex justify-between text-lg font-bold text-slate-800 pt-2 border-t">
                      <span>Total:</span>
                      <span>R$ {totalCarrinho.toFixed(2)}</span>
                    </div>
                  </div>

                  <button
                    onClick={handleCriarOrcamento}
                    disabled={saving || carrinho.length === 0}
                    className="w-full mt-4 bg-slate-800 hover:bg-slate-700 disabled:bg-gray-300 text-white font-semibold py-3 rounded-lg transition-colors"
                  >
                    {saving ? 'Salvando...' : 'Gerar Orçamento'}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}