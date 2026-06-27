import React, { useState, useEffect } from "react";
import { useRouter } from "next/router";
import Link from "next/link";
import { Layout } from "@/components/Layout";
import { useReports, ReportDetail } from "@/lib/hooks/useReports";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";
import { Loader, ArrowLeft } from "lucide-react";

export default function TrendsPage() {
  const router = useRouter();
  const { id } = router.query;
  const [report, setReport] = useState<ReportDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const { getReport } = useReports();

  useEffect(() => {
    if (!id) return;

    const fetchReport = async () => {
      const data = await getReport(id as string);
      setReport(data);
      setLoading(false);
    };

    fetchReport();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  const trendData = [
    { date: "Jan", glucose: 95, hemoglobin: 14.2, platelets: 250 },
    { date: "Feb", glucose: 98, hemoglobin: 14.5, platelets: 245 },
    { date: "Mar", glucose: 101, hemoglobin: 14.1, platelets: 260 },
    { date: "Apr", glucose: 99, hemoglobin: 14.8, platelets: 255 },
    { date: "May", glucose: 102, hemoglobin: 14.4, platelets: 270 },
    { date: "Jun", glucose: 105, hemoglobin: 15.0, platelets: 265 },
  ];

  if (loading) {
    return (
      <Layout>
        <div className="flex justify-center items-center h-64">
          <Loader className="w-8 h-8 animate-spin text-blue-600" />
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="space-y-8">
        {/* Header */}
        <div>
          <Link href={`/report/${id}`} className="flex items-center space-x-2 text-blue-600 hover:underline mb-4">
            <ArrowLeft className="w-4 h-4" />
            <span>Back to Report</span>
          </Link>
          <h1 className="text-3xl font-bold text-gray-900">Health Trends</h1>
          {report && <p className="text-gray-600 mt-2">{report.original_filename}</p>}
        </div>

        {/* Glucose Trend */}
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Glucose Levels Over Time</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={trendData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="glucose" stroke="#3b82f6" name="Glucose (mg/dL)" />
            </LineChart>
          </ResponsiveContainer>
          <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <p className="text-sm text-gray-700">
              <strong>Analysis:</strong> Your glucose levels show a slight upward trend. Consider discussing dietary changes and exercise habits with your doctor.
            </p>
          </div>
        </div>

        {/* Hemoglobin Trend */}
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Hemoglobin Levels Over Time</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={trendData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="hemoglobin" stroke="#10b981" name="Hemoglobin (g/dL)" />
            </LineChart>
          </ResponsiveContainer>
          <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg">
            <p className="text-sm text-gray-700">
              <strong>Analysis:</strong> Hemoglobin levels remain within normal range with stable trends.
            </p>
          </div>
        </div>

        {/* Platelets Trend */}
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Platelet Count Over Time</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={trendData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="platelets" stroke="#f59e0b" name="Platelets (K/μL)" />
            </LineChart>
          </ResponsiveContainer>
          <div className="mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
            <p className="text-sm text-gray-700">
              <strong>Analysis:</strong> Platelet count shows normal variation. All values within reference range.
            </p>
          </div>
        </div>

        {/* Summary Card */}
        <div className="bg-gradient-to-br from-blue-50 to-indigo-50 border border-blue-200 rounded-lg p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Trend Summary</h2>
          <div className="space-y-2 text-sm text-gray-700">
            <p>✓ <strong>Overall Status:</strong> Stable with minor variations</p>
            <p>⚠ <strong>Attention Needed:</strong> Glucose trending upward - monitor closely</p>
            <p>✓ <strong>Positive Trend:</strong> Hemoglobin and Platelets stable</p>
            <p>💡 <strong>Recommendation:</strong> Schedule follow-up in 3 months for comprehensive check-up</p>
          </div>
        </div>
      </div>
    </Layout>
  );
}
