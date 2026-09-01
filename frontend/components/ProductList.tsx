'use client';

import React from 'react';

const ProductList = ({ products }: any) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {products.map((product) => (
        <div key={product.id} className="card hover:shadow-lg transition">
          {product.image_path && (
            <img
              src={product.image_path}
              alt={product.product_name}
              className="w-full h-40 object-cover rounded-lg mb-4"
            />
          )}
          <h3 className="text-lg font-bold text-gray-900 mb-2">{product.product_name}</h3>
          <p className="text-gray-600 text-sm mb-2">{product.product_category}</p>
          <p className="text-gray-600 text-sm mb-2">Manufacturer: {product.manufacturer_name || 'N/A'}</p>
          <p className="text-gray-600 text-sm mb-4">MRP: ₹{product.mrp || 'N/A'}</p>
          <a
            href={`/products/${product.id}`}
            className="btn-primary inline-block"
          >
            View Details
          </a>
        </div>
      ))}
    </div>
  );
};

export default ProductList;
