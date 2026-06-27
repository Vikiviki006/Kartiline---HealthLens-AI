import { useState, useEffect } from "react";
import api from "@/lib/api";

export interface Report {
  id: string;
  original_filename: string;
  file_size_bytes: number;
  status: "pending" | "processing" | "completed" | "failed";
  report_type?: string;
  report_date?: string;
  created_at: string;
  total_markers: number;
  abnormal_markers: number;
}

export interface ReportDetail extends Report {
  stored_path: string;
  mime_type: string;
  ocr_engine_used?: string;
  extracted_text: string;
  markers: Marker[];
}

export interface Marker {
  id: string;
  marker_name: string;
  value: string;
  unit: string;
  reference_range: string;
  severity: "normal" | "abnormal" | "critical";
  numeric_value?: number;
  category?: string;
}

export const useReports = () => {
  const [reports, setReports] = useState<Report[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchReports = async (page = 1, pageSize = 10) => {
    try {
      setLoading(true);
      const response = await api.get("/reports", {
        params: { page, page_size: pageSize },
      });
      setReports(response.data.data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch reports");
    } finally {
      setLoading(false);
    }
  };

  const getReport = async (reportId: string): Promise<ReportDetail | null> => {
    try {
      const response = await api.get(`/reports/${reportId}`);
      return response.data.data;
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch report");
      return null;
    }
  };

  const uploadReport = async (file: File) => {
    try {
      setLoading(true);
      const formData = new FormData();
      formData.append("file", file);

      const response = await api.post("/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setError(null);
      return response.data.data;
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload failed");
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const analyzeReport = async (reportId: string, force = false) => {
    try {
      setLoading(true);
      const response = await api.post(`/reports/${reportId}/analyze`, null, {
        params: { force },
      });
      setError(null);
      return response.data.data;
    } catch (err) {
      setError(err instanceof Error ? err.message : "Analysis failed");
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const deleteReport = async (reportId: string) => {
    try {
      setLoading(true);
      await api.delete(`/reports/${reportId}`);
      setReports(reports.filter((r) => r.id !== reportId));
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Delete failed");
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    reports,
    loading,
    error,
    fetchReports,
    getReport,
    uploadReport,
    analyzeReport,
    deleteReport,
  };
};
