import api from './api';

interface Product {
  id: number;
  product_name: string;
  product_category: string;
  manufacturer_name?: string;
  barcode?: string;
  batch_number?: string;
  net_quantity?: string;
  unit_of_measurement?: string;
  mrp?: number;
  manufacturing_date?: string;
  expiry_date?: string;
  image_path?: string;
  created_at: string;
}

interface ProductResponse {
  message: string;
  product: Product;
  extracted_data: any;
}

export const productService = {
  getProducts: async (page = 1, perPage = 10, search = '', category = '') => {
    return (await api.get('/products/', {
      params: { page, per_page: perPage, search, category },
    })).data;
  },

  getProduct: async (id: number): Promise<Product> => {
    return (await api.get(`/products/${id}`)).data;
  },

  uploadProduct: async (formData: FormData): Promise<ProductResponse> => {
    return (await api.post('/products/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })).data;
  },

  deleteProduct: async (id: number) => {
    return (await api.delete(`/products/${id}`)).data;
  },
};
