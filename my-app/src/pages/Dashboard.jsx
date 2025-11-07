import React, { useState, useEffect } from 'react';
import { Helmet } from 'react-helmet';
import { motion } from 'framer-motion';
import Layout from '@/components/Layout';
import MetricCard from '../dashboard/MetricCard';
import PerformanceChart from '../dashboard/PerformanceChart';
import InsightCard from '../dashboard/InsightCard';
import { TrendingUp, TrendingDown, DollarSign, MousePointer, Target, Zap } from 'lucide-react';

const Dashboard = () => {
  const [metrics, setMetrics] = useState(null);

  useEffect(() => {
    const storedMetrics = localStorage.getItem('dashflow_metrics');
    if (storedMetrics) {
      setMetrics(JSON.parse(storedMetrics));
    } else {
      const mockMetrics = {
        ctr: 3.45,
        ctrChange: 15.2,
        cpc: 2.87,
        cpcChange: -8.5,
        conversions: 127,
        conversionsChange: 22.3,
        totalCost: 4523.50,
        totalCostChange: 5.7,
        impressions: 45230,
        clicks: 1560,
      };
      setMetrics(mockMetrics);
      localStorage.setItem('dashflow_metrics', JSON.stringify(mockMetrics));
    }
  }, []);

  if (!metrics) return null;

  return (
    <>
      <Helmet>
        <title>Dashboard - DashFlow</title>
        <meta name="description" content="Visualize métricas e insights das suas campanhas de Google Ads" />
      </Helmet>
      <Layout>
        <div className="space-y-6">
          <div>
            <h1 className="text-3xl font-bold text-slate-900">Dashboard</h1>
            <p className="text-slate-600 mt-1">Visão geral do desempenho das suas campanhas</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <MetricCard
              title="CTR Médio"
              value={`${metrics.ctr}%`}
              change={metrics.ctrChange}
              icon={MousePointer}
              color="blue"
            />
            <MetricCard
              title="CPC Médio"
              value={`R$ ${metrics.cpc.toFixed(2)}`}
              change={metrics.cpcChange}
              icon={DollarSign}
              color="green"
            />
            <MetricCard
              title="Conversões"
              value={metrics.conversions}
              change={metrics.conversionsChange}
              icon={Target}
              color="purple"
            />
            <MetricCard
              title="Custo Total"
              value={`R$ ${metrics.totalCost.toFixed(2)}`}
              change={metrics.totalCostChange}
              icon={Zap}
              color="orange"
            />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2">
              <PerformanceChart />
            </div>
            <div>
              <InsightCard />
            </div>
          </div>
        </div>
      </Layout>
    </>
  );
};

export default Dashboard;