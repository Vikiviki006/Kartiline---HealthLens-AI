import React from "react";
import { useRouter } from "next/router";
import Link from "next/link";
import { Layout } from "@/components/Layout";
import { ReportUpload } from "@/components/ReportUpload";
import { ArrowLeft, FileText } from "lucide-react";

export default function UploadPage() {
  const router = useRouter();

  const handleUploadSuccess = () => {
    setTimeout(() => {
      router.push("/dashboard");
    }, 1500);
  };

  return (
    <Layout>
      <div className="max-w-2xl mx-auto space-y-8">
        {/* Header */}
        <div className="flex items-center space-x-4">
          <Link href="/dashboard">
            <button className="p-2 hover:bg-gray-100 rounded-lg">
              <ArrowLeft className="w-6 h-6 text-gray-600" />
            </button>
          </Link>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Upload Medical Report</h1>
            <p className="text-gray-600 mt-1">Submit your lab report or medical document for AI analysis</p>
          </div>
        </div>

        {/* Upload Card */}
        <div className="bg-white border border-gray-200 rounded-lg p-8">
          <ReportUpload onUploadSuccess={handleUploadSuccess} />
        </div>

        {/* Guidelines */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
            <h3 className="font-semibold text-blue-900 mb-4 flex items-center space-x-2">
              <FileText className="w-5 h-5" />
              <span>Supported Formats</span>
            </h3>
            <ul className="space-y-2 text-sm text-blue-800">
              <li>✓ PDF documents</li>
              <li>✓ JPEG images</li>
              <li>✓ PNG images</li>
              <li>✓ TIFF images</li>
            </ul>
          </div>

          <div className="bg-green-50 border border-green-200 rounded-lg p-6">
            <h3 className="font-semibold text-green-900 mb-4">File Requirements</h3>
            <ul className="space-y-2 text-sm text-green-800">
              <li>✓ Maximum file size: 10 MB</li>
              <li>✓ Clear, legible text</li>
              <li>✓ No corrupted files</li>
              <li>✓ Single or multi-page</li>
            </ul>
          </div>
        </div>

        {/* Privacy Notice */}
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
          <h3 className="font-semibold text-yellow-900 mb-2">Privacy & Security</h3>
          <p className="text-sm text-yellow-800">
            Your medical reports are encrypted and stored securely. We never share your personal health information with third parties.
            Always review AI-generated insights with a qualified healthcare professional.
          </p>
        </div>
      </div>
    </Layout>
  );
}
