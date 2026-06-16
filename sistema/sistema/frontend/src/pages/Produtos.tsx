import { useState, useEffect } from 'react';
import { api } from '../services/api';
import type { Produto, Categoria, Fornecedor } from '../types';
import DataTable from '../components/DataTable';
import Modal from '../components/Modal';

const emptyProduto: Produto = {
  codigo: '', descricao: '', codigo_barras: '', preco_custo: 0, preco_venda: 0,
  estoque_atual: 0, estoque_minimo: 0,
  categoria_id: undefined, ativo: true,
};

export default function Produtos() {
  const [data, setData] = useState<Produto[]>([]);
  const [categorias, setCategorias] = useState<Categoria[]>([]);
  const [fornecedores, setFornecedores] = useState<Fornecedor[]>([]);
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [form, setForm] = useState<Produto>(emptyProduto);
  const [editId, setEditId] = useState<number | null>(null);

  useEffect(() => { load(); loadCategorias(); loadFornecedores(); }, []);

  const load = async () => {
    try {
      const result = await api.getProdutos();
      setData(Array.isArray(result) ? result : []);
    } catch (err) { console.error(err); }
    finally { setLoading(false); }
  };

  const loadCategorias = async () => {
    try { setCategorias(await api.getCategorias()); }
    catch (err) { console.error(err); }
  };

  const loadFornecedores = async () => {
    try { setFornecedores(await api.getFornecedores()); }
    catch (err) { console.error(err); }
  };

  const openNew = () => { setForm(emptyProduto); setEditId(null); setModalOpen(true); };
  const openEdit = (item: Produto) => { setForm(item); setEditId(item.id!); setModalOpen(true); };

  const handleSave = async () => {
    try {
      const payload: any = { ...form };
      if (!payload.codigo) payload.codigo = payload.descricao;
      if (editId) await api.updateProduto(editId, payload);
      else await api.createProduto(payload);
      setModalOpen(false);
      load();
    } catch (err: any) { alert(err.message); }
  };

  const handleDelete = async (item: Produto) => {
    if (!confirm(`Excluir produto ${item.descricao}?`)) return;
    try { await api.deleteProduto(item.id!); load(); }
    catch (err: any) { alert(err.message); }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target;
    setForm(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? (e.target as HTMLInputElement).checked :
              type === 'number' ? Number(value) : value,
    }));
  };

  const columns = [
    { key: 'descricao', header: 'Descrição' },
    { key: 'codigo_barras', header: 'Cód. Barras' },
    {
      key: 'preco_venda', header: 'Preço Venda',
      render: (item: Produto) => `R$ ${Number(item.preco_venda).toFixed(2)}`,
    },
    { key: 'estoque_atual', header: 'Estoque' },
    { key: 'estoque_minimo', header: 'Est. Mínimo' },
    { key: 'categoria_nome', header: 'Categoria' },
    {
      key: 'ativo', header: 'Ativo',
      render: (item: Produto) => (
        <span className={`px-2 py-1 text-xs rounded-full ${item.ativo ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
          {item.ativo ? 'Sim' : 'Não'}
        </span>
      ),
    },
  ];

  return (
    <div>
      <DataTable title="Produtos" columns={columns} data={data} loading={loading}
        onNew={openNew} onEdit={openEdit} onDelete={handleDelete} />
      <Modal open={modalOpen} onClose={() => setModalOpen(false)} title={editId ? 'Editar Produto' : 'Novo Produto'}>
        <form onSubmit={(e) => { e.preventDefault(); handleSave(); }} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Descrição</label>
            <input name="descricao" value={form.descricao} onChange={handleChange} className="w-full border rounded-lg px-3 py-2 text-sm" required />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Código</label>
              <input name="codigo" value={form.codigo || ''} onChange={handleChange} className="w-full border rounded-lg px-3 py-2 text-sm" placeholder="Código interno" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Código de Barras</label>
              <input name="codigo_barras" value={form.codigo_barras || ''} onChange={handleChange} className="w-full border rounded-lg px-3 py-2 text-sm" />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Preço de Custo</label>
              <input name="preco_custo" type="number" step="0.01" value={form.preco_custo} onChange={handleChange} className="w-full border rounded-lg px-3 py-2 text-sm" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Preço de Venda</label>
              <input name="preco_venda" type="number" step="0.01" value={form.preco_venda} onChange={handleChange} className="w-full border rounded-lg px-3 py-2 text-sm" required />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Estoque Atual</label>
              <input name="estoque_atual" type="number" value={form.estoque_atual} onChange={handleChange} className="w-full border rounded-lg px-3 py-2 text-sm" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Estoque Mínimo</label>
              <input name="estoque_minimo" type="number" value={form.estoque_minimo} onChange={handleChange} className="w-full border rounded-lg px-3 py-2 text-sm" />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Categoria</label>
              <select name="categoria_id" value={form.categoria_id || ''} onChange={handleChange} className="w-full border rounded-lg px-3 py-2 text-sm">
                <option value="">Selecione...</option>
                {categorias.filter(c => c.ativo).map(cat => (
                  <option key={cat.id} value={cat.id}>{cat.nome}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Fornecedor</label>
              <select name="fornecedor_id" value={form.fornecedor_id || ''} onChange={handleChange} className="w-full border rounded-lg px-3 py-2 text-sm">
                <option value="">Selecione...</option>
                {fornecedores.filter(f => f.ativo).map(f => (
                  <option key={f.id} value={f.id}>{f.nome}</option>
                ))}
              </select>
            </div>
          </div>
          <label className="flex items-center gap-2 text-sm">
            <input name="ativo" type="checkbox" checked={form.ativo} onChange={handleChange} className="rounded" />
            Produto Ativo
          </label>
          <div className="flex justify-end gap-3 pt-4 border-t">
            <button type="button" onClick={() => setModalOpen(false)} className="px-4 py-2 text-sm text-gray-600 hover:text-gray-800">Cancelar</button>
            <button type="submit" className="px-4 py-2 text-sm bg-slate-800 text-white rounded-lg hover:bg-slate-700">
              {editId ? 'Atualizar' : 'Salvar'}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
}