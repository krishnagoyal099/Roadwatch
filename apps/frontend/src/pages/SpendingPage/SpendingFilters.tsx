import React from 'react';
import { ROAD_TYPES } from '../../lib/constants';
import { Filter } from 'lucide-react';

interface SpendingFiltersProps {
  filters: {
    district: string;
    road_type: string;
  };
  onFilterChange: (filters: Partial<{ district: string; road_type: string }>) => void;
}

export const SpendingFilters: React.FC<SpendingFiltersProps> = ({ filters, onFilterChange }) => {
  return (
    <div className="bg-white border border-slate-100 rounded-xl p-5 shadow-xs flex flex-col sm:flex-row items-center gap-4">
      {/* Demo Specific District filter */}
      <div className="relative w-full">
        <select
          value={filters.district}
          onChange={(e) => onFilterChange({ district: e.target.value })}
          className="w-full pl-3.5 pr-8 py-2 rounded-lg border border-slate-300 bg-white text-slate-700 text-sm focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 focus:outline-hidden transition-all appearance-none"
        >
          <option value="">All Districts</option>
          <option value="Bengaluru">Bengaluru Demo District</option>
        </select>
        <Filter className="w-4 h-4 text-slate-400 absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none" />
      </div>

      {/* Road classification types */}
      <div className="relative w-full">
        <select
          value={filters.road_type}
          onChange={(e) => onFilterChange({ road_type: e.target.value })}
          className="w-full pl-3.5 pr-8 py-2 rounded-lg border border-slate-300 bg-white text-slate-700 text-sm focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 focus:outline-hidden transition-all appearance-none"
        >
          <option value="">All Road Types</option>
          {ROAD_TYPES.map((rt) => (
            <option key={rt} value={rt}>
              {rt === 'NH' ? 'National Highway (NH)' : rt === 'SH' ? 'State Highway (SH)' : `${rt} Road`}
            </option>
          ))}
        </select>
        <Filter className="w-4 h-4 text-slate-400 absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none" />
      </div>
    </div>
  );
};