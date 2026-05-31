import React from 'react';
import { SpendingResponse } from '../../types/api';
import { MetricCard } from '../../components/shared/MetricCard';
import { Landmark, ClipboardList, HardHat, FileBadge2 } from 'lucide-react';

interface MetricsCardsProps {
  data: SpendingResponse | null;
}

export const MetricsCards: React.FC<MetricsCardsProps> = ({ data }) => {
  const totalBudget = data?.total_budget_sanctioned_lakhs || 0;
  const totalSegments = data?.total_road_segments || 0;
  const totalContractors = data?.total_contractors || 0;
  
  // Calculate total active complaints density
  const totalComplaints = data?.segments.reduce((acc, s) => acc + s.open_complaints, 0) || 0;

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
      <MetricCard
        title="Sanctioned Budget"
        value={`₹${totalBudget.toLocaleString('en-IN')} L`}
        description="Public PWD / NHAI allocations"
        icon={<Landmark className="w-6 h-6 text-blue-600" />}
      />
      <MetricCard
        title="Covered Segments"
        value={totalSegments}
        description="Demo road stretches preloaded"
        icon={<ClipboardList className="w-6 h-6 text-slate-600" />}
      />
      <MetricCard
        title="Active Contractors"
        value={totalContractors}
        description="Infrastructure developers"
        icon={<HardHat className="w-6 h-6 text-amber-600" />}
      />
      <MetricCard
        title="Total Open Complaints"
        value={totalComplaints}
        description="Stretches with active defects"
        icon={<FileBadge2 className="w-6 h-6 text-rose-600" />}
      />
    </div>
  );
};