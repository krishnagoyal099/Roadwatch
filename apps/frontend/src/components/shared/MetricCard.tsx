import React from 'react';

interface MetricCardProps {
  title: string;
  value: string | number;
  description?: string;
  icon?: React.ReactNode;
}

export const MetricCard: React.FC<MetricCardProps> = ({ title, value, description, icon }) => {
  return (
    <div className="bg-white rounded-xl shadow-xs border border-slate-100 p-5 flex items-start justify-between">
      <div className="space-y-1">
        <p className="text-sm font-medium text-slate-500 uppercase tracking-wider">{title}</p>
        <p className="text-3xl font-bold text-slate-900">{value}</p>
        {description && <p className="text-xs text-slate-400">{description}</p>}
      </div>
      {icon && (
        <div className="p-3 bg-slate-50 rounded-lg text-slate-500">
          {icon}
        </div>
      )}
    </div>
  );
};