'use client';

import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import toast from 'react-hot-toast';
import { productService } from '@/services/productService';

interface ProductImage {
  type: 'front' | 'back' | 'side' | 'top' | 'bottom';
  file: File | null;
  preview: string | null;
}

interface MultiAngleUploadFormProps {
  productId: number;
  onUploadSuccess?: (result: any) => void;
}

const MultiAngleUploadForm: React.FC<MultiAngleUploadFormProps> = ({ productId, onUploadSuccess }) => {
  const [images, setImages] = useState<Record<string, ProductImage>>({
    front: { type: 'front', file: null, preview: null },
    back: { type: 'back', file: null, preview: null },
    side: { type: 'side', file: null, preview: null },
    top: { type: 'top', file: null, preview: null },
    bottom: { type: 'bottom', file: null, preview: null },
  });
  const [uploading, setUploading] = useState(false);

  const handleImageDrop = (imageType: keyof typeof images, acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      const file = acceptedFiles[0];
      const preview = URL.createObjectURL(file);
      setImages({
        ...images,
        [imageType]: {
          type: imageType as any,
          file,
          preview,
        },
      });
    }
  };

  const DropZoneArea = ({ type }: { type: keyof typeof images }) => {
    const { getRootProps, getInputProps } = useDropzone({
      onDrop: (files) => handleImageDrop(type, files),
      accept: { 'image/*': ['.png', '.jpg', '.jpeg', '.gif', '.bmp'] },
      multiple: false,
    });

    const image = images[type];

    return (
      <div className="bg-white rounded-lg shadow-md p-6 h-full">
        <h3 className="text-lg font-bold mb-4 capitalize text-gray-800">{type} View</h3>
        <div
          {...getRootProps()}
          className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center cursor-pointer hover:border-blue-500 transition h-48 flex flex-col items-center justify-center"
        >
          <input {...getInputProps()} />
          {image.preview ? (
            <div className="w-full h-full flex flex-col items-center justify-center">
              <img
                src={image.preview}
                alt={`${type} view`}
                className="max-h-40 max-w-full object-contain mb-2"
              />
              <p className="text-sm text-green-600 font-medium">{image.file?.name}</p>
              <button
                type="button"
                onClick={(e) => {
                  e.stopPropagation();
                  setImages({
                    ...images,
                    [type]: { type: type as any, file: null, preview: null },
                  });
                }}
                className="mt-2 text-xs text-red-600 hover:text-red-800 underline"
              >
                Remove
              </button>
            </div>
          ) : (
            <>
              <p className="text-gray-600 mb-2">Click to upload {type} view</p>
              <p className="text-sm text-gray-500">PNG, JPG, JPEG, GIF, BMP</p>
            </>
          )}
        </div>
      </div>
    );
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Check if at least one image is selected
    const hasImages = Object.values(images).some((img) => img.file !== null);
    if (!hasImages) {
      toast.error('Please upload at least one image');
      return;
    }

    setUploading(true);
    const formData = new FormData();
    formData.append('product_id', productId.toString());

    // Add all selected images
    Object.values(images).forEach((img) => {
      if (img.file) {
        formData.append(img.type, img.file);
      }
    });

    try {
      const result = await productService.uploadProductImages(formData);
      toast.success('Images uploaded successfully!');
      setImages({
        front: { type: 'front', file: null, preview: null },
        back: { type: 'back', file: null, preview: null },
        side: { type: 'side', file: null, preview: null },
        top: { type: 'top', file: null, preview: null },
        bottom: { type: 'bottom', file: null, preview: null },
      });
      if (onUploadSuccess) {
        onUploadSuccess(result);
      }
    } catch (error: any) {
      toast.error(error.response?.data?.error || 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
        <DropZoneArea type="front" />
        <DropZoneArea type="back" />
        <DropZoneArea type="side" />
        <DropZoneArea type="top" />
        <DropZoneArea type="bottom" />
      </div>

      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <p className="text-sm text-blue-800">
          <strong>Note:</strong> Upload clear images of all sides of the product. Each image will be analyzed using OCR to extract text and validate compliance.
        </p>
      </div>

      <button
        type="submit"
        disabled={uploading}
        className="w-full bg-blue-600 text-white py-3 rounded-lg font-medium hover:bg-blue-700 transition disabled:opacity-50"
      >
        {uploading ? 'Uploading Images...' : 'Upload All Images'}
      </button>
    </form>
  );
};

export default MultiAngleUploadForm;
