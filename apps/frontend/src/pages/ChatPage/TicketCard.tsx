import React from 'react';
import { TicketConfirmation } from '../../types/api';
import { SeverityIndicator } from '../../components/shared/SeverityIndicator';
import { StatusBadge } from '../../components/shared/StatusBadge';
import { Landmark, UserCheck, PhoneCall, MapPin } from 'lucide-react';

interface TicketCardProps {
  ticket: TicketConfirmation;
}

export const TicketCard: React.FC<TicketCardProps> = ({ ticket }) => {
  return (
    <div className="bg-white border border-slate-200/80 rounded-xl p-5 shadow-sm max-w-sm overflow-hidden space-y-4 animate-fade-slide">
      {/* Passcard Header metadata details */}
      <div className="flex items-center justify-between border-b border-slate-100 pb-3">
        <div>
          <span className="text-[9px] font-bold text-slate-400 tracking-widest uppercase block leading-none">Engineering ID</span>
          <p className="text-sm font-extrabold text-slate-900 tracking-tight mt-1">{ticket.ticket_number}</p>
        </div>
        <StatusBadge status={ticket.status} />
      </div>

      {/* Attributes core grid */}
      <div className="space-y-3.5">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <span className="text-[9px] font-bold text-slate-400 tracking-widest uppercase block">Defect</span>
            <p className="text-xs font-semibold text-slate-800 mt-0.5">{ticket.defect_type}</p>
          </div>
          <div>
            <span className="text-[9px] font-bold text-slate-400 tracking-widest uppercase block">Assessed Severity</span>
            <div className="mt-1">
              <SeverityIndicator score={ticket.severity_score} />
            </div>
          </div>
        </div>

        {ticket.road_name && (
          <div className="flex items-start gap-2 pt-2.5 border-t border-slate-50">
            <MapPin className="w-3.5 h-3.5 text-slate-400 mt-0.5 shrink-0" />
            <div>
              <span className="text-[9px] font-bold text-slate-400 tracking-widest uppercase block">Location Stretch</span>
              <p className="text-xs font-semibold text-slate-600 leading-tight">
                {ticket.road_name} <span className="text-slate-400 font-medium">({ticket.district})</span>
              </p>
            </div>
          </div>
        )}

        {ticket.executive_engineer_name && (
          <div className="bg-slate-50/70 border border-slate-100 rounded-lg p-3 mt-1.5 space-y-2">
            <span className="text-[9px] font-bold text-slate-400 tracking-widest uppercase block">Responsible Officer</span>
            <div className="flex flex-col gap-1.5">
              <div className="flex items-center gap-1.5 text-xs text-slate-700 font-semibold">
                <UserCheck className="w-3.5 h-3.5 text-blue-500" />
                <span>Engineer {ticket.executive_engineer_name}</span>
              </div>
              {ticket.executive_engineer_contact && (
                <div className="flex items-center gap-1.5 text-xs text-slate-500">
                  <PhoneCall className="w-3.5 h-3.5 text-slate-400" />
                  <a href={`tel:${ticket.executive_engineer_contact}`} className="hover:underline font-medium">
                    {ticket.executive_engineer_contact}
                  </a>
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Metadata stamp panel */}
      <div className="pt-3 border-t border-slate-100 flex items-center justify-between text-[10px] text-slate-400 font-medium">
        <span className="flex items-center gap-1.5">
          <Landmark className="w-3.5 h-3.5 text-slate-400" />
          <span>Sourced from PWD/NHAI</span>
        </span>
        <span className="text-emerald-600 font-semibold">Audit active</span>
      </div>
    </div>
  );
};