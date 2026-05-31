import React from 'react';
import { TicketConfirmation } from '../../types/api';
import { SeverityIndicator } from './SeverityIndicator';
import { StatusBadge } from './StatusBadge';
import { Landmark, UserCheck, PhoneCall, MapPin, Percent } from 'lucide-react';
import { cn } from '../../lib/helpers';

interface TicketCardProps {
  ticket: TicketConfirmation;
}

export const TicketCard: React.FC<TicketCardProps> = ({ ticket }) => {
  return (
    <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-md w-full max-w-md overflow-hidden space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-100 pb-3">
        <div>
          <span className="text-xs font-bold text-slate-400 tracking-wider uppercase">Engineering Ticket</span>
          <p className="text-lg font-extrabold text-slate-800">{ticket.ticket_number}</p>
        </div>
        <StatusBadge status={ticket.status} />
      </div>
      {/* Body */}
      <div className="space-y-3.5">
        <div>
          <span className="text-[10px] uppercase font-bold tracking-wider text-slate-400">Classified Defect</span>
          <p className="text-sm font-semibold text-slate-700">{ticket.defect_type}</p>
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <span className="text-[10px] uppercase font-bold tracking-wider text-slate-400">Model Confidence</span>
            <div className="flex items-center gap-1 text-sm font-semibold text-slate-700">
              <Percent className="w-3.5 h-3.5 text-blue-500" />
              <span>{ticket.confidence_pct}%</span>
            </div>
          </div>
          <div>
            <span className="text-[10px] uppercase font-bold tracking-wider text-slate-400">Assessed Severity</span>
            <SeverityIndicator score={ticket.severity_score} />
          </div>
        </div>
        {ticket.road_name && (
          <div className="flex items-start gap-2 pt-2 border-t border-slate-50">
            <MapPin className="w-4 h-4 text-slate-400 mt-0.5 shrink-0" />
            <div>
              <span className="text-[10px] uppercase font-bold tracking-wider text-slate-400 block leading-none">Matched Segment</span>
              <span className="text-xs font-semibold text-slate-600">{ticket.road_name} ({ticket.district || 'District'})</span>
            </div>
          </div>
        )}
        {ticket.executive_engineer_name && (
          <div className="bg-slate-50 rounded-lg p-3 mt-1.5 space-y-2">
            <span className="text-[10px] uppercase font-bold tracking-wider text-slate-400 block">Responsible Authority</span>
            <div className="flex flex-col gap-1">
              <div className="flex items-center gap-1.5 text-xs text-slate-700 font-semibold">
                <UserCheck className="w-3.5 h-3.5 text-blue-500" />
                <span>Engineer {ticket.executive_engineer_name}</span>
              </div>
              {ticket.executive_engineer_contact && (
                <div className="flex items-center gap-1.5 text-xs text-slate-500">
                  <PhoneCall className="w-3.5 h-3.5 text-slate-400" />
                  <a href={`tel:${ticket.executive_engineer_contact}`} className="hover:underline hover:text-blue-600 font-medium">
                    {ticket.executive_engineer_contact}
                  </a>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
      {/* Footer */}
      <div className="pt-3 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-400 font-semibold">
        <span className="flex items-center gap-1">
          <Landmark className="w-3.5 h-3.5" />
          <span>Sourced from PWD/NHAI</span>
        </span>
        <span>Audit logging active</span>
      </div>
    </div>
  );
};
