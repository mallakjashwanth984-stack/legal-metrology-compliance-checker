'use client';

import React, { useEffect, useState } from 'react';
import { dashboardService } from '@/services/dashboardService';
import toast from 'react-hot-toast';

const RecentInspections = () => {
  const [inspections, setInspections] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadInspections = async () => {
      try {
        const result = await dashboardService.getRecentInspections(5);
        setInspections(result.recent_inspections);
      } catch (error) {
        toast.error('Failed to load recent inspections');
      } finally {
        setLoading(false);
      }
    };

    loadInspections();
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-xl font-bold mb-4">Recent Inspections</h2>
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b">
              <th className="text-left py-2">Product</th>
              <th className="text-left py-2">Date</th>
              <th className="text-left py-2">Status</th>
              <th className="text-left py-2">Compliance %</th>
            </tr>
          </thead>
          <tbody>
            {inspections.map((inspection, idx) => (
              <tr key={idx} className="border-b hover:bg-gray-50">
                <td className="py-3">{inspection.product_name}</td>
                <td className="py-3">{new Date(inspection.inspection_date).toLocaleDateString()}</td>
                <td className="py-3">
                  <span className={`badge ${inspection.compliance_status === 'compliant' ? 'badge-compliant' : 'badge-non-compliant'}`}>
                    {inspection.compliance_status}
                  </span>
                </td>
                <td className="py-3">{inspection.compliance_percentage.toFixed(1)}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default RecentInspections;
