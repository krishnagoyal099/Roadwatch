import { apiClient } from '../lib/axios';
import { SpendingResponse } from '../types/api';

export const spendingApi = {
  getSpending: async (filters: { district?: string; road_type?: string }): Promise<SpendingResponse> => {
    const response = await apiClient.get<SpendingResponse>('/api/spending', {
      params: filters,
    });
    return response.data;
  },
};