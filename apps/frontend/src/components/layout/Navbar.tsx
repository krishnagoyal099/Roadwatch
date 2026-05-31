import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Icons } from '../ui/Icons';

export const Navbar: React.FC = () => {
  const location = useLocation();

  const navItems = [
    { path: '/', label: 'Assistant', icon: <Icons.Chat size={14} /> },
    { path: '/dashboard', label: 'Dashboard', icon: <Icons.Dashboard size={14} /> },
    { path: '/spending', label: 'Spending', icon: <Icons.Landmark size={14} /> },
  ];

  return (
    <header className="sticky top-0 z-40 w-full border-b border-zinc-200/60 bg-white/85 backdrop-blur-md">
      <div className="max-w-6xl mx-auto px-6">
        <div className="flex h-16 items-center justify-between">
          <Link to="/" className="flex items-center gap-3 group">
            {/* Swapped shield-check for the perspective lane brand target logo */}
            <div className="p-2 bg-zinc-950 text-white rounded-lg group-hover:scale-105 transition-transform">
              <Icons.BrandLogo size={16} />
            </div>
            <div className="flex flex-col">
              <span className="font-extrabold text-sm tracking-widest text-zinc-900 font-sans leading-none uppercase">
                ROADWATCH
              </span>
              <span className="text-[9px] font-bold text-zinc-400 uppercase tracking-widest mt-1.5 leading-none">
                Civic Ledger
              </span>
            </div>
          </Link>

          <nav className="flex space-x-1.5 bg-zinc-50 p-1 rounded-xl border border-zinc-200/40">
            {navItems.map((item) => {
              const isActive = location.pathname === item.path;
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-semibold tracking-tight transition-all duration-150 ${
                    isActive
                      ? 'bg-white text-zinc-950 shadow-xs border border-zinc-200/50'
                      : 'text-zinc-500 hover:text-zinc-900 hover:bg-zinc-100/50'
                  }`}
                >
                  {item.icon}
                  <span>{item.label}</span>
                </Link>
              );
            })}
          </nav>
        </div>
      </div>
    </header>
  );
};