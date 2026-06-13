import { useState, useEffect } from 'react';
import { api } from '../services/api';
import DataTable from '../components/DataTable';

interface VendaFinanceiro {
  id: number;
  cliente_id: number;
  numero_pedido: string;
  data_venda: string;
  total: number;
  tipo_pagamento: string;
  status: string;
  observacao: string;
}

export default function Financeiro() {
  const [vendas, setVendas] = useState<VendaFinanceiro[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => { load(); }, []);

  const load = async () => {
    try {
      const result = await api.getVendas();
      setVendas(Array.isArray(result) ? result : []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const totalRecebido = vendas
    .filter(v => v.status === 'concluida')
    .reduce((acc, v) => acc + Number(v.total), 0);

  const totalPendente = vendas
    .filter(v => v.status === 'pendente')
    .reduce((acc, v) => acc + Number(v.total), 0);

  const formatPagamento = (fp: string) => {
    const map: Record<string, string> = {
      dinheiro: 'Dinheiro', credito: 'Cartão Crédito', debito: 'Cartão Débito',
      pix: 'PIX', boleto: 'Boleto', outro: 'Outro',
    };
    return map[fp] || fp;
  };

  const columns = [
    { key: 'id', header: 'Nº' },
    { key: 'numero_pedido', header: 'Pedido' },
    {
      key: 'data_venda', header: 'Data',
      render: (item: VendaFinanceiro) => item.data_venda ? new Date(item.data_venda).toLocaleDateString('pt-BR') : '-',
    },
    {
      key: 'total', header: 'Valor',
      render: (item: VendaFinanceiro) => `R$ ${Number(item.total).toFixed(2)}`,
    },
    {
      key: 'tipo_pagamento', header: 'Pagamento',
      render: (item: VendaFinanceiro) => formatPagamento(item.tipo_pagamento || ''),
    },
    {
      key: 'status', header: 'Status',
      render: (item: VendaFinanceiro) => {
        const colors: Record<string, string> = {
          concluida: 'bg-green-100 text-green-700',
          pendente: 'bg-yellow-100 text-yellow-700',
          cancelada: 'bg-red-100 text-red-700',
        };
        return (
          <span className={`px-2 py-1 text-xs rounded-full ${colors[item.status] || 'bg-gray-100 text-gray-700'}`}>
            {item.status}
          </span>
        );
      },
    },
  ];

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-800">Financeiro</h1>

      {/* Cards de resumo */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white rounded-xl shadow-sm p-6">
          <p className="text-sm text-gray-500">Total de Vendas</p>
          <p className="text-2xl font-bold text-gray-800 mt-1">{vendas.length}</p>
        </div>
        <div className="bg-white rounded-xl shadow-sm p-6 border-l-4 border-green-500">
          <p className="text-sm text-gray-500">Total Recebido</p>
          <p className="text-2xl font-bold text-green-600 mt-1">R$ {totalRecebido.toFixed(2)}</p>
        </div>
        <div className="bg-white rounded-xl shadow-sm p-6 border-l-4 border-yellow-500">
          <p className="text-sm text-gray-500">Total Pendente</p>
          <p className="text-2xl font-bold text-yellow-600 mt-1">R$ {totalPendente.toFixed(2)}</p>
        </div>
      </div>

      {/* Tabela */}
      <DataTable title="Histórico de Vendas" columns={columns} data={vendas} loading={loading} />
    </div>
  );
}