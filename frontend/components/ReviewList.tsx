'use client';

import React, { useEffect, useState } from 'react';
import { reviewService } from '@/services/reviewService';
import toast from 'react-hot-toast';

interface Review {
  id: number;
  reviewer_name: string;
  rating: number;
  title: string;
  review_text: string;
  compliance_feedback: string;
  department: string;
  helpful_count: number;
  unhelpful_count: number;
  created_at: string;
}

interface ReviewListProps {
  productId: number;
}

const ReviewList: React.FC<ReviewListProps> = ({ productId }) => {
  const [reviews, setReviews] = useState<Review[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [averageRating, setAverageRating] = useState(0);

  useEffect(() => {
    loadReviews();
  }, [productId, page]);

  const loadReviews = async () => {
    try {
      setLoading(true);
      const result = await reviewService.getProductReviews(productId, page, 5);
      setReviews(result.reviews);
      setTotalPages(result.pages);
      setAverageRating(result.average_rating);
    } catch (error) {
      toast.error('Failed to load reviews');
    } finally {
      setLoading(false);
    }
  };

  const handleMarkHelpful = async (reviewId: number) => {
    try {
      await reviewService.markHelpful(reviewId);
      loadReviews();
      toast.success('Marked as helpful');
    } catch (error) {
      toast.error('Failed to mark as helpful');
    }
  };

  const handleMarkUnhelpful = async (reviewId: number) => {
    try {
      await reviewService.markUnhelpful(reviewId);
      loadReviews();
      toast.success('Marked as unhelpful');
    } catch (error) {
      toast.error('Failed to mark as unhelpful');
    }
  };

  const renderStars = (rating: number) => {
    return (
      <div className="flex gap-1">
        {[1, 2, 3, 4, 5].map((star) => (
          <span key={star} className={star <= rating ? 'text-yellow-400 text-lg' : 'text-gray-300 text-lg'}>
            ★
          </span>
        ))}
      </div>
    );
  };

  const getComplianceBadgeColor = (feedback: string) => {
    switch (feedback) {
      case 'compliant':
        return 'bg-green-100 text-green-800';
      case 'non_compliant':
        return 'bg-red-100 text-red-800';
      case 'needs_improvement':
        return 'bg-yellow-100 text-yellow-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) return <div className="text-center py-8">Loading reviews...</div>;

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="mb-6">
        <h2 className="text-2xl font-bold mb-2">Customer Reviews</h2>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            {renderStars(Math.round(averageRating))}
            <span className="text-lg font-semibold text-gray-700">{averageRating.toFixed(1)}</span>
          </div>
          <span className="text-gray-600">Based on {reviews.length} reviews</span>
        </div>
      </div>

      <div className="space-y-4">
        {reviews.length === 0 ? (
          <p className="text-gray-500 text-center py-8">No reviews yet. Be the first to review!</p>
        ) : (
          reviews.map((review) => (
            <div key={review.id} className="border-b pb-4 last:border-b-0">
              <div className="flex justify-between items-start mb-2">
                <div>
                  <h3 className="font-semibold text-gray-900">{review.title}</h3>
                  <p className="text-sm text-gray-600">
                    {review.reviewer_name} • {review.department}
                  </p>
                </div>
                <span className={`badge ${getComplianceBadgeColor(review.compliance_feedback)}`}>
                  {review.compliance_feedback.replace('_', ' ').toUpperCase()}
                </span>
              </div>

              <div className="mb-2">{renderStars(review.rating)}</div>

              <p className="text-gray-700 mb-3">{review.review_text}</p>

              <div className="flex gap-4 text-sm">
                <button
                  onClick={() => handleMarkHelpful(review.id)}
                  className="text-blue-600 hover:text-blue-800 flex items-center gap-1"
                >
                  👍 Helpful ({review.helpful_count})
                </button>
                <button
                  onClick={() => handleMarkUnhelpful(review.id)}
                  className="text-gray-600 hover:text-gray-800 flex items-center gap-1"
                >
                  👎 Unhelpful ({review.unhelpful_count})
                </button>
              </div>

              <p className="text-xs text-gray-500 mt-2">
                {new Date(review.created_at).toLocaleDateString()}
              </p>
            </div>
          ))
        )}
      </div>

      {totalPages > 1 && (
        <div className="mt-6 flex justify-center gap-2">
          <button
            onClick={() => setPage(Math.max(1, page - 1))}
            disabled={page === 1}
            className="btn-primary disabled:opacity-50"
          >
            Previous
          </button>
          <span className="px-4 py-2 text-gray-600">
            Page {page} of {totalPages}
          </span>
          <button
            onClick={() => setPage(Math.min(totalPages, page + 1))}
            disabled={page === totalPages}
            className="btn-primary disabled:opacity-50"
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
};

export default ReviewList;
