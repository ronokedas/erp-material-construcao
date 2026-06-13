import { useState, useEffect } from 'react';
import { api } from '../services/api';
import type { Produto, Cliente, ItemVenda } from '../types';

export default function Vendas() {
  const [produtos, setProdutos] = useState<Produto[]>([]);
  const [clientes, setClientes] = useState<Cliente[]>([]);
  const [clienteId, setClienteId] = useState<number>(0);
  const [tipoPagamento, setTipoPagamento] = useState('dinheiro');
  const [observacao, setObservacao] = useState('');
  const [carrinho, setCarrinho] = useState<ItemVenda[]>([]);
  const [produtoSearch, setProdutoSearch] = useState('');
  const [quantidade, setQuantidade] = useState(1);
  const [saving, setSaving] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    loadProdutos();
    loadClientes();
  }, []);

  const loadProdutos = async () => {
    try {
      const result = await api.getProdutos();
      setProdutos(Array.isArray(result) ? result : []);
    } catch (err) { console.error(err); }
  };

  const loadClientes = async () => {
    try {
      const result = await api.getClientes();
      setClientes(Array.isArray(result) ? result : []);
    } catch (err) { console.error(err); }
  };

  const produtosFiltrados = produtos.filter(p =>
    p.ativo && (p.descricao.toLowerCase().includes(produtoSearch.toLowerCase()) ||
    (p.codigo_barras && p.codigo_barras.toLowerCase().includes(produtoSearch.toLowerCase())))
  );

  const adicionarItem = (produto: Produto) => {
    const qtd = quantidade <= 0 ? 1 : quantidade;
    const existente = carrinho.find(item => item.produto_id === produto.id);
    
    if (existente) {
      setCarrinho(carrinho.map(item =>
        item.produto_id === produto.id
          ? { ...item, quantidade: item.quantidade + qtd, subtotal: (item.quantidade + qtd) * item.preco_unitario }
          : item
      ));
    } else {
      setCarrinho([...carrinho, {
        produto_id: produto.id!,
        produto_nome: produto.descricao,
        quantidade: qtd,
        preco_unitario: produto.preco_venda,
        subtotal: qtd * produto.preco_venda,
      }]);
    }
    setProdutoSearch('');
    setQuantidade(1);
  };

  const removerItem = (produtoId: number) => {
    setCarrinho(carrinho.filter(item => item.produto_id !== produtoId));
  };

  const alterarQuantidade = (produtoId: number, qtd: number) => {
    if (qtd <= 0) return removerItem(produtoId);
    setCarrinho(carrinho.map(item =>
      item.produto_id === produtoId
        ? { ...item, quantidade: qtd, subtotal: qtd * item.preco_unitario }
        : item
    ));
  };

  const total = carrinho.reduce((acc, item) => acc + item.subtotal, 0);

  const handleFinalizar = async () => {
    if (!clienteId) { setError('Selecione um cliente'); return; }
    if (carrinho.length === 0) { setError('Adicione produtos ao carrinho'); return; }
    
    setSaving(true);
    setError('');
    
    try {
      await api.createVenda({
        cliente_id: clienteId,
        tipo_pagamento: tipoPagamento,
        observacao,
        itens: carrinho.map(item => ({
          produto_id: item.produto_id,
          quantidade: item.quantidade,
          preco_unitario: item.preco_unitario,
        })),
      });
      setSuccess(true);
      setCarrinho([]);
      setClienteId(0);
      setObservacao('');
      setTimeout(() => setSuccess(false), 3000);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-800">Vendas</h1>

      {success && (
        <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg">
          Venda realizada com sucesso!
        </div>
      )}

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg">
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Seleção de Produtos */}
        <div className="lg:col-span-2 space-y-4">
          <div className="bg-white rounded-xl shadow-sm p-4">
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
                        <p className="text-xs text-gray-500">Estoque: {prod.estoque_atual}</p>
                      </div>
                      <p className="text-sm font-semibold text-slate-700">R$ {Number(prod.preco_venda).toFixed(2)}</p>
                    </button>
                  ))
                )}
              </div>
            )}
          </div>

          {/* Carrinho */}
          <div className="bg-white rounded-xl shadow-sm">
            <div className="p-4 border-b border-gray-200">
              <h3 className="text-lg font-semibold text-gray-800">Carrinho</h3>
            </div>
            <div className="p-4">
              {carrinho.length === 0 ? (
                <p className="text-gray-400 text-center py-8">Carrinho vazio</p>
              ) : (
                <table className="w-full">
                  <thead>
                    <tr className="text-left text-sm text-gray-500">
                      <th className="pb-2">Produto</th>
                      <th className="pb-2">Qtd</th>
                      <th className="pb-2">Preço</th>
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
                        <td className="py-2 text-sm">R$ {item.preco_unitario.toFixed(2)}</td>
                        <td className="py-2 text-sm text-right">R$ {item.subtotal.toFixed(2)}</td>
                        <td className="py-2 text-right">
                          <button onClick={() => removerItem(item.produto_id)} className="text-red-500 text-sm hover:text-red-700">
                            Remover
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                  <tfoot>
                    <tr className="border-t border-gray-200">
                      <td colSpan={3} className="py-3 text-right font-semibold text-gray-800">Total:</td>
                      <td className="py-3 text-right font-bold text-lg text-slate-800">R$ {total.toFixed(2)}</td>
                      <td></td>
                    </tr>
                  </tfoot>
                </table>
              )}
            </div>
          </div>
        </div>

        {/* Finalização */}
        <div className="space-y-4">
          <div className="bg-white rounded-xl shadow-sm p-4">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Finalizar Venda</h3>
            
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">Cliente</label>
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
              <label className="block text-sm font-medium text-gray-700 mb-1">Forma de Pagamento</label>
              <select
                value={tipoPagamento}
                onChange={(e) => setTipoPagamento(e.target.value)}
                className="w-full border rounded-lg px-3 py-2 text-sm"
              >
                <option value="dinheiro">Dinheiro</option>
                <option value="credito">Cartão de Crédito</option>
                <option value="debito">Cartão de Débito</option>
                <option value="pix">PIX</option>
                <option value="boleto">Boleto</option>
                <option value="outro">Outro</option>
              </select>
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

            <div className="text-3xl font-bold text-slate-800 mb-4 text-center">
              R$ {total.toFixed(2)}
            </div>

            <button
              onClick={handleFinalizar}
              disabled={saving || carrinho.length === 0}
              className="w-full bg-green-600 hover:bg-green-700 disabled:bg-gray-300 text-white font-semibold py-3 rounded-lg transition-colors"
            >
              {saving ? 'Finalizando...' : 'Finalizar Venda'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}