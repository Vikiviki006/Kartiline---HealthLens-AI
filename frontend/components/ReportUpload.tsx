import React, { useState } from "react";
import { Upload as UploadIcon, Loader } from "lucide-react";
import { useReports } from "@/lib/hooks/useReports";

export const ReportUpload: React.FC<{ onUploadSuccess?: () => void }> = ({ onUploadSuccess }) => {
  const [dragActive, setDragActive] = useState(false);
  const { uploadReport, loading, error } = useReports();

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = async (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const files = e.dataTransfer.files;
    if (files && files[0]) {
      await handleFile(files[0]);
    }
  };

  const handleFile = async (file: File) => {
    // Validate file type
    const validTypes = ["application/pdf", "image/jpeg", "image/png", "image/tiff"];
    if (!validTypes.includes(file.type)) {
      alert("Please upload a PDF or image file (JPEG, PNG, TIFF)");
      return;
    }

    // Validate file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
      alert("File size must be less than 10MB");
      return;
    }

    try {
      await uploadReport(file);
      alert("Report uploaded successfully!");
      onUploadSuccess?.();
    } catch (err) {
      alert("Upload failed. Please try again.");
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  return (
    <div
      className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
        dragActive ? "border-blue-500 bg-blue-50" : "border-gray-300 bg-gray-50"
      }`}
      onDragEnter={handleDrag}
      onDragLeave={handleDrag}
      onDragOver={handleDrag}
      onDrop={handleDrop}
    >
      <UploadIcon className="w-12 h-12 mx-auto mb-4 text-gray-400" />
      <h3 className="text-lg font-semibold text-gray-900 mb-2">Upload Medical Report</h3>
      <p className="text-gray-600 mb-4">Drag and drop your file here or click to browse</p>

      <input
        type="file"
        accept=".pdf,.jpg,.jpeg,.png,.tiff"
        onChange={handleChange}
        className="hidden"
        id="file-upload"
        disabled={loading}
      />

      <label
        htmlFor="file-upload"
        className={`px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center space-x-2 mx-auto cursor-pointer inline-flex ${loading ? 'opacity-50 pointer-events-none' : ''}`}
      >
        {loading ? <Loader className="w-5 h-5 animate-spin" /> : <UploadIcon className="w-5 h-5" />}
        <span>{loading ? "Uploading..." : "Select File"}</span>
      </label>

      {error && <p className="mt-4 text-red-600 text-sm">{error}</p>}

      <p className="text-xs text-gray-500 mt-4">
        Supported formats: PDF, JPEG, PNG, TIFF. Max 10MB.
      </p>
    </div>
  );
};
