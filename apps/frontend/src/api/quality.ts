import { apiClient } from '../lib/axios';

export interface RoadQualityResponse {
  road_name?: string | null;
  district?: string | null;
  road_type?: string | null;
  contractor_name?: string | null;
  last_maintenance_date?: string | null;
  open_complaints: number;
  average_severity: number;
  quality_label: string;
  recent_complaints: Array<{
    ticket_number: string;
    defect_type: string;
    severity_score: number;
    status: string;
    created_at?: string | null;
  }>;
  error?: string | null;
}

export const qualityApi = {
  getByCoordinates: async (lat: number, lng: number): Promise<RoadQualityResponse> => {
    const response = await apiClient.get<RoadQualityResponse>('/api/road-quality', {
      params: { lat, lng },
    });
    return response.data;
  },
};