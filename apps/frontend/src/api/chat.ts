import { apiClient } from '../lib/axios';
import { ChatRequest, ChatResponse } from '../types/api';

export const chatApi = {
  sendMessage: async (payload: ChatRequest): Promise<ChatResponse> => {
    const response = await apiClient.post<ChatResponse>('/api/chat', payload);
    return response.data;
  },
};