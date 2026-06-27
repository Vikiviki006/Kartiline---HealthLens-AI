import React, { useEffect } from "react";
import { Layout } from "@/components/Layout";
import { ReportUpload } from "@/components/ReportUpload";
import { ReportList } from "@/components/ReportList";
import { useReports } from "@/lib/hooks/useReports";
import { BarChart3, TrendingUp, Clock, AlertCircle } from "lucide-react";

export default function Dashboard() {
  const { reports, loading, fetchReports, deleteReport } = useReports();

  useEffect(() => {
    fetchReports();
  }, []);

  const handleDelete = async (id: string) => {
    if (confirm("Are you sure you want to delete this report?")) {
      await deleteReport(id);
    }
  };

  const stats = {
    totalReports: reports.length,
    abnormalReports: reports.filter((r) => r.abnormal_markers > 0).length,
    processingReports: reports.filter((r) => r.status === "processing").length,
    completedReports: reports.filter((r) => r.status === "completed").length,
  };

  return (
    <Layout>
      <div className="space-y-8">
        {/* Header */}
        <div>
          <h1 className="text-4xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600 mt-2">Manage your medical reports and health insights</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {/* Total Reports */}
          <div className="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm font-medium">Total Reports</p>
                <p className="text-4xl font-bold text-gray-900 mt-2">{stats.totalReports}</p>
              </div>
              <BarChart3 className="w-12 h-12 text-blue-600 opacity-20" />
            </div>
          </div>

          {/* Abnormal Reports */}
          <div className="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm font-medium">Abnormal Markers</p>
                <p className="text-4xl font-bold text-yellow-600 mt-2">{stats.abnormalReports}</p>
              </div>
              <AlertCircle className="w-12 h-12 text-yellow-600 opacity-20" />
            </div>
          </div>

          {/* Processing */}
          <div className="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm font-medium">Processing</p>
                <p className="text-4xl font-bold text-blue-600 mt-2">{stats.processingReports}</p>
              </div>
              <Clock className="w-12 h-12 text-blue-600 opacity-20" />
            </div>
          </div>

          {/* Completed */}
          <div className="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm font-medium">Completed</p>
                <p className="text-4xl font-bold text-green-600 mt-2">{stats.completedReports}</p>
              </div>
              <TrendingUp className="w-12 h-12 text-green-600 opacity-20" />
            </div>
          </div>
        </div>

        {/* Two Column Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Upload Section */}
          <div className="lg:col-span-1 bg-white border border-gray-200 rounded-lg p-6">
            <h2 className="text-lg font-bold text-gray-900 mb-6">Upload New Report</h2>
            <ReportUpload onUploadSuccess={() => fetchReports()} />
          </div>

          {/* Tips */}
          <div className="lg:col-span-1 bg-gradient-to-br from-blue-50 to-indigo-50 border border-blue-200 rounded-lg p-6">
            <h2 className="text-lg font-bold text-blue-900 mb-4">💡 Tips</h2>
            <ul className="space-y-3 text-sm text-blue-800">
              <li>✓ Upload clear, legible reports for best OCR results</li>
              <li>✓ Use "Analyze" to get AI insights on your markers</li>
              <li>✓ Check trends to track your health over time</li>
              <li>✓ Prepare doctor visit summaries for consultations</li>
              <li>✓ Chat with AI to ask questions about results</li>
            </ul>
          </div>

          {/* Quick Links */}
          <div className="lg:col-span-1 bg-gradient-to-br from-green-50 to-emerald-50 border border-green-200 rounded-lg p-6">
            <h2 className="text-lg font-bold text-green-900 mb-4">📚 Resources</h2>
            <ul className="space-y-3 text-sm text-green-800">
              <li><a href="#" className="hover:text-green-900 font-medium">How to Upload Reports →</a></li>
              <li><a href="#" className="hover:text-green-900 font-medium">Understanding Lab Values →</a></li>
              <li><a href="#" className="hover:text-green-900 font-medium">Health Tips Guide →</a></li>
              <li><a href="#" className="hover:text-green-900 font-medium">FAQ →</a></li>
              <li><a href="/profile" className="hover:text-green-900 font-medium">My Account →</a></li>
            </ul>
          </div>
        </div>

        {/* Reports List */}
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-gray-900">Your Reports</h2>
            {reports.length > 0 && (
              <span className="text-sm text-gray-600">{reports.length} report{reports.length !== 1 ? "s" : ""}</span>
            )}
          </div>
          <ReportList reports={reports} loading={loading} onDelete={handleDelete} />
        </div>

        {/* Health Tips */}
        <div className="bg-gradient-to-r from-purple-50 to-pink-50 border border-purple-200 rounded-lg p-8">
          <h2 className="text-2xl font-bold text-purple-900 mb-4">🏥 Health Reminder</h2>
          <p className="text-purple-800">
            HealthLens AI is for <strong>educational purposes only</strong>. Always consult with qualified healthcare professionals before making any medical decisions. 
            This platform does not provide medical diagnoses or treatment recommendations.
          </p>
        </div>
      </div>
    </Layout>
  );
}
