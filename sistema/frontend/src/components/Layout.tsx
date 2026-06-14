import { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate, useLocation } from 'react-router-dom';

interface LayoutProps {
  children: React.ReactNode;
}

const menuItems = [
  { path: '/', label: 'Dashboard', icon: '📊' },
  { path: '/clientes', label: 'Clientes', icon: '👥' },
  { path: '/fornecedores', label: 'Fornecedores', icon: '🏭' },
  { path: '/categorias', label: 'Categorias', icon: '📂' },
  { path: '/produtos', label: 'Produtos', icon: '📦' },
  { path: '/vendas', label: 'Vendas', icon: '🛒' },
  { path: '/orcamentos', label: 'Orçamentos', icon: '📝' },
  { path: '/estoque', label: 'Estoque', icon: '📋' },
  { path: '/financeiro', label: 'Financeiro', icon: '💰' },
];

export default function Layout({ children }: LayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <aside className={`${sidebarOpen ? 'w-64' : 'w-20'} bg-slate-800 text-white transition-all duration-300 flex flex-col`}>
        {/* Logo */}
        <button
          onClick={() => navigate('/')}
          className="h-16 w-full flex items-center justify-center border-b border-slate-700 hover:bg-slate-700 transition-colors cursor-pointer"
        >
          <h1 className={`font-bold text-sm leading-tight text-center ${!sidebarOpen && 'hidden'}`}>
            AgenciaRosano<br/>Material de Construção
          </h1>
          <span className={`text-2xl ${sidebarOpen && 'hidden'}`}>🏗️</span>
        </button>

        {/* Menu */}
        <nav className="flex-1 overflow-y-auto py-4">
          {menuItems.map((item) => (
            <button
              key={item.path}
              onClick={() => navigate(item.path)}
              className={`w-full flex items-center gap-3 px-4 py-3 text-sm transition-colors hover:bg-slate-700 ${
                location.pathname === item.path ? 'bg-slate-700 border-r-4 border-yellow-400' : ''
              }`}
            >
              <span className="text-xl">{item.icon}</span>
              <span className={`${!sidebarOpen && 'hidden'}`}>{item.label}</span>
            </button>
          ))}
        </nav>

        {/* Toggle */}
        <button
          onClick={() => setSidebarOpen(!sidebarOpen)}
          className="h-12 border-t border-slate-700 flex items-center justify-center hover:bg-slate-700"
        >
          <span className="text-xl">{sidebarOpen ? '◀' : '▶'}</span>
        </button>
      </aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <header className="h-16 bg-white shadow-sm flex items-center justify-between px-6">
          <h2 className="text-xl font-semibold text-gray-800">
            {menuItems.find((item) => item.path === location.pathname)?.label || 'ERP Material de Construção'}
          </h2>
          
          <div className="flex items-center gap-4">
            <div className="text-right">
              <p className="text-sm font-medium text-gray-700">{user?.nome || 'Usuário'}</p>
              <p className="text-xs text-gray-500">{user?.email || ''}</p>
            </div>
            <button
              onClick={logout}
              className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
            >
              Sair
            </button>
          </div>
        </header>

        {/* Content */}
        <main className="flex-1 overflow-y-auto p-6 bg-gray-50">
          {children}
        </main>
      </div>
    </div>
  );
}