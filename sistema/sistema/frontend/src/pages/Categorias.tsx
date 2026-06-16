import { useState, useEffect } from 'react';
import { api } from '../services/api';
import type { Categoria } from '../types';
import DataTable from '../components/DataTable';
import Modal from '../components/Modal';

const emptyCategoria: Categoria = { nome: '', descricao: '', ativo: true };

export default function Categorias() {
  const [data, setData] = useState<Categoria[]>([]);
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [form, setForm] = useState<Categoria>(emptyCategoria);
  const [editId, setEditId] = useState<number | null>(null);

  useEffect(() => { load(); }, []);

  const load = async () => {
    try {
      const result = await api.getCategorias();
      setData(Array.isArray(result) ? result : []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const openNew = () => { setForm(emptyCategoria); setEditId(null); setModalOpen(true); };
  const openEdit = (item: Categoria) => { setForm(item); setEditId(item.id!); setModalOpen(true); };

  const handleSave = async () => {
    try {
      if (editId) await api.updateCategoria(editId, form);
      else await api.createCategoria(form);
      setModalOpen(false);
      load();
    } catch (err: any) { alert(err.message); }
  };

  const handleDelete = async (item: Categoria) => {
    if (!confirm(`Excluir categoria ${item.nome}?`)) return;
    try { await api.deleteCategoria(item.id!); load(); }
    catch (err: any) { alert(err.message); }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target;
    setForm(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? (e.target as HTMLInputElement).checked : value,
    }));
  };

  const columns = [
    { key: 'nome', header: 'Nome' },
    { key: 'descricao', header: 'Descrição' },
    {
      key: 'ativo', header: 'Ativo',
      render: (item: Categoria) => (
        <span className={`px-2 py-1 text-xs rounded-full ${item.ativo ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
          {item.ativo ? 'Sim' : 'Não'}
        </span>
      ),
    },
  ];

  return (
    <div>
      <DataTable title="Categorias" columns={columns} data={data} loading={loading}
        onNew={openNew} onEdit={openEdit} onDelete={handleDelete} />
      <Modal open={modalOpen} onClose={() => setModalOpen(false)} title={editId ? 'Editar Categoria' : 'Nova Categoria'}>
        <form onSubmit={(e) => { e.preventDefault(); handleSave(); }} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Nome</label>
            <input name="nome" value={form.nome} onChange={handleChange} className="w-full border rounded-lg px-3 py-2 text-sm" required />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Descrição</label>
            <textarea name="descricao" value={form.descricao} onChange={handleChange} className="w-full border rounded-lg px-3 py-2 text-sm" rows={3} />
          </div>
          <label className="flex items-center gap-2 text-sm">
            <input name="ativo" type="checkbox" checked={form.ativo} onChange={handleChange} className="rounded" />
            Categoria Ativa
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