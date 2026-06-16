import { useState, useEffect } from 'react';
import { api } from '../services/api';
import type { Cliente } from '../types';
import DataTable from '../components/DataTable';
import Modal from '../components/Modal';

const emptyCliente: Cliente = {
  nome: '', cpf_cnpj: '', telefone: '', email: '', endereco: '',
  cidade: '', estado: '', cep: '', ativo: true,
};

export default function Clientes() {
  const [clientes, setClientes] = useState<Cliente[]>([]);
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [form, setForm] = useState<Cliente>(emptyCliente);
  const [editId, setEditId] = useState<number | null>(null);

  useEffect(() => { load(); }, []);

  const load = async () => {
    try {
      const data = await api.getClientes();
      setClientes(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error('Erro ao carregar clientes:', err);
    } finally {
      setLoading(false);
    }
  };

  const openNew = () => {
    setForm(emptyCliente);
    setEditId(null);
    setModalOpen(true);
  };

  const openEdit = (item: Cliente) => {
    setForm(item);
    setEditId(item.id!);
    setModalOpen(true);
  };

  const handleSave = async () => {
    try {
      if (editId) {
        await api.updateCliente(editId, form);
      } else {
        await api.createCliente(form);
      }
      setModalOpen(false);
      load();
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleDelete = async (item: Cliente) => {
    if (!confirm(`Excluir cliente ${item.nome}?`)) return;
    try {
      await api.deleteCliente(item.id!);
      load();
    } catch (err: any) {
      alert(err.message);
    }
  };

  const columns = [
    { key: 'nome', header: 'Nome' },
    { key: 'cpf_cnpj', header: 'CPF/CNPJ' },
    { key: 'telefone', header: 'Telefone' },
    { key: 'email', header: 'E-mail' },
    { key: 'cidade', header: 'Cidade' },
    { key: 'estado', header: 'Estado' },
    {
      key: 'ativo', header: 'Ativo',
      render: (item: Cliente) => (
        <span className={`px-2 py-1 text-xs rounded-full ${item.ativo ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
          {item.ativo ? 'Sim' : 'Não'}
        </span>
      ),
    },
  ];

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    setForm(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? (e.target as HTMLInputElement).checked : value,
    }));
  };

  return (
    <div>
      <DataTable
        title="Clientes"
        columns={columns}
        data={clientes}
        loading={loading}
        onNew={openNew}
        onEdit={openEdit}
        onDelete={handleDelete}
      />

      <Modal open={modalOpen} onClose={() => setModalOpen(false)} title={editId ? 'Editar Cliente' : 'Novo Cliente'}>
        <form onSubmit={(e) => { e.preventDefault(); handleSave(); }} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Nome</label>
            <input name="nome" value={form.nome} onChange={handleChange} className="w-full border rounded-lg px-3 py-2 text-sm" required />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">CPF/CNPJ</label>
              <input name="cpf_cnpj" value={form.cpf_cnpj} onChange={handleChange} className="w-full border rounded-lg px-3 py-2 text-sm" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Telefone</label>
              <input name="telefone" value={form.telefone} onChange={handleChange} className="w-full border rounded-lg px-3 py-2 text-sm" />
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">E-mail</label>
            <input name="email" type="email" value={form.email} onChange={handleChange} className="w-full border rounded-lg px-3 py-2 text-sm" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Endereço</label>
            <input name="endereco" value={form.endereco} onChange={handleChange} className="w-full border rounded-lg px-3 py-2 text-sm" />
          </div>
          <div className="grid grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Cidade</label>
              <input name="cidade" value={form.cidade} onChange={handleChange} className="w-full border rounded-lg px-3 py-2 text-sm" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Estado</label>
              <input name="estado" value={form.estado} onChange={handleChange} className="w-full border rounded-lg px-3 py-2 text-sm" maxLength={2} />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">CEP</label>
              <input name="cep" value={form.cep} onChange={handleChange} className="w-full border rounded-lg px-3 py-2 text-sm" />
            </div>
          </div>
          <label className="flex items-center gap-2 text-sm">
            <input name="ativo" type="checkbox" checked={form.ativo} onChange={handleChange} className="rounded" />
            Cliente Ativo
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