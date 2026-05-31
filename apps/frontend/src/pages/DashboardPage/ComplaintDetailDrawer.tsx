import React, { useEffect, useState } from 'react';
import { complaintsApi } from '../../api/complaints';
import { ComplaintDetail } from '../../types/api';
import { EventTimeline } from './EventTimeline';
import { StatusBadge } from '../../components/shared/StatusBadge';
import { SeverityIndicator } from '../../components/shared/SeverityIndicator';
import { Button } from '../../components/ui/Button';
import { Spinner } from '../../components/ui/Spinner';
import { formatDate } from '../../lib/helpers'; // <-- Fixed relative path import
import { X, Calendar, Landmark, MapPin, BadgeInfo } from 'lucide-react';

interface ComplaintDetailDrawerProps {
  id: string;
  onClose: () => void;
  onStatusUpdated: () => void;
}

export const ComplaintDetailDrawer: React.FC<ComplaintDetailDrawerProps> = ({
  id,
  onClose,
  onStatusUpdated,
}) => {
  const [detail, setDetail] = useState<ComplaintDetail | null>(null);
  const [loading, setLoading] = useState(false);
  const [updating, setUpdating] = useState(false);

  useEffect(() => {
    async function loadDetail() {
      setLoading(true);
      try {
        const data = await complaintsApi.getById(id);
        setDetail(data);
      } catch (err) {
        console.error('Detail fetch failed', err);
      } finally {
        setLoading(false);
      }
    }
    loadDetail();
  }, [id]);

  const handleUpdateStatus = async (newStatus: 'Filed' | 'Escalated' | 'Resolved') => {
    setUpdating(true);
    try {
      await complaintsApi.updateStatus(id, {
        new_status: newStatus,
        event_note: `Manual state transitioned by operator during review to ${newStatus}.`,
      });
      const data = await complaintsApi.getById(id);
      setDetail(data);
      onStatusUpdated();
    } catch (err) {
      console.error('Status transition failed', err);
    } finally {
      setUpdating(false);
    }
  };

  return (
    <div className="fixed inset-y-0 right-0 z-50 w-full max-w-xl bg-white shadow-2xl border-l border-slate-200 flex flex-col h-full overflow-hidden">
      {/* Header Panel */}
      <div className="bg-slate-900 text-white px-6 py-5 flex items-center justify-between shadow-sm">
        <div>
          <span className="text-[10px] font-bold tracking-wider uppercase text-slate-400">Complaint Tracker ID</span>
          <h2 className="text-lg font-bold flex items-center gap-2">
            <span>{detail?.ticket_number || 'Loading...'}</span>
          </h2>
        </div>
        <button onClick={onClose} className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 cursor-pointer">
          <X className="w-5 h-5" />
        </button>
      </div>

      {loading ? (
        <div className="flex-1 flex flex-col items-center justify-center gap-2">
          <Spinner />
          <span className="text-xs text-slate-400 font-semibold">Resolving record metadata...</span>
        </div>
      ) : detail ? (
        <div className="flex-1 overflow-y-auto px-6 py-6 space-y-6">
          {/* Defect primary view */}
          <div className="flex flex-col sm:flex-row gap-5 items-start">
            {detail.image_url && (
              <img
                src={detail.image_url}
                alt="Defect visual log"
                className="w-full sm:w-44 h-44 object-cover rounded-xl border border-slate-100 shadow-xs shrink-0"
              />
            )}
            <div className="space-y-3 flex-1">
              <div className="flex items-center justify-between">
                <p className="text-xl font-bold text-slate-800">{detail.defect_type}</p>
                <StatusBadge status={detail.status} />
              </div>
              <SeverityIndicator score={detail.severity_score} />
              <div className="flex items-center gap-1.5 text-xs font-bold text-slate-400 bg-slate-50 px-3 py-1 rounded-md w-fit">
                <BadgeInfo className="w-3.5 h-3.5 text-slate-400" />
                <span>Detection Confidence: {detail.confidence_pct}%</span>
              </div>
            </div>
          </div>

          {/* Quick Demo-Prep update trigger button array */}
          <div className="bg-blue-50/50 border border-blue-100 rounded-xl p-4 space-y-3">
            <span className="text-[10px] font-bold text-blue-500 uppercase tracking-wider block">
              Administrative Control Hub (Demo Tool)
            </span>
            <div className="flex flex-wrap gap-2">
              <Button
                variant="outline"
                disabled={updating || detail.status === 'Filed'}
                onClick={() => handleUpdateStatus('Filed')}
                className="h-8 text-xs px-3 bg-white hover:bg-slate-50 border-slate-200"
              >
                Reset to Filed
              </Button>
              <Button
                variant="outline"
                disabled={updating || detail.status === 'Escalated'}
                onClick={() => handleUpdateStatus('Escalated')}
                className="h-8 text-xs px-3 bg-white hover:bg-slate-50 text-orange-600 border-orange-200 hover:bg-orange-50/20"
              >
                Escalate Ticket
              </Button>
              <Button
                variant="outline"
                disabled={updating || detail.status === 'Resolved'}
                onClick={() => handleUpdateStatus('Resolved')}
                className="h-8 text-xs px-3 bg-white hover:bg-slate-50 text-emerald-600 border-emerald-200 hover:bg-emerald-50/20"
              >
                Mark Resolved
              </Button>
              {updating && <Spinner />}
            </div>
          </div>

          {/* Geographic matching details */}
          <div className="border-t border-b border-slate-100 py-4.5 grid grid-cols-2 gap-4">
            <div className="flex items-start gap-2">
              <MapPin className="w-4 h-4 text-slate-400 mt-0.5 shrink-0" />
              <div>
                <span className="text-[10px] font-bold tracking-wider text-slate-400 uppercase block">Matched Location</span>
                <span className="text-xs font-semibold text-slate-700">{detail.road_name || 'N/A'}</span>
                {detail.district && (
                  <span className="text-[10px] font-bold text-slate-400 block">{detail.district} District</span>
                )}
              </div>
            </div>
            <div className="flex items-start gap-2">
              <Calendar className="w-4 h-4 text-slate-400 mt-0.5 shrink-0" />
              <div>
                <span className="text-[10px] font-bold tracking-wider text-slate-400 uppercase block">Report Timeline</span>
                <span className="text-xs font-semibold text-slate-700 block">Logged: {formatDate(detail.created_at)}</span>
              </div>
            </div>
          </div>

          {/* Fiscal segment assignments */}
          <div className="space-y-3 bg-slate-50/75 rounded-xl p-4">
            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">Contractor Assignment Layer</span>
            <div className="grid grid-cols-2 gap-3.5 text-xs">
              <div>
                <span className="text-[10px] font-bold text-slate-400 uppercase block">Engineering Executive</span>
                <span className="font-semibold text-slate-700 block">{detail.executive_engineer_name || 'R. Kumar'}</span>
                <span className="text-[10px] text-slate-500">{detail.executive_engineer_contact || '99001-23456'}</span>
              </div>
              <div>
                <span className="text-[10px] font-bold text-slate-400 uppercase block">Assigned Contractor</span>
                <span className="font-semibold text-slate-700 block">{detail.contractor_name || 'NCC Ltd'}</span>
                <div className="flex items-center gap-1 mt-0.5 font-semibold text-slate-500">
                  <Landmark className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                  <span>Budget: ₹{detail.budget_sanctioned || 150}L</span>
                </div>
              </div>
            </div>
          </div>

          {/* Audit Trail Timeline */}
          <div className="space-y-4">
            <h3 className="text-xs font-bold text-slate-400 tracking-wider uppercase">Public Audit Timeline Trail</h3>
            <EventTimeline events={detail.events} />
          </div>
        </div>
      ) : (
        <div className="flex-1 p-6">Complaint record could not be resolved.</div>
      )}
    </div>
  );
};