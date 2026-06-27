import React from "react";
import Link from "next/link";
import { Report } from "@/lib/hooks/useReports";
import { format } from "date-fns";
import { ArrowRight, Loader, Trash2 } from "lucide-react";

interface ReportListProps {
  reports: Report[];
  loading: boolean;
  onDelete?: (id: string) => Promise<void>;
}

export const ReportList: React.FC<ReportListProps> = ({ reports, loading, onDelete }) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case "completed":
        return "bg-green-100 text-green-800";
      case "processing":
        return "bg-blue-100 text-blue-800";
      case "failed":
        return "bg-red-100 text-red-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  const getStatusIcon = (status: string) => {
    if (status === "processing") {
      return <Loader className="w-4 h-4 animate-spin" />;
    }
    return null;
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <Loader className="w-8 h-8 animate-spin text-blue-600" />
      </div>
    );
  }

  if (reports.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">No reports yet. Upload your first medical report to get started.</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {reports.map((report) => (
        <div
          key={report.id}
          className="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow"
        >
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <div className="flex items-center space-x-3">
                <h3 className="text-lg font-semibold text-gray-900">{report.original_filename}</h3>
                <span className={`inline-flex items-center space-x-1 px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(report.status)}`}>
                  {getStatusIcon(report.status)}
                  <span className="capitalize">{report.status}</span>
                </span>
              </div>
              <p className="text-sm text-gray-600 mt-1">
                {format(new Date(report.created_at), "MMM dd, yyyy")} • {(report.file_size_bytes / 1024).toFixed(2)} KB
              </p>
              {report.total_markers > 0 && (
                <p className="text-sm text-gray-600 mt-2">
                  {report.total_markers} markers detected • {report.abnormal_markers} abnormal
                </p>
              )}
            </div>

            <div className="flex items-center space-x-2">
              <Link href={`/report/${report.id}`}>
                <button className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg">
                  <ArrowRight className="w-5 h-5" />
                </button>
              </Link>
              {onDelete && (
                <button
                  onClick={() => onDelete(report.id)}
                  className="p-2 text-red-600 hover:bg-red-50 rounded-lg"
                >
                  <Trash2 className="w-5 h-5" />
                </button>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};
