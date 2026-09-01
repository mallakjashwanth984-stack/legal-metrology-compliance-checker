'use client';

import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import toast from 'react-hot-toast';

const ProductUploadForm = ({ onUpload }: any) => {
  const [formData, setFormData] = useState({
    product_name: '',
    category: '',
  });
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);

  const { getRootProps, getInputProps } = useDropzone({
    onDrop: (acceptedFiles) => {
      if (acceptedFiles.length > 0) {
        setFile(acceptedFiles[0]);
      }
    },
    accept: { 'image/*': ['.png', '.jpg', '.jpeg', '.gif', '.bmp'] },
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      toast.error('Please select an image');
      return;
    }

    setUploading(true);
    const uploadFormData = new FormData();
    uploadFormData.append('image', file);
    uploadFormData.append('product_name', formData.product_name);
    uploadFormData.append('category', formData.category);

    try {
      await onUpload(uploadFormData);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <form onSubmit={handleSubmit}>
        <div className="mb-6">
          <label className="block text-gray-700 font-medium mb-2">Product Name</label>
          <input
            type="text"
            name="product_name"
            value={formData.product_name}
            onChange={handleChange}
            className="input"
            placeholder="e.g., Milk Pack 1L"
            required
          />
        </div>

        <div className="mb-6">
          <label className="block text-gray-700 font-medium mb-2">Category</label>
          <input
            type="text"
            name="category"
            value={formData.category}
            onChange={handleChange}
            className="input"
            placeholder="e.g., Dairy, Food, Beverages"
            required
          />
        </div>

        <div className="mb-6">
          <label className="block text-gray-700 font-medium mb-2">Product Image</label>
          <div
            {...getRootProps()}
            className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center cursor-pointer hover:border-blue-500 transition"
          >
            <input {...getInputProps()} />
            {file ? (
              <p className="text-green-600 font-medium">{file.name}</p>
            ) : (
              <>
                <p className="text-gray-600 mb-2">Drag and drop your image here, or click to select</p>
                <p className="text-sm text-gray-500">Supported formats: PNG, JPG, JPEG, GIF, BMP</p>
              </>
            )}
          </div>
        </div>

        <button
          type="submit"
          disabled={uploading}
          className="w-full bg-blue-600 text-white py-2 rounded-lg font-medium hover:bg-blue-700 transition disabled:opacity-50"
        >
          {uploading ? 'Uploading...' : 'Upload Product'}
        </button>
      </form>
    </div>
  );
};

export default ProductUploadForm;
