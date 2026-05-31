import React, { useState } from 'react';
import { useComplaints } from '../../hooks/useComplaints';
import { MetricsCards } from './MetricsCards';
import { ComplaintFilters } from './ComplaintFilters';
import { ComplaintTable } from './ComplaintTable';
import { ComplaintDetailDrawer } from './ComplaintDetailDrawer';
import { PageWrapper } from '../../components/layout/PageWrapper';
import { EmptyState } from '../../components/shared/EmptyState';
import { Spinner } from '../../components/ui/Spinner';

export const DashboardPage: React.FC = () => {
  const { complaints, total, loading, filters, updateFilters, refetch } = useComplaints();
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedId, setSelectedId] = useState<string | null>(null);

  const handleReset = () => {
    setSearchTerm('');
    updateFilters({ status: '', defect_type: '' });
  };

  const filteredComplaints = complaints.filter((c) =>
    c.ticket_number.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <PageWrapper>
      <div className="space-y-8 animate-slide-up">
        {/* Editorial-style header */}
        <div className="space-y-2 border-b border-zinc-200/60 pb-5">
          <h1 className="text-5xl font-serif font-light text-zinc-950 leading-none tracking-tight">
            Accountability ledger.
          </h1>
          <p className="text-xs text-zinc-500 font-semibold uppercase tracking-widest">
            Cross-referenced public road database & civic response logs
          </p>
        </div>

        <MetricsCards complaints={complaints} total={total} />

        <ComplaintFilters
          filters={filters}
          searchTerm={searchTerm}
          onSearchChange={setSearchTerm}
          onFilterChange={updateFilters}
          onReset={handleReset}
        />

        {loading ? (
          <div className="flex justify-center py-16">
            <Spinner />
          </div>
        ) : filteredComplaints.length > 0 ? (
          <ComplaintTable complaints={filteredComplaints} onRowClick={(id) => setSelectedId(id)} />
        ) : (
          <EmptyState message="No complaints registered under current filter options." />
        )}

        {selectedId && (
          <ComplaintDetailDrawer
            id={selectedId}
            onClose={() => setSelectedId(null)}
            onStatusUpdated={refetch}
          />
        )}
      </div>
    </PageWrapper>
  );
};