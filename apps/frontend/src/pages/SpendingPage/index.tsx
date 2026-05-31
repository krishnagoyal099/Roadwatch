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
      <div className="space-y-8 animate-slide-up">
        {/* Editorial-style header */}
        <div className="space-y-2 border-b border-zinc-200/60 pb-5">
          <h1 className="text-5xl font-serif font-light text-zinc-950 leading-none tracking-tight">
            Infrastructure spending.
          </h1>
          <p className="text-xs text-zinc-500 font-semibold uppercase tracking-widest">
            Public project budgets mapped with quality performance metrics
          </p>
        </div>

        <MetricsCards data={data} />

        <SpendingFilters filters={filters} onFilterChange={updateFilters} />

        {loading ? (
          <div className="flex justify-center py-16">
            <Spinner />
          </div>
        ) : data && data.segments.length > 0 ? (
          <SpendingTable segments={data.segments} />
        ) : (
          <EmptyState message="No budget records returned for this filter criteria." />
        )}
      </div>
    </PageWrapper>
  );
};