import React from "react";
import { AlertCircle, CheckCircle, Info } from "lucide-react";

interface ToastProps {
  message: string;
  type: "success" | "error" | "info";
  onClose: () => void;
}

export const Toast: React.FC<ToastProps> = ({ message, type, onClose }) => {
  const bgColor =
    type === "success" ? "bg-green-50" : type === "error" ? "bg-red-50" : "bg-blue-50";

  const borderColor =
    type === "success" ? "border-green-200" : type === "error" ? "border-red-200" : "border-blue-200";

  const textColor =
    type === "success" ? "text-green-800" : type === "error" ? "text-red-800" : "text-blue-800";

  const icon =
    type === "success" ? (
      <CheckCircle className="w-5 h-5 text-green-600" />
    ) : type === "error" ? (
      <AlertCircle className="w-5 h-5 text-red-600" />
    ) : (
      <Info className="w-5 h-5 text-blue-600" />
    );

  return (
    <div className={`${bgColor} border ${borderColor} rounded-lg p-4 flex items-center space-x-3 ${textColor}`}>
      {icon}
      <span className="flex-1">{message}</span>
      <button onClick={onClose} className="text-xl font-bold opacity-70 hover:opacity-100">
        ×
      </button>
    </div>
  );
};
