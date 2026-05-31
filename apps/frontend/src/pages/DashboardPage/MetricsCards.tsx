import React from 'react';
import { ComplaintSummary } from '../../types/api';
import { MetricCard } from '../../components/shared/MetricCard';
import { AlertCircle, CheckCircle, ShieldAlert } from 'lucide-react';

interface MetricsCardsProps {
  complaints: ComplaintSummary[];
  total: number;
}

export const MetricsCards: React.FC<MetricsCardsProps> = ({ complaints, total }) => {
  const resolved = complaints.filter((c) => c.status === 'Resolved').length;
  
  const avgSeverity = total > 0 
    ? (complaints.reduce((acc, c) => acc + c.severity_score, 0) / complaints.length).toFixed(1)
    : '0.0';

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
      <MetricCard
        title="Total Complaints Filed"
        value={total}
        description="Public tickets logged"
        icon={<ShieldAlert className="w-6 h-6 text-blue-600" />}
      />
      <MetricCard
        title="Complaints Resolved"
        value={`${resolved} Resolved`}
        description="Completed field repairs"
        icon={<CheckCircle className="w-6 h-6 text-emerald-600" />}
      />
      <MetricCard
        title="Average Severity"
        value={`${avgSeverity} / 5`}
        description="Calculated priority density"
        icon={<AlertCircle className="w-6 h-6 text-amber-600" />}
      />
    </div>
  );
};