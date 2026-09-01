import api from './api';

interface ReviewData {
  rating: number;
  title: string;
  review_text: string;
  compliance_feedback: string;
  issues_found?: string[];
  recommendations?: string;
}

export const reviewService = {
  createReview: async (productId: number, data: ReviewData) => {
    return (await api.post(`/reviews/${productId}`, data)).data;
  },

  getProductReviews: async (productId: number, page = 1, perPage = 10) => {
    return (await api.get(`/reviews/${productId}`, {
      params: { page, per_page: perPage, status: 'approved' },
    })).data;
  },

  getReview: async (reviewId: number) => {
    return (await api.get(`/reviews/${reviewId}`)).data;
  },

  updateReview: async (reviewId: number, data: Partial<ReviewData>) => {
    return (await api.put(`/reviews/${reviewId}`, data)).data;
  },

  deleteReview: async (reviewId: number) => {
    return (await api.delete(`/reviews/${reviewId}`)).data;
  },

  approveReview: async (reviewId: number) => {
    return (await api.put(`/reviews/${reviewId}/approve`, {})).data;
  },

  rejectReview: async (reviewId: number) => {
    return (await api.put(`/reviews/${reviewId}/reject`, {})).data;
  },

  markHelpful: async (reviewId: number) => {
    return (await api.put(`/reviews/${reviewId}/helpful`, {})).data;
  },

  markUnhelpful: async (reviewId: number) => {
    return (await api.put(`/reviews/${reviewId}/unhelpful`, {})).data;
  },

  getUserReviews: async (userId: number, page = 1, perPage = 10) => {
    return (await api.get(`/reviews/user/${userId}`, {
      params: { page, per_page: perPage },
    })).data;
  },

  getComplianceSummary: async (productId: number) => {
    return (await api.get(`/reviews/compliance-summary/${productId}`)).data;
  },
};
