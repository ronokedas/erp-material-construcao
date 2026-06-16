import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import type { DashboardData, Venda } from '../types';

function toNumber(val: any): number {
  if (val === null || val === undefined) return 0;
  const n = Number(val);
  return isNaN(n) ? 0 : n;
}

export default function Dashboard() {
  const navigate = useNavigate();
  const [data, setData] = useState<DashboardData | null>(null);
  const [ultimasVendas, setUltimasVendas] = useState<Venda[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      const [dashResult, vendasResult] = await Promise.all([
        api.getDashboard(),
        api.getVendas(),
      ]);
      setData(dashResult);
      const vendas = Array.isArray(vendasResult) ? vendasResult : [];
      setUltimasVendas(vendas.slice(0, 5));
    } catch (err) {
      console.error('Erro ao carregar dashboard:', err);
    } finally {
      setLoading(false);
    }
  };

  const cards = [
    { label: 'Clientes', value: data?.total_clientes || 0, icon: '👥', color: 'bg-blue-500', rota: '/clientes' },
    { label: 'Produtos', value: data?.total_produtos || 0, icon: '📦', color: 'bg-green-500', rota: '/produtos' },
    { label: 'Fornecedores', value: data?.total_fornecedores || 0, icon: '🏭', color: 'bg-purple-500', rota: '/fornecedores' },
    { label: 'Vendas Hoje', value: data?.vendas_hoje || 0, icon: '🛒', color: 'bg-orange-500', rota: '/vendas' },
    { label: 'Valor Vendas', value: `R$ ${toNumber(data?.valor_total_vendas || 0).toFixed(2)}`, icon: '💰', color: 'bg-emerald-500', rota: '/vendas' },
    { label: 'Valor Hoje', value: `R$ ${toNumber(data?.valor_vendas_hoje || 0).toFixed(2)}`, icon: '💵', color: 'bg-yellow-500', rota: '/vendas' },
    { label: 'Estoque Baixo', value: data?.produtos_estoque_baixo || 0, icon: '⚠️', color: 'bg-red-500', rota: '/estoque' },
  ];

  const statusBadge = (status: string) => {
    const colors: Record<string, string> = {
      pendente: 'bg-yellow-100 text-yellow-700',
      confirmada: 'bg-green-100 text-green-700',
      cancelada: 'bg-red-100 text-red-700',
      entregue: 'bg-blue-100 text-blue-700',
    };
    return (
      <span className={`px-2 py-1 rounded-full text-xs font-medium ${colors[status] || 'bg-gray-100 text-gray-700'}`}>
        {status}
      </span>
    );
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-2xl text-gray-400">Carregando...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-800">Dashboard</h1>

      {/* Cards Clicáveis */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {cards.map((card) => (
          <button
            key={card.label}
            onClick={() => navigate(card.rota)}
            className="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow text-left w-full cursor-pointer"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500">{card.label}</p>
                <p className="text-2xl font-bold text-gray-800 mt-1">{card.value}</p>
              </div>
              <div className={`${card.color} w-12 h-12 rounded-lg flex items-center justify-center text-2xl`}>
                {card.icon}
              </div>
            </div>
          </button>
        ))}
      </div>

      {/* Últimas Vendas */}
      <div className="bg-white rounded-xl shadow-sm">
        <div className="p-4 border-b border-gray-200 flex justify-between items-center">
          <h3 className="text-lg font-semibold text-gray-800">Últimas Vendas</h3>
          <button
            onClick={() => navigate('/vendas')}
            className="text-sm text-slate-600 hover:text-slate-800 font-medium"
          >
            Ver todas →
          </button>
        </div>
        <div className="p-4">
          {ultimasVendas.length === 0 ? (
            <p className="text-gray-400 text-center py-4">Nenhuma venda registrada</p>
          ) : (
            <table className="w-full">
              <thead>
                <tr className="text-left text-sm text-gray-500">
                  <th className="pb-2">Nº Pedido</th>
                  <th className="pb-2">Data</th>
                  <th className="pb-2 text-right">Valor</th>
                  <th className="pb-2">Status</th>
                </tr>
              </thead>
              <tbody>
                {ultimasVendas.map((venda) => (
                  <tr key={venda.id} className="border-t border-gray-100">
                    <td className="py-2 text-sm font-medium">{venda.numero_pedido}</td>
                    <td className="py-2 text-sm text-gray-500">
                      {venda.data_venda ? new Date(venda.data_venda).toLocaleDateString() : '-'}
                    </td>
                    <td className="py-2 text-sm text-right font-semibold">
                      R$ {toNumber(venda.total).toFixed(2)}
                    </td>
                    <td className="py-2">{statusBadge(venda.status)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>

      {/* Produtos em Destaque (Estoque Baixo) */}
      <div className="bg-white rounded-xl shadow-sm">
        <div className="p-4 border-b border-gray-200 flex justify-between items-center">
          <h3 className="text-lg font-semibold text-gray-800">Produtos em Destaque</h3>
          <button
            onClick={() => navigate('/produtos')}
            className="text-sm text-slate-600 hover:text-slate-800 font-medium"
          >
            Ver todos →
          </button>
        </div>
        <div className="p-4">
          {data && data.produtos_estoque_baixo > 0 ? (
            <div className="flex items-center gap-3 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
              <span className="text-3xl">⚠️</span>
              <div>
                <p className="font-semibold text-yellow-800">
                  {data.produtos_estoque_baixo} produto(s) com estoque baixo
                </p>
                <p className="text-sm text-yellow-600">
                  Clique em "Ver todos" para conferir e fazer novos pedidos
                </p>
              </div>
            </div>
          ) : (
            <p className="text-gray-400 text-center py-4">Nenhum produto com estoque baixo</p>
          )}
        </div>
      </div>
    </div>
  );
}