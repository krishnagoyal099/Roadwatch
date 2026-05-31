import React from 'react';
import { SegmentSpending } from '../../types/api';
import { formatDate, formatCurrencyLakhs } from '../../lib/helpers';
import { AlertTriangle, HardHat } from 'lucide-react';

interface SpendingTableProps {
  segments: SegmentSpending[];
}

export const SpendingTable: React.FC<SpendingTableProps> = ({ segments }) => {
  // Colour codes segment rows based on outstanding complaint density
  const getComplaintColor = (count: number) => {
    if (count === 0) return 'bg-emerald-50 text-emerald-700 border-emerald-200';
    if (count <= 3) return 'bg-amber-50 text-amber-700 border-amber-200';
    return 'bg-rose-50 text-rose-700 border-rose-200';
  };

  return (
    <div className="bg-white border border-slate-100 rounded-xl shadow-xs overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-50/75 border-b border-slate-100 text-[11px] font-bold tracking-wider text-slate-400 uppercase">
              <th className="px-6 py-4">Road Stretch</th>
              <th className="px-6 py-4">Road Type</th>
              <th className="px-6 py-4">Primary Contractor</th>
              <th className="px-6 py-4">Sanctioned Budget</th>
              <th className="px-6 py-4">Last Maintenance Date</th>
              <th className="px-6 py-4">Active Complaints</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 text-sm font-medium text-slate-700">
            {segments.map((seg, idx) => (
              <tr key={idx} className="hover:bg-slate-50/25 transition-colors">
                <td className="px-6 py-4 font-bold text-slate-900">{seg.road_name || 'N/A'}</td>
                <td className="px-6 py-4 text-xs font-bold text-slate-400">{seg.road_type}</td>
                <td className="px-6 py-4">
                  <div className="flex items-center gap-1.5 text-slate-600">
                    <HardHat className="w-3.5 h-3.5 text-slate-400" />
                    <span>{seg.contractor_name || 'Uncontracted'}</span>
                  </div>
                </td>
                <td className="px-6 py-4 font-bold text-slate-900">
                  {formatCurrencyLakhs(seg.budget_sanctioned_lakhs)}
                </td>
                <td className="px-6 py-4 text-slate-400 font-normal">
                  {formatDate(seg.last_maintenance_date)}
                </td>
                <td className="px-6 py-4">
                  <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-bold border ${
                    getComplaintColor(seg.open_complaints)
                  }`}>
                    {seg.open_complaints > 3 && <AlertTriangle className="w-3.5 h-3.5" />}
                    <span>{seg.open_complaints} Open</span>
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};