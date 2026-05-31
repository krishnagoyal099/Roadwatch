import React from 'react';
import { EventTimeline as EventType } from '../../types/api';
import { formatDate } from '../../lib/helpers';
import { FilePlus, Sparkles, ShieldCheck, ClipboardCheck } from 'lucide-react';

interface EventTimelineProps {
  events: EventType[];
}

export const EventTimeline: React.FC<EventTimelineProps> = ({ events }) => {
  const getTimelineIcon = (type: string) => {
    switch (type) {
      case 'Filed':
        return <FilePlus className="w-4 h-4 text-blue-600" />;
      case 'Escalated':
        return <Sparkles className="w-4 h-4 text-orange-600" />;
      case 'Resolved':
        return <ShieldCheck className="w-4 h-4 text-emerald-600" />;
      default:
        return <ClipboardCheck className="w-4 h-4 text-slate-600" />;
    }
  };

  const getTimelineBadgeColor = (type: string) => {
    switch (type) {
      case 'Filed':
        return 'bg-blue-50 border-blue-200';
      case 'Escalated':
        return 'bg-orange-50 border-orange-200';
      case 'Resolved':
        return 'bg-emerald-50 border-emerald-200';
      default:
        return 'bg-slate-50 border-slate-200';
    }
  };

  return (
    <div className="relative border-l-2 border-slate-100 pl-6 ml-3 space-y-6 py-2">
      {events.map((ev) => (
        <div key={ev.id} className="relative group">
          {/* Indicator Dot Circle */}
          <div className={`absolute -left-[35px] top-1 w-6 h-6 rounded-full border flex items-center justify-center shrink-0 z-10 ${
            getTimelineBadgeColor(ev.event_type)
          }`}>
            {getTimelineIcon(ev.event_type)}
          </div>

          {/* Core metadata details */}
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="text-sm font-bold text-slate-800">{ev.event_type}</span>
              <span className="text-[10px] font-semibold text-slate-400 bg-slate-100 px-2 py-0.5 rounded-md">
                {formatDate(ev.created_at)}
              </span>
            </div>
            {ev.event_note && (
              <p className="text-xs text-slate-500 leading-relaxed max-w-md font-medium">
                {ev.event_note}
              </p>
            )}
          </div>
        </div>
      ))}
    </div>
  );
};