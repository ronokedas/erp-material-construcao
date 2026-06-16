import { useState, useEffect } from 'react';
import { api } from '../services/api';
import type { Produto } from '../types';
import DataTable from '../components/DataTable';

export default function Estoque() {
  const [produtos, setProdutos] = useState<Produto[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => { load(); }, []);

  const load = async () => {
    try {
      const result = await api.getProdutos();
      setProdutos(Array.isArray(result) ? result : []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const columns = [
    { key: 'descricao', header: 'Produto' },
    { key: 'codigo_barras', header: 'Cód. Barras' },
    {
      key: 'estoque_atual', header: 'Estoque Atual',
      render: (item: Produto) => (
        <span className={`font-semibold ${
          item.estoque_atual <= item.estoque_minimo ? 'text-red-600' : 
          item.estoque_atual <= item.estoque_minimo * 2 ? 'text-yellow-600' : 'text-green-600'
        }`}>
          {item.estoque_atual}
        </span>
      ),
    },
    { key: 'estoque_minimo', header: 'Est. Mínimo' },
    { key: 'categoria_nome', header: 'Categoria' },
    { key: 'fornecedor_nome', header: 'Fornecedor' },
    {
      key: 'preco_custo', header: 'Custo',
      render: (item: Produto) => `R$ ${Number(item.preco_custo).toFixed(2)}`,
    },
    {
      key: 'preco_venda', header: 'Venda',
      render: (item: Produto) => `R$ ${Number(item.preco_venda).toFixed(2)}`,
    },
  ];

  const estoqueBaixo = produtos.filter(p => p.estoque_atual <= p.estoque_minimo);
  const valorTotalEstoque = produtos.reduce((acc, p) => acc + (p.preco_custo * p.estoque_atual), 0);

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-800">Controle de Estoque</h1>

      {/* Cards de resumo */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white rounded-xl shadow-sm p-6">
          <p className="text-sm text-gray-500">Total de Produtos</p>
          <p className="text-2xl font-bold text-gray-800 mt-1">{produtos.length}</p>
        </div>
        <div className="bg-white rounded-xl shadow-sm p-6">
          <p className="text-sm text-gray-500">Estoque Baixo</p>
          <p className="text-2xl font-bold text-red-600 mt-1">{estoqueBaixo.length}</p>
        </div>
        <div className="bg-white rounded-xl shadow-sm p-6">
          <p className="text-sm text-gray-500">Valor Total em Estoque</p>
          <p className="text-2xl font-bold text-gray-800 mt-1">R$ {valorTotalEstoque.toFixed(2)}</p>
        </div>
      </div>

      {/* Alertas de estoque baixo */}
      {estoqueBaixo.length > 0 && (
        <div className="bg-red-50 border border-red-200 rounded-xl p-4">
          <h3 className="font-semibold text-red-700 mb-2">⚠️ Produtos com Estoque Baixo</h3>
          <div className="space-y-1">
              {estoqueBaixo.map(p => (
              <p key={p.id} className="text-sm text-red-600">
                {p.descricao} - Estoque: {p.estoque_atual} (Mínimo: {p.estoque_minimo})
              </p>
            ))}
          </div>
        </div>
      )}

      {/* Tabela */}
      <DataTable title="Todos os Produtos" columns={columns} data={produtos} loading={loading} />
    </div>
  );
}