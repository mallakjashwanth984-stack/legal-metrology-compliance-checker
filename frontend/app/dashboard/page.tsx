'use client';

import React, { useEffect, useState } from 'react';
import { dashboardService } from '@/services/dashboardService';
import DashboardCard from '@/components/DashboardCard';
import ComplianceChart from '@/components/ComplianceChart';
import RecentInspections from '@/components/RecentInspections';
import toast from 'react-hot-toast';

const DashboardPage = () => {
  const [overview, setOverview] = useState<any>(null);
  const [trends, setTrends] = useState<any>(null);
  const [topViolations, setTopViolations] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadDashboardData = async () => {
      try {
        const [overviewData, trendsData, violationsData] = await Promise.all([
          dashboardService.getOverview(),
          dashboardService.getComplianceTrends(30),
          dashboardService.getTopViolations(10),
        ]);
        setOverview(overviewData);
        setTrends(trendsData);
        setTopViolations(violationsData);
      } catch (error) {
        toast.error('Failed to load dashboard data');
      } finally {
        setLoading(false);
      }
    };

    loadDashboardData();
  }, []);

  if (loading) return <div className="text-center py-8">Loading...</div>;

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Dashboard</h1>

        {/* Overview Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <DashboardCard
            title="Total Products"
            value={overview?.total_products || 0}
            icon="📦"
          />
          <DashboardCard
            title="Compliant Products"
            value={overview?.compliant_products || 0}
            icon="✅"
          />
          <DashboardCard
            title="Non-Compliant"
            value={overview?.non_compliant_products || 0}
            icon="❌"
          />
          <DashboardCard
            title="Total Violations"
            value={overview?.total_violations || 0}
            icon="⚠️"
          />
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <ComplianceChart data={trends?.compliance_trends || []} />
        </div>

        {/* Recent Inspections */}
        <RecentInspections />
      </div>
    </div>
  );
};

export default DashboardPage;
