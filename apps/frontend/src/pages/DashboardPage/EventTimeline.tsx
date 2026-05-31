import React from 'react';
import { EventTimeline as EventType } from '../../types/api';
import { formatDate } from '../../lib/helpers';
import { Check, AlertCircle, ArrowUpRight } from 'lucide-react';

interface EventTimelineProps {
  events: EventType[];
}

export const EventTimeline: React.FC<EventTimelineProps> = ({ events }) => {
  const getTimelineIndicator = (type: string) => {
    switch (type) {
      case 'Filed':
        return <Check className="w-3 h-3 text-blue-600" />;
      case 'Escalated':
        return <AlertCircle className="w-3 h-3 text-orange-600" />;
      case 'Resolved':
        return <Check className="w-3 h-3 text-emerald-600" />;
      default:
        return <ArrowUpRight className="w-3 h-3 text-slate-600" />;
    }
  };

  const getTimelineBorderColor = (type: string) => {
    switch (type) {
      case 'Filed':
        return 'border-blue-200 bg-blue-50';
      case 'Escalated':
        return 'border-orange-200 bg-orange-50';
      case 'Resolved':
        return 'border-emerald-200 bg-emerald-50';
      default:
        return 'border-slate-200 bg-slate-50';
    }
  };

  return (
    <div className="relative border-l border-slate-200 pl-5 ml-2.5 space-y-6 py-1">
      {events.map((ev) => (
        <div key={ev.id} className="relative">
          {/* Indicator Dot Circle */}
          <div className={`absolute -left-[29px] top-0.5 w-4.5 h-4.5 rounded-full border flex items-center justify-center shrink-0 z-10 ${
            getTimelineBorderColor(ev.event_type)
          }`}>
            {getTimelineIndicator(ev.event_type)}
          </div>

          {/* Core Event Stamp */}
          <div className="space-y-1">
            <div className="flex items-baseline gap-2">
              <span className="text-xs font-bold text-slate-800">{ev.event_type}</span>
              <span className="text-[10px] font-semibold text-slate-400">
                {formatDate(ev.created_at)}
              </span>
            </div>
            {ev.event_note && (
              <p className="text-xs text-slate-500 leading-relaxed max-w-sm font-medium">
                {ev.event_note}
              </p>
            )}
          </div>
        </div>
      ))}
    </div>
  );
};