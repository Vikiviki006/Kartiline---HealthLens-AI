import React, { useEffect, useState } from "react";
import { useRouter } from "next/router";
import Link from "next/link";
import { Layout } from "@/components/Layout";
import { MarkerCard } from "@/components/MarkerCard";
import { QuickActions } from "@/components/QuickActions";
import { useReports, ReportDetail } from "@/lib/hooks/useReports";
import { ArrowLeft, Loader, Zap } from "lucide-react";

export default function ReportPage() {
  const router = useRouter();
  const { id } = router.query;
  const [report, setReport] = useState<ReportDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const { getReport, analyzeReport } = useReports();
  const [analyzing, setAnalyzing] = useState(false);

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

  const handleAnalyze = async () => {
    if (!report) return;
    setAnalyzing(true);
    try {
      await analyzeReport(report.id);
      // Refresh report data
      const updated = await getReport(report.id);
      setReport(updated);
    } finally {
      setAnalyzing(false);
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

  if (!report) {
    return (
      <Layout>
        <div className="text-center py-12">
          <p className="text-red-600">Report not found</p>
        </div>
      </Layout>
    );
  }

  const normalMarkers = report.markers?.filter((m) => m.severity === "normal") || [];
  const abnormalMarkers = report.markers?.filter((m) => m.severity !== "normal") || [];

  return (
    <Layout>
      <div className="space-y-8">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <Link href="/dashboard">
              <button className="p-2 hover:bg-gray-100 rounded-lg">
                <ArrowLeft className="w-6 h-6 text-gray-600" />
              </button>
            </Link>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">{report.original_filename}</h1>
              <p className="text-gray-600 mt-1">
                Uploaded {new Date(report.created_at).toLocaleDateString()}
              </p>
            </div>
          </div>
          <div className="text-right">
            <span className={`inline-block px-4 py-2 rounded-lg font-medium capitalize ${
              report.status === "completed" ? "bg-green-100 text-green-800" :
              report.status === "processing" ? "bg-blue-100 text-blue-800" :
              "bg-gray-100 text-gray-800"
            }`}>
              {report.status}
            </span>
          </div>
        </div>

        {/* Quick Actions */}
        {report.id && <QuickActions reportId={report.id} />}

        {/* File Info */}
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Report Information</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div>
              <p className="text-sm text-gray-600">File Size</p>
              <p className="text-lg font-semibold text-gray-900">
                {(report.file_size_bytes / 1024).toFixed(2)} KB
              </p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Format</p>
              <p className="text-lg font-semibold text-gray-900">{report.mime_type.split("/")[1].toUpperCase()}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">OCR Engine</p>
              <p className="text-lg font-semibold text-gray-900">{report.ocr_engine_used || "—"}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Total Markers</p>
              <p className="text-lg font-semibold text-gray-900">{report.markers?.length || 0}</p>
            </div>
          </div>
        </div>

        {/* AI Summary */}
        {report.ai_summary && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
            <div className="flex items-center space-x-2 mb-3">
              <Zap className="w-5 h-5 text-blue-600" />
              <h2 className="text-lg font-semibold text-blue-900">AI Health Summary</h2>
            </div>
            <p className="text-sm text-blue-800 leading-relaxed">{report.ai_summary}</p>
          </div>
        )}

        {/* Extracted Text Preview */}
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Extracted Text Preview</h2>
          <div className="bg-gray-50 border border-gray-200 rounded p-4 max-h-48 overflow-y-auto">
<p className="text-sm text-gray-700 whitespace-pre-wrap">
  {report.extracted_text
    ? `${report.extracted_text.substring(0, 500)}...`
    : "No extracted text available."}
</p>          </div>
        </div>

        {/* Analysis Section */}
        {report.markers && report.markers.length > 0 ? (
          <>
            {/* Normal Markers */}
            {normalMarkers.length > 0 && (
              <div className="bg-white border border-gray-200 rounded-lg p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">
                  Normal Markers ({normalMarkers.length})
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {normalMarkers.map((marker) => (
                    <MarkerCard key={marker.id} marker={marker} />
                  ))}
                </div>
              </div>
            )}

            {/* Abnormal Markers */}
            {abnormalMarkers.length > 0 && (
              <div className="bg-white border border-gray-200 rounded-lg p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">
                  ⚠️ Abnormal Markers ({abnormalMarkers.length})
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {abnormalMarkers.map((marker) => (
                    <MarkerCard key={marker.id} marker={marker} />
                  ))}
                </div>
              </div>
            )}
          </>
        ) : (
          <div className="bg-white border border-gray-200 rounded-lg p-6">
            <p className="text-gray-600 text-center py-8">
              No markers analyzed yet. Click the button below to run AI analysis.
            </p>
          </div>
        )}

        {/* Analyze Button */}
        {report.status !== "completed" && (
          <button
            onClick={handleAnalyze}
            disabled={analyzing}
            className="w-full py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 font-medium flex items-center justify-center space-x-2"
          >
            {analyzing ? (
              <>
                <Loader className="w-5 h-5 animate-spin" />
                <span>Analyzing Report...</span>
              </>
            ) : (
              <>
                <Zap className="w-5 h-5" />
                <span>Run AI Analysis</span>
              </>
            )}
          </button>
        )}
      </div>
    </Layout>
  );
}
