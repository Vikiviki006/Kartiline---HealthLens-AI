import React from "react";
import { Marker } from "@/lib/hooks/useReports";
import { AlertCircle, CheckCircle, AlertTriangle } from "lucide-react";

interface MarkerCardProps {
  marker: Marker;
}

export const MarkerCard: React.FC<MarkerCardProps> = ({ marker }) => {
  const getSeverityStyles = (severity: string) => {
    switch (severity) {
      case "critical":
        return "bg-red-50 border-red-200";
      case "abnormal":
        return "bg-yellow-50 border-yellow-200";
      default:
        return "bg-green-50 border-green-200";
    }
  };

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case "critical":
        return <AlertCircle className="w-5 h-5 text-red-600" />;
      case "abnormal":
        return <AlertTriangle className="w-5 h-5 text-yellow-600" />;
      default:
        return <CheckCircle className="w-5 h-5 text-green-600" />;
    }
  };

  return (
    <div className={`border rounded-lg p-4 ${getSeverityStyles(marker.severity)}`}>
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center space-x-2">
            {getSeverityIcon(marker.severity)}
            <h3 className="text-lg font-semibold text-gray-900">{marker.marker_name}</h3>
          </div>
          <p className="text-sm text-gray-600 mt-1 capitalize">{marker.category || "General"}</p>
        </div>
        <span className={`px-3 py-1 rounded-full text-xs font-medium capitalize ${
          marker.severity === "critical" ? "bg-red-100 text-red-800" :
          marker.severity === "abnormal" ? "bg-yellow-100 text-yellow-800" :
          "bg-green-100 text-green-800"
        }`}>
          {marker.severity}
        </span>
      </div>

      <div className="mt-4 grid grid-cols-2 gap-4">
        <div>
          <p className="text-xs text-gray-600">Value</p>
          <p className="text-lg font-semibold text-gray-900">
            {marker.value} {marker.unit}
          </p>
        </div>
        <div>
          <p className="text-xs text-gray-600">Reference Range</p>
          <p className="text-sm text-gray-700">{marker.reference_range}</p>
        </div>
      </div>
    </div>
  );
};
