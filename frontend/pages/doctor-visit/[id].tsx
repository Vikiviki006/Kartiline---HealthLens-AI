import React, { useState, useEffect } from "react";
import { useRouter } from "next/router";
import Link from "next/link";
import { Layout } from "@/components/Layout";
import { useReports, ReportDetail } from "@/lib/hooks/useReports";
import { Loader, ArrowLeft, Download, FileText } from "lucide-react";
import api from "@/lib/api";

export default function DoctorVisitPage() {
  const router = useRouter();
  const { id } = router.query;
  const [report, setReport] = useState<ReportDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [downloading, setDownloading] = useState(false);
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

  const handleDownload = async () => {
    if (!id) return;
    setDownloading(true);
    try {
      const response = await api.get(`/reports/${id}/pdf`, {
        responseType: "blob",
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      
      // Clean name for filename
      const cleanName = report?.original_filename.replace(/\.[^/.]+$/, "") || "HealthLens";
      link.setAttribute("download", `${cleanName}_Summary.pdf`);
      document.body.appendChild(link);
      link.click();
      link.parentNode?.removeChild(link);
    } catch (error) {
      console.error("Error downloading PDF:", error);
      alert("Failed to download PDF summary. Please try again.");
    } finally {
      setDownloading(false);
    }
  };

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
          <h1 className="text-3xl font-bold text-gray-900">Doctor Visit Preparation</h1>
          {report && <p className="text-gray-600 mt-2">{report.original_filename}</p>}
        </div>

        {/* Download Summary */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <FileText className="w-8 h-8 text-blue-600" />
              <div>
                <h2 className="font-semibold text-gray-900">Health Summary Report</h2>
                <p className="text-sm text-gray-600">Generate a PDF to bring to your doctor</p>
              </div>
            </div>
            <button
              onClick={handleDownload}
              disabled={downloading}
              className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              {downloading ? (
                <>
                  <Loader className="w-5 h-5 animate-spin" />
                  <span>Downloading...</span>
                </>
              ) : (
                <>
                  <Download className="w-5 h-5" />
                  <span>Download PDF</span>
                </>
              )}
            </button>
          </div>
        </div>

        {/* Key Questions */}
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Questions to Ask Your Doctor</h2>
          <div className="space-y-4">
            <div className="border-l-4 border-blue-600 pl-4">
              <h3 className="font-semibold text-gray-900 mb-2">About Glucose Levels</h3>
              <ul className="space-y-2 text-sm text-gray-700">
                <li>• Why are my glucose levels trending upward?</li>
                <li>• Should I adjust my diet or exercise routine?</li>
                <li>• Do I need to be tested for prediabetes?</li>
                <li>• What's my individual target glucose range?</li>
              </ul>
            </div>

            <div className="border-l-4 border-green-600 pl-4">
              <h3 className="font-semibold text-gray-900 mb-2">About Blood Markers</h3>
              <ul className="space-y-2 text-sm text-gray-700">
                <li>• Are all my values within the normal range?</li>
                <li>• Should I take any supplements or medications?</li>
                <li>• How often should I get these tests repeated?</li>
                <li>• What lifestyle changes would help improve my results?</li>
              </ul>
            </div>

            <div className="border-l-4 border-yellow-600 pl-4">
              <h3 className="font-semibold text-gray-900 mb-2">About Prevention</h3>
              <ul className="space-y-2 text-sm text-gray-700">
                <li>• What health risks should I be aware of?</li>
                <li>• Are there any warning signs I should watch for?</li>
                <li>• What preventive measures should I take?</li>
                <li>• Do I need specialist referrals based on these results?</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Preparation Tips */}
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Preparation Tips</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-gray-50 p-4 rounded-lg">
              <h3 className="font-semibold text-gray-900 mb-3">✓ What to Bring</h3>
              <ul className="space-y-2 text-sm text-gray-700">
                <li>• Your printed health summary</li>
                <li>• This report with markers highlighted</li>
                <li>• List of current medications</li>
                <li>• Blood pressure readings from home</li>
                <li>• Medical history notes</li>
              </ul>
            </div>

            <div className="bg-gray-50 p-4 rounded-lg">
              <h3 className="font-semibold text-gray-900 mb-3">💡 Discussion Topics</h3>
              <ul className="space-y-2 text-sm text-gray-700">
                <li>• Concerns about upward glucose trend</li>
                <li>• Dietary and lifestyle recommendations</li>
                <li>• Follow-up testing timeline</li>
                <li>• When to schedule next appointment</li>
                <li>• Red flags to watch for</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Action Items */}
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Action Items Before Visit</h2>
          <div className="space-y-3">
            <label className="flex items-center space-x-3 p-3 hover:bg-gray-50 rounded-lg cursor-pointer">
              <input type="checkbox" className="w-5 h-5 text-blue-600 rounded" />
              <span className="text-gray-700">Print or save this health summary</span>
            </label>
            <label className="flex items-center space-x-3 p-3 hover:bg-gray-50 rounded-lg cursor-pointer">
              <input type="checkbox" className="w-5 h-5 text-blue-600 rounded" />
              <span className="text-gray-700">List any symptoms you've experienced</span>
            </label>
            <label className="flex items-center space-x-3 p-3 hover:bg-gray-50 rounded-lg cursor-pointer">
              <input type="checkbox" className="w-5 h-5 text-blue-600 rounded" />
              <span className="text-gray-700">Gather previous test results</span>
            </label>
            <label className="flex items-center space-x-3 p-3 hover:bg-gray-50 rounded-lg cursor-pointer">
              <input type="checkbox" className="w-5 h-5 text-blue-600 rounded" />
              <span className="text-gray-700">Record your medications and supplements</span>
            </label>
            <label className="flex items-center space-x-3 p-3 hover:bg-gray-50 rounded-lg cursor-pointer">
              <input type="checkbox" className="w-5 h-5 text-blue-600 rounded" />
              <span className="text-gray-700">Note any lifestyle changes recently</span>
            </label>
          </div>
        </div>

        {/* Important Note */}
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
          <h3 className="font-semibold text-yellow-900 mb-2">⚠️ Important Disclaimer</h3>
          <p className="text-sm text-yellow-800">
            This AI-generated summary is for informational purposes only and should not replace professional medical advice. 
            Always consult with a qualified healthcare provider regarding your health concerns and any medical decisions.
          </p>
        </div>
      </div>
    </Layout>
  );
}
