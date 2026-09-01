import api from './api';

interface Violation {
  id: number;
  product_id: number;
  violation_type: string;
  severity: 'critical' | 'major' | 'minor';
  description: string;
  rule_reference?: string;
  is_resolved: boolean;
  created_at: string;
}

interface ComplianceResponse {
  product_id: number;
  compliance_status: 'compliant' | 'non_compliant';
  compliance_percentage: number;
  total_violations: number;
  critical_violations: number;
  major_violations: number;
  minor_violations: number;
  violations: Violation[];
}

export const complianceService = {
  checkCompliance: async (productId: number): Promise<ComplianceResponse> => {
    return (await api.post(`/compliance/check/${productId}`)).data;
  },

  getViolations: async (productId: number, severity?: string) => {
    return (await api.get(`/compliance/violations/${productId}`, {
      params: { severity },
    })).data;
  },

  resolveViolation: async (violationId: number, resolutionNotes: string) => {
    return (await api.put(`/compliance/violations/${violationId}/resolve`, {
      resolution_notes: resolutionNotes,
    })).data;
  },
};
