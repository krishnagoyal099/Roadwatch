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
    <div className="bg-white border border-slate-200/80 rounded-xl shadow-xs overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-50/70 border-b border-slate-200 text-[10px] font-bold tracking-widest text-slate-400 uppercase">
              <th className="px-6 py-3.5">Ticket ID</th>
              <th className="px-6 py-3.5">Defect Type</th>
              <th className="px-6 py-3.5">Severity</th>
              <th className="px-6 py-3.5">Road Stretch</th>
              <th className="px-6 py-3.5">Responsible Engineer</th>
              <th className="px-6 py-3.5">Status</th>
              <th className="px-6 py-3.5">Logged Date</th>
              <th className="px-6 py-3.5 text-right">Inspect</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 text-xs font-semibold text-slate-700">
            {complaints.map((item) => (
              <tr
                key={item.id}
                onClick={() => onRowClick(item.id)}
                className="hover:bg-slate-50/60 cursor-pointer transition-colors group"
              >
                <td className="px-6 py-4 font-bold text-slate-900 group-hover:text-blue-600 transition-colors">
                  {item.ticket_number}
                </td>
                <td className="px-6 py-4 font-medium text-slate-800">{item.defect_type}</td>
                <td className="px-6 py-4">
                  <SeverityIndicator score={item.severity_score} />
                </td>
                <td className="px-6 py-4 text-slate-500 font-medium">
                  {item.road_name || 'N/A'}
                </td>
                <td className="px-6 py-4 text-slate-500 font-medium">
                  {item.assigned_engineer || 'Unassigned'}
                </td>
                <td className="px-6 py-4">
                  <StatusBadge status={item.status} />
                </td>
                <td className="px-6 py-4 text-slate-400 font-normal">
                  {formatDate(item.created_at)}
                </td>
                <td className="px-6 py-4 text-right">
                  <span className="inline-flex p-1 rounded bg-slate-100 text-slate-400 group-hover:bg-blue-50 group-hover:text-blue-600 transition-colors">
                    <ArrowUpRight className="w-3.5 h-3.5" />
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