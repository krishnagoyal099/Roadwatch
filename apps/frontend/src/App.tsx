import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import { Navbar } from './components/layout/Navbar';
import { AppRoutes } from './routes';

const App: React.FC = () => {
  return (
    <Router>
      <div className="min-h-screen flex flex-col bg-slate-50/50">
        <Navbar />
        <main className="flex-1">
          <AppRoutes />
        </main>
      </div>
    </Router>
  );
};

export default App;