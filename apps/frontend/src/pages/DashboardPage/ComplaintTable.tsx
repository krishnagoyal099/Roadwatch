import React from 'react';
import { ComplaintSummary } from '../../types/api';
import { StatusBadge } from '../../components/shared/StatusBadge';
import { SeverityIndicator } from '../../components/shared/SeverityIndicator';
import { formatDate } from '../../lib/helpers';
import { ArrowUpRight } from 'lucide-react';

interface ComplaintTableProps {
  complaints: ComplaintSummary[];
  onRowClick: (id: string) => void;
}

export const ComplaintTable: React.FC<ComplaintTableProps> = ({ complaints, onRowClick }) => {
  return (
    <div className="bg-white border border-slate-100 rounded-xl shadow-xs overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-50/75 border-b border-slate-100 text-[11px] font-bold tracking-wider text-slate-400 uppercase">
              <th className="px-6 py-4">Ticket</th>
              <th className="px-6 py-4">Defect Type</th>
              <th className="px-6 py-4">Severity</th>
              <th className="px-6 py-4">Road Name</th>
              <th className="px-6 py-4">Assigned Engineer</th>
              <th className="px-6 py-4">Status</th>
              <th className="px-6 py-4">Date Filed</th>
              <th className="px-6 py-4 text-right">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 text-sm font-medium text-slate-700">
            {complaints.map((item) => (
              <tr
                key={item.id}
                onClick={() => onRowClick(item.id)}
                className="hover:bg-slate-50/50 cursor-pointer transition-colors group"
              >
                <td className="px-6 py-4 font-bold text-slate-900 group-hover:text-blue-600 transition-colors">
                  {item.ticket_number}
                </td>
                <td className="px-6 py-4">{item.defect_type}</td>
                <td className="px-6 py-4">
                  <SeverityIndicator score={item.severity_score} />
                </td>
                <td className="px-6 py-4 text-slate-600">
                  {item.road_name || 'Unassigned Road'}
                </td>
                <td className="px-6 py-4 text-slate-500">
                  {item.assigned_engineer || 'Unassigned'}
                </td>
                <td className="px-6 py-4">
                  <StatusBadge status={item.status} />
                </td>
                <td className="px-6 py-4 text-slate-400 font-normal">
                  {formatDate(item.created_at)}
                </td>
                <td className="px-6 py-4 text-right">
                  <span className="inline-flex p-1 rounded-md bg-slate-50 text-slate-400 group-hover:bg-blue-50 group-hover:text-blue-600 transition-all">
                    <ArrowUpRight className="w-4 h-4" />
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