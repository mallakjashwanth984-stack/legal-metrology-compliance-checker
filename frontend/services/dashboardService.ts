import api from './api';

export const dashboardService = {
  getOverview: async () => {
    return (await api.get('/dashboard/overview')).data;
  },

  getRecentInspections: async (limit = 10) => {
    return (await api.get('/dashboard/recent-inspections', {
      params: { limit },
    })).data;
  },

  getViolationsByType: async () => {
    return (await api.get('/dashboard/violations-by-type')).data;
  },

  getComplianceTrends: async (days = 30) => {
    return (await api.get('/dashboard/compliance-trends', {
      params: { days },
    })).data;
  },

  getTopViolations: async (limit = 10) => {
    return (await api.get('/dashboard/top-violations', {
      params: { limit },
    })).data;
  },
};
