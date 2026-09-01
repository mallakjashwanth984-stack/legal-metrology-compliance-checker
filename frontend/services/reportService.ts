import api from './api';

interface ComplianceReport {
  id: number;
  product_id: number;
  report_title: string;
  total_violations: number;
  critical_violations: number;
  major_violations: number;
  minor_violations: number;
  compliance_status: 'compliant' | 'non_compliant';
  compliance_percentage: number;
  summary: string;
  created_at: string;
}

export const reportService = {
  generateReport: async (productId: number): Promise<ComplianceReport> => {
    return (await api.post(`/reports/${productId}`)).data.report;
  },

  getReports: async (page = 1, perPage = 10, productId?: number) => {
    return (await api.get('/reports/', {
      params: { page, per_page: perPage, product_id: productId },
    })).data;
  },

  getReport: async (id: number): Promise<ComplianceReport> => {
    return (await api.get(`/reports/${id}`)).data;
  },

  downloadReport: async (id: number) => {
    return api.get(`/reports/download/${id}`, {
      responseType: 'blob',
    });
  },
};
