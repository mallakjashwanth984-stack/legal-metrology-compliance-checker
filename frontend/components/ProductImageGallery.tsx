'use client';

import React, { useEffect, useState } from 'react';
import { productService } from '@/services/productService';
import toast from 'react-hot-toast';

interface ProductImage {
  id: number;
  image_type: string;
  image_path: string;
  extracted_text: string;
  image_quality_score: number;
  uploaded_by_name: string;
  created_at: string;
}

interface ProductImageGalleryProps {
  productId: number;
}

const ProductImageGallery: React.FC<ProductImageGalleryProps> = ({ productId }) => {
  const [images, setImages] = useState<ProductImage[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedImage, setSelectedImage] = useState<ProductImage | null>(null);
  const imageTypes = ['front', 'back', 'side', 'top', 'bottom'];

  useEffect(() => {
    loadImages();
  }, [productId]);

  const loadImages = async () => {
    try {
      setLoading(true);
      const result = await productService.getProductImages(productId);
      setImages(result.images);
    } catch (error) {
      toast.error('Failed to load images');
    } finally {
      setLoading(false);
    }
  };

  const getImageByType = (type: string) => {
    return images.find((img) => img.image_type === type);
  };

  const getQualityColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  if (loading) return <div className="text-center py-8">Loading images...</div>;

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-bold mb-4">Product Images</h2>

      <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6">
        {imageTypes.map((type) => {
          const image = getImageByType(type);
          return (
            <div
              key={type}
              className="border-2 border-gray-200 rounded-lg p-4 text-center cursor-pointer hover:border-blue-500 transition"
              onClick={() => image && setSelectedImage(image)}
            >
              <div className="capitalize font-semibold text-gray-700 mb-2">{type}</div>
              {image ? (
                <>
                  <div className="bg-gray-100 rounded mb-2 h-20 flex items-center justify-center">
                    <img
                      src={image.image_path}
                      alt={type}
                      className="max-h-full max-w-full object-contain"
                    />
                  </div>
                  <div className={`text-sm font-medium ${getQualityColor(image.image_quality_score)}`}>
                    Quality: {image.image_quality_score.toFixed(1)}%
                  </div>
                </>
              ) : (
                <div className="bg-gray-100 rounded h-20 flex items-center justify-center text-gray-500 text-sm">
                  Not uploaded
                </div>
              )}
            </div>
          );
        })}
      </div>

      {selectedImage && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50" onClick={() => setSelectedImage(null)}>
          <div className="bg-white rounded-lg p-6 max-w-2xl w-full max-h-96 overflow-y-auto" onClick={(e) => e.stopPropagation()}>
            <div className="flex justify-between items-start mb-4">
              <div>
                <h3 className="text-xl font-bold capitalize">{selectedImage.image_type} View</h3>
                <p className="text-sm text-gray-600">
                  Uploaded by {selectedImage.uploaded_by_name} on {new Date(selectedImage.created_at).toLocaleDateString()}
                </p>
              </div>
              <button
                onClick={() => setSelectedImage(null)}
                className="text-gray-500 hover:text-gray-700 font-bold text-2xl"
              >
                ×
              </button>
            </div>

            <img
              src={selectedImage.image_path}
              alt={selectedImage.image_type}
              className="w-full h-64 object-contain mb-4 border rounded"
            />

            <div className="mb-4">
              <h4 className="font-semibold mb-2">Image Quality Score</h4>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-blue-600 h-2 rounded-full transition"
                  style={{ width: `${selectedImage.image_quality_score}%` }}
                />
              </div>
              <p className="text-sm text-gray-600 mt-1">{selectedImage.image_quality_score.toFixed(1)}%</p>
            </div>

            {selectedImage.extracted_text && (
              <div>
                <h4 className="font-semibold mb-2">Extracted Text</h4>
                <div className="bg-gray-50 p-3 rounded text-sm text-gray-700 max-h-32 overflow-y-auto">
                  {selectedImage.extracted_text}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default ProductImageGallery;
