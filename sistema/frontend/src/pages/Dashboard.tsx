import { useState, useEffect } from 'react';
import { api } from '../services/api';
import type { DashboardData } from '../types';

export default function Dashboard() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      const result = await api.getDashboard();
      setData(result);
    } catch (err) {
      console.error('Erro ao carregar dashboard:', err);
    } finally {
      setLoading(false);
    }
  };

  const cards = [
    { label: 'Clientes', value: data?.total_clientes || 0, icon: '👥', color: 'bg-blue-500' },
    { label: 'Produtos', value: data?.total_produtos || 0, icon: '📦', color: 'bg-green-500' },
    { label: 'Fornecedores', value: data?.total_fornecedores || 0, icon: '🏭', color: 'bg-purple-500' },
    { label: 'Vendas Hoje', value: data?.vendas_hoje || 0, icon: '🛒', color: 'bg-orange-500' },
    { label: 'Valor Vendas', value: `R$ ${(data?.valor_total_vendas || 0).toFixed(2)}`, icon: '💰', color: 'bg-emerald-500' },
    { label: 'Valor Hoje', value: `R$ ${(data?.valor_vendas_hoje || 0).toFixed(2)}`, icon: '💵', color: 'bg-yellow-500' },
    { label: 'Estoque Baixo', value: data?.produtos_estoque_baixo || 0, icon: '⚠️', color: 'bg-red-500' },
  ];

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

      {/* Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {cards.map((card) => (
          <div key={card.label} className="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500">{card.label}</p>
                <p className="text-2xl font-bold text-gray-800 mt-1">{card.value}</p>
              </div>
              <div className={`${card.color} w-12 h-12 rounded-lg flex items-center justify-center text-2xl`}>
                {card.icon}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Placeholder para gráficos futuros */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl shadow-sm p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Últimas Vendas</h3>
          <div className="text-center py-8 text-gray-400">
            Gráfico de vendas será implementado em breve
          </div>
        </div>
        <div className="bg-white rounded-xl shadow-sm p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Produtos em Destaque</h3>
          <div className="text-center py-8 text-gray-400">
            Gráfico de produtos será implementado em breve
          </div>
        </div>
      </div>
    </div>
  );
}