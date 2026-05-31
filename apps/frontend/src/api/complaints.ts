import { apiClient } from '../lib/axios';
import { ComplaintListResponse, ComplaintDetail, StatusUpdate } from '../types/api';

export const complaintsApi = {
  list: async (filters: {
    status?: string;
    defect_type?: string;
    limit?: number;
    offset?: number;
  }): Promise<ComplaintListResponse> => {
    const response = await apiClient.get<ComplaintListResponse>('/api/complaints', {
      params: filters,
    });
    return response.data;
  },

  getById: async (id: string): Promise<ComplaintDetail> => {
    const response = await apiClient.get<ComplaintDetail>(`/api/complaints/${id}`);
    return response.data;
  },

  updateStatus: async (id: string, update: StatusUpdate): Promise<any> => {
    const response = await apiClient.patch(`/api/complaints/${id}/status`, update);
    return response.data;
  },
};