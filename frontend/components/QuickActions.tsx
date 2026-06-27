import React from "react";
import { BarChart3, TrendingUp, MessageCircle, ClipboardList } from "lucide-react";
import Link from "next/link";

interface QuickActionsProps {
  reportId: string;
}

export const QuickActions: React.FC<QuickActionsProps> = ({ reportId }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
      <Link href={`/trends/${reportId}`}>
        <div className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer">
          <BarChart3 className="w-8 h-8 text-blue-600 mb-2" />
          <h3 className="font-semibold text-gray-900">View Trends</h3>
          <p className="text-xs text-gray-600">See health marker trends</p>
        </div>
      </Link>

      <Link href={`/chat/${reportId}`}>
        <div className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer">
          <MessageCircle className="w-8 h-8 text-green-600 mb-2" />
          <h3 className="font-semibold text-gray-900">Chat AI</h3>
          <p className="text-xs text-gray-600">Ask questions about your report</p>
        </div>
      </Link>

      <Link href={`/doctor-visit/${reportId}`}>
        <div className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer">
          <ClipboardList className="w-8 h-8 text-yellow-600 mb-2" />
          <h3 className="font-semibold text-gray-900">Doctor Visit</h3>
          <p className="text-xs text-gray-600">Prepare for consultation</p>
        </div>
      </Link>

      <div className="bg-white border border-gray-200 rounded-lg p-4">
        <TrendingUp className="w-8 h-8 text-purple-600 mb-2" />
        <h3 className="font-semibold text-gray-900">Insights</h3>
        <p className="text-xs text-gray-600">AI-powered recommendations</p>
      </div>
    </div>
  );
};
