import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { ChatPage } from './pages/ChatPage';
import { DashboardPage } from './pages/DashboardPage';
import { SpendingPage } from './pages/SpendingPage';

export const AppRoutes: React.FC = () => {
  return (
    <Routes>
      <Route path="/" element={<ChatPage />} />
      <Route path="/dashboard" element={<DashboardPage />} />
      <Route path="/spending" element={<SpendingPage />} />
      {/* Fallback boundary redirect */}
      <Route path="*" element={<ChatPage />} />
    </Routes>
  );
};