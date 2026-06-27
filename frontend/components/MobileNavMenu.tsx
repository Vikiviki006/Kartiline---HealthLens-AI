import React from "react";
import Link from "next/link";

interface NavMenuProps {
  isOpen: boolean;
  onClose: () => void;
}

export const MobileNavMenu: React.FC<NavMenuProps> = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-40" onClick={onClose}>
      <div
        className="fixed left-0 top-0 w-64 h-screen bg-white shadow-lg"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="p-6 space-y-4">
          <Link href="/dashboard" onClick={onClose} className="block text-gray-700 hover:text-blue-600">
            Dashboard
          </Link>
          <Link href="/upload" onClick={onClose} className="block text-gray-700 hover:text-blue-600">
            Upload Report
          </Link>
          <Link href="/profile" onClick={onClose} className="block text-gray-700 hover:text-blue-600">
            Profile
          </Link>
          <div className="border-t pt-4">
            <button
              onClick={() => {
                localStorage.removeItem("authToken");
                window.location.href = "/login";
              }}
              className="w-full text-left text-red-600 hover:text-red-700"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
