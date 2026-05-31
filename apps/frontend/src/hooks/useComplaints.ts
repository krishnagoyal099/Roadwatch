import { useState, useEffect, useCallback } from 'react';
import { complaintsApi } from '../api/complaints';
import { ComplaintSummary } from '../types/api';

export function useComplaints() {
  const [complaints, setComplaints] = useState<ComplaintSummary[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [filters, setFilters] = useState({
    status: '',
    defect_type: '',
    limit: 50,
    offset: 0,
  });

  const fetchComplaints = useCallback(async () => {
    setLoading(true);
    try {
      const response = await complaintsApi.list(filters);
      setComplaints(response.complaints);
      setTotal(response.total);
    } catch (err) {
      console.error('Complaints query failed', err);
    } finally {
      setLoading(false);
    }
  }, [filters]);

  useEffect(() => {
    fetchComplaints();
  }, [fetchComplaints]);

  const updateFilters = (newFilters: Partial<typeof filters>) => {
    setFilters((prev) => ({ ...prev, ...newFilters, offset: 0 }));
  };

  return { complaints, total, loading, filters, updateFilters, refetch: fetchComplaints };
}