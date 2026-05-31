import React from 'react';
import { useSpending } from '../../hooks/useSpending';
import { MetricsCards } from './MetricsCards';
import { SpendingFilters } from './SpendingFilters';
import { SpendingTable } from './SpendingTable';
import { PageWrapper } from '../../components/layout/PageWrapper';
import { EmptyState } from '../../components/shared/EmptyState';
import { Spinner } from '../../components/ui/Spinner';

export const SpendingPage: React.FC = () => {
  const { data, loading, filters, updateFilters } = useSpending();

  return (
    <PageWrapper>
      <div className="space-y-6">
        {/* Page Title Header */}
        <div className="space-y-1">
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight">Public Fiscal Spending</h1>
          <p className="text-sm text-slate-500 font-medium">
            Cross-referenced public infrastructure budgets mapped with outstanding quality metrics.
          </p>
        </div>

        {/* Aggregated Spending KPI Statistics Cards */}
        <MetricsCards data={data} />

        {/* Filters Panel bar */}
        <SpendingFilters filters={filters} onFilterChange={updateFilters} />

        {/* Primary Fiscal Stretches list display */}
        {loading ? (
          <div className="flex justify-center py-12">
            <Spinner />
          </div>
        ) : data && data.segments.length > 0 ? (
          <SpendingTable segments={data.segments} />
        ) : (
          <EmptyState message="No segment contracts or fiscal records resolved matching selected options." />
        )}
      </div>
    </PageWrapper>
  );
};