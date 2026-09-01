'use client';

import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { productService } from '@/services/productService';
import { complianceService } from '@/services/complianceService';
import toast from 'react-hot-toast';
import ProductUploadForm from '@/components/ProductUploadForm';

const UploadPage = () => {
  const [uploadedProduct, setUploadedProduct] = useState<any>(null);
  const [checking, setChecking] = useState(false);

  const handleUpload = async (formData: FormData) => {
    try {
      const result = await productService.uploadProduct(formData);
      setUploadedProduct(result.product);
      toast.success('Product uploaded successfully!');
      return result.product;
    } catch (error: any) {
      toast.error(error.response?.data?.error || 'Upload failed');
      throw error;
    }
  };

  const handleCheckCompliance = async () => {
    if (!uploadedProduct) {
      toast.error('Please upload a product first');
      return;
    }

    setChecking(true);
    try {
      const result = await complianceService.checkCompliance(uploadedProduct.id);
      toast.success('Compliance check completed!');
      return result;
    } catch (error: any) {
      toast.error(error.response?.data?.error || 'Compliance check failed');
    } finally {
      setChecking(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Upload Product</h1>

        <ProductUploadForm onUpload={handleUpload} />

        {uploadedProduct && (
          <div className="mt-8 bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-bold mb-4">Product Details</h2>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-gray-600 font-medium">Product Name</p>
                <p className="text-lg">{uploadedProduct.product_name}</p>
              </div>
              <div>
                <p className="text-gray-600 font-medium">Category</p>
                <p className="text-lg">{uploadedProduct.product_category}</p>
              </div>
              <div>
                <p className="text-gray-600 font-medium">Manufacturer</p>
                <p className="text-lg">{uploadedProduct.manufacturer_name || 'N/A'}</p>
              </div>
              <div>
                <p className="text-gray-600 font-medium">MRP</p>
                <p className="text-lg">₹{uploadedProduct.mrp || 'N/A'}</p>
              </div>
            </div>

            <button
              onClick={handleCheckCompliance}
              disabled={checking}
              className="mt-6 bg-blue-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-blue-700 transition disabled:opacity-50"
            >
              {checking ? 'Checking Compliance...' : 'Check Compliance'}
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default UploadPage;
