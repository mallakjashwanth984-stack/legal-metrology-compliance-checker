'use client';

import React, { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { productService } from '@/services/productService';
import MultiAngleUploadForm from '@/components/MultiAngleUploadForm';
import ProductImageGallery from '@/components/ProductImageGallery';
import CreateReviewForm from '@/components/CreateReviewForm';
import ReviewList from '@/components/ReviewList';
import toast from 'react-hot-toast';

const ProductDetailPage = () => {
  const params = useParams();
  const productId = parseInt(params.id as string);
  const [product, setProduct] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'images' | 'reviews'>('images');

  useEffect(() => {
    loadProduct();
  }, [productId]);

  const loadProduct = async () => {
    try {
      setLoading(true);
      const result = await productService.getProduct(productId);
      setProduct(result);
    } catch (error: any) {
      toast.error('Failed to load product');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="text-center py-8">Loading...</div>;
  if (!product) return <div className="text-center py-8">Product not found</div>;

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">{product.product_name}</h1>
        <p className="text-gray-600 mb-6">{product.product_category}</p>

        {/* Product Info Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-white rounded-lg shadow-md p-4">
            <p className="text-gray-600 text-sm">Manufacturer</p>
            <p className="text-lg font-semibold text-gray-900">{product.manufacturer_name || 'N/A'}</p>
          </div>
          <div className="bg-white rounded-lg shadow-md p-4">
            <p className="text-gray-600 text-sm">Net Quantity</p>
            <p className="text-lg font-semibold text-gray-900">
              {product.net_quantity} {product.unit_of_measurement}
            </p>
          </div>
          <div className="bg-white rounded-lg shadow-md p-4">
            <p className="text-gray-600 text-sm">MRP</p>
            <p className="text-lg font-semibold text-gray-900">₹{product.mrp || 'N/A'}</p>
          </div>
          <div className="bg-white rounded-lg shadow-md p-4">
            <p className="text-gray-600 text-sm">Barcode</p>
            <p className="text-lg font-semibold text-gray-900 truncate">{product.barcode || 'N/A'}</p>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex gap-4 mb-6">
          <button
            onClick={() => setActiveTab('images')}
            className={`px-6 py-2 rounded-lg font-medium transition ${
              activeTab === 'images'
                ? 'bg-blue-600 text-white'
                : 'bg-white text-gray-700 border border-gray-200 hover:border-gray-300'
            }`}
          >
            📷 Images & Compliance
          </button>
          <button
            onClick={() => setActiveTab('reviews')}
            className={`px-6 py-2 rounded-lg font-medium transition ${
              activeTab === 'reviews'
                ? 'bg-blue-600 text-white'
                : 'bg-white text-gray-700 border border-gray-200 hover:border-gray-300'
            }`}
          >
            ⭐ Reviews
          </button>
        </div>

        {/* Content */}
        {activeTab === 'images' && (
          <div className="space-y-8">
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-2xl font-bold mb-4">Upload Product Images</h2>
              <MultiAngleUploadForm productId={productId} onUploadSuccess={loadProduct} />
            </div>
            <ProductImageGallery productId={productId} />
          </div>
        )}

        {activeTab === 'reviews' && (
          <div className="space-y-8">
            <CreateReviewForm productId={productId} />
            <ReviewList productId={productId} />
          </div>
        )}
      </div>
    </div>
  );
};

export default ProductDetailPage;
