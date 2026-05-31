import React from 'react';
import { DEFECT_TYPES, STATUS_TYPES } from '../../lib/constants';
import { Input } from '../../components/ui/Input';
import { Filter, RotateCcw } from 'lucide-react';
import { Button } from '../../components/ui/Button';

interface ComplaintFiltersProps {
  filters: {
    status: string;
    defect_type: string;
  };
  searchTerm: string;
  onSearchChange: (val: string) => void;
  onFilterChange: (filters: Partial<{ status: string; defect_type: string }>) => void;
  onReset: () => void;
}

export const ComplaintFilters: React.FC<ComplaintFiltersProps> = ({
  filters,
  searchTerm,
  onSearchChange,
  onFilterChange,
  onReset,
}) => {
  return (
    <div className="bg-white border border-slate-100 rounded-xl p-5 shadow-xs flex flex-col md:flex-row items-center gap-4">
      {/* Search Input Bar */}
      <div className="w-full md:w-1/3">
        <Input
          type="text"
          placeholder="Search ticket number (e.g. RW-1001)..."
          value={searchTerm}
          onChange={(e) => onSearchChange(e.target.value)}
        />
      </div>

      {/* Filter Selectors */}
      <div className="w-full md:flex-1 flex flex-col sm:flex-row items-center gap-3">
        <div className="relative w-full">
          <select
            value={filters.status}
            onChange={(e) => onFilterChange({ status: e.target.value })}
            className="w-full pl-3.5 pr-8 py-2 rounded-lg border border-slate-300 bg-white text-slate-700 text-sm focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 focus:outline-hidden transition-all appearance-none"
          >
            <option value="">All Statuses</option>
            {STATUS_TYPES.map((st) => (
              <option key={st} value={st}>{st}</option>
            ))}
          </select>
          <Filter className="w-4 h-4 text-slate-400 absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none" />
        </div>

        <div className="relative w-full">
          <select
            value={filters.defect_type}
            onChange={(e) => onFilterChange({ defect_type: e.target.value })}
            className="w-full pl-3.5 pr-8 py-2 rounded-lg border border-slate-300 bg-white text-slate-700 text-sm focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 focus:outline-hidden transition-all appearance-none"
          >
            <option value="">All Defect Types</option>
            {DEFECT_TYPES.map((dt) => (
              <option key={dt} value={dt}>{dt}</option>
            ))}
          </select>
          <Filter className="w-4 h-4 text-slate-400 absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none" />
        </div>

        <Button variant="outline" onClick={onReset} className="w-full sm:w-auto shrink-0 flex items-center gap-1.5 border-slate-200">
          <RotateCcw className="w-3.5 h-3.5 text-slate-500" />
          <span>Reset</span>
        </Button>
      </div>
    </div>
  );
};