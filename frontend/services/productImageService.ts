import api from './api';

interface MultiImageFormData {
  product_id: number;
  [key: string]: any;
}

export const productImageService = {
  uploadProductImages: async (formData: FormData) => {
    return (await api.post('/product-images/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })).data;
  },

  getProductImages: async (productId: number) => {
    return (await api.get(`/product-images/${productId}`)).data;
  },

  getProductImageByType: async (productId: number, imageType: string) => {
    return (await api.get(`/product-images/by-type/${productId}/${imageType}`)).data;
  },

  deleteProductImage: async (imageId: number) => {
    return (await api.delete(`/product-images/${imageId}`)).data;
  },
};
