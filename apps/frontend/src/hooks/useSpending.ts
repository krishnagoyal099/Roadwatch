import { useState, useEffect, useCallback } from 'react';
import { spendingApi } from '../api/spending';
import { SpendingResponse } from '../types/api';

export function useSpending() {
  const [data, setData] = useState<SpendingResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [filters, setFilters] = useState({
    district: '',
    road_type: '',
  });

  const fetchSpending = useCallback(async () => {
    setLoading(true);
    try {
      const response = await spendingApi.getSpending(filters);
      setData(response);
    } catch (err) {
      console.error('Spending aggregate lookup failed', err);
    } finally {
      setLoading(false);
    }
  }, [filters]);

  useEffect(() => {
    fetchSpending();
  }, [fetchSpending]);

  const updateFilters = (newFilters: Partial<typeof filters>) => {
    setFilters((prev) => ({ ...prev, ...newFilters }));
  };

  return { data, loading, filters, updateFilters };
}