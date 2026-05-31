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

  // Client-side search match to enable responsive lookups
  const filteredComplaints = complaints.filter((c) =>
    c.ticket_number.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <PageWrapper>
      <div className="space-y-6">
        {/* Page Title Header */}
        <div className="space-y-1">
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight">Public Accountability Tracker</h1>
          <p className="text-sm text-slate-500 font-medium">
            Verifiably logged complaint lifecycles mapped across active demo districts.
          </p>
        </div>

        {/* Dashboard KPI Statistics */}
        <MetricsCards complaints={complaints} total={total} />

        {/* Filters Controls Panel */}
        <ComplaintFilters
          filters={filters}
          searchTerm={searchTerm}
          onSearchChange={setSearchTerm}
          onFilterChange={updateFilters}
          onReset={handleReset}
        />

        {/* Primary complaint list display */}
        {loading ? (
          <div className="flex justify-center py-12">
            <Spinner />
          </div>
        ) : filteredComplaints.length > 0 ? (
          <ComplaintTable complaints={filteredComplaints} onRowClick={(id) => setSelectedId(id)} />
        ) : (
          <EmptyState message="No complaint records found matching your current filter specifications." />
        )}

        {/* Dynamic Detail Event Inspector Drawer */}
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