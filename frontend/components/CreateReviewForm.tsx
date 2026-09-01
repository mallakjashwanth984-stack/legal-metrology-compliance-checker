'use client';

import React, { useState } from 'react';
import { reviewService } from '@/services/reviewService';
import toast from 'react-hot-toast';

interface CreateReviewFormProps {
  productId: number;
  onReviewCreated?: () => void;
}

const CreateReviewForm: React.FC<CreateReviewFormProps> = ({ productId, onReviewCreated }) => {
  const [formData, setFormData] = useState({
    rating: 5,
    title: '',
    review_text: '',
    compliance_feedback: 'compliant',
    issues_found: [] as string[],
    recommendations: '',
  });
  const [submitting, setSubmitting] = useState(false);
  const [issueInput, setIssueInput] = useState('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleAddIssue = () => {
    if (issueInput.trim()) {
      setFormData({
        ...formData,
        issues_found: [...formData.issues_found, issueInput.trim()],
      });
      setIssueInput('');
    }
  };

  const handleRemoveIssue = (index: number) => {
    setFormData({
      ...formData,
      issues_found: formData.issues_found.filter((_, i) => i !== index),
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!formData.title.trim()) {
      toast.error('Please enter a review title');
      return;
    }

    if (!formData.review_text.trim()) {
      toast.error('Please enter a review');
      return;
    }

    setSubmitting(true);
    try {
      await reviewService.createReview(productId, {
        ...formData,
        issues_found: formData.issues_found.length > 0 ? formData.issues_found : null,
      });
      toast.success('Review submitted! It will be displayed after admin approval.');
      setFormData({
        rating: 5,
        title: '',
        review_text: '',
        compliance_feedback: 'compliant',
        issues_found: [],
        recommendations: '',
      });
      if (onReviewCreated) {
        onReviewCreated();
      }
    } catch (error: any) {
      toast.error(error.response?.data?.error || 'Failed to submit review');
    } finally {
      setSubmitting(false);
    }
  };

  const renderStarInput = () => {
    return (
      <div className="flex gap-2">
        {[1, 2, 3, 4, 5].map((star) => (
          <button
            key={star}
            type="button"
            onClick={() => setFormData({ ...formData, rating: star })}
            className={`text-3xl transition ${
              star <= formData.rating ? 'text-yellow-400' : 'text-gray-300 hover:text-yellow-200'
            }`}
          >
            ★
          </button>
        ))}
      </div>
    );
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 mb-8">
      <h2 className="text-2xl font-bold mb-6">Write a Review</h2>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label className="block text-gray-700 font-medium mb-2">Rating</label>
          {renderStarInput()}
        </div>

        <div>
          <label className="block text-gray-700 font-medium mb-2">Review Title</label>
          <input
            type="text"
            name="title"
            value={formData.title}
            onChange={handleChange}
            className="input"
            placeholder="What's most important to know?"
            required
          />
        </div>

        <div>
          <label className="block text-gray-700 font-medium mb-2">Review</label>
          <textarea
            name="review_text"
            value={formData.review_text}
            onChange={handleChange}
            rows={4}
            className="input"
            placeholder="Share your experience with this product..."
            required
          />
        </div>

        <div>
          <label className="block text-gray-700 font-medium mb-2">Compliance Feedback</label>
          <select
            name="compliance_feedback"
            value={formData.compliance_feedback}
            onChange={handleChange}
            className="input"
          >
            <option value="compliant">✓ Compliant</option>
            <option value="non_compliant">✗ Non-Compliant</option>
            <option value="needs_improvement">~ Needs Improvement</option>
          </select>
        </div>

        <div>
          <label className="block text-gray-700 font-medium mb-2">Issues Found (Optional)</label>
          <div className="flex gap-2 mb-2">
            <input
              type="text"
              value={issueInput}
              onChange={(e) => setIssueInput(e.target.value)}
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  e.preventDefault();
                  handleAddIssue();
                }
              }}
              className="input flex-1"
              placeholder="Enter an issue and press Enter"
            />
            <button
              type="button"
              onClick={handleAddIssue}
              className="btn-secondary px-4"
            >
              Add
            </button>
          </div>
          {formData.issues_found.length > 0 && (
            <div className="flex flex-wrap gap-2">
              {formData.issues_found.map((issue, index) => (
                <span
                  key={index}
                  className="badge bg-gray-200 text-gray-800 flex items-center gap-2"
                >
                  {issue}
                  <button
                    type="button"
                    onClick={() => handleRemoveIssue(index)}
                    className="text-red-600 hover:text-red-800 font-bold"
                  >
                    ×
                  </button>
                </span>
              ))}
            </div>
          )}
        </div>

        <div>
          <label className="block text-gray-700 font-medium mb-2">Recommendations (Optional)</label>
          <textarea
            name="recommendations"
            value={formData.recommendations}
            onChange={handleChange}
            rows={3}
            className="input"
            placeholder="What improvements would you suggest?"
          />
        </div>

        <button
          type="submit"
          disabled={submitting}
          className="w-full bg-blue-600 text-white py-2 rounded-lg font-medium hover:bg-blue-700 transition disabled:opacity-50"
        >
          {submitting ? 'Submitting...' : 'Submit Review'}
        </button>
      </form>

      <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <p className="text-sm text-blue-800">
          <strong>Note:</strong> Your review will be moderated by our administrators before being displayed.
        </p>
      </div>
    </div>
  );
};

export default CreateReviewForm;
