import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/router";
import { Layout } from "@/components/Layout";
import { User, Mail, Lock, Bell, Shield, Trash2, LogOut } from "lucide-react";

export default function ProfilePage() {
  const router = useRouter();
  const [profile, setProfile] = useState({
    fullName: localStorage.getItem("userName") || "John Doe",
    email: "john@example.com",
    phone: "+1 (555) 123-4567",
    dateOfBirth: "1990-01-15",
  });

  const [settings, setSettings] = useState({
    emailNotifications: true,
    reportReminders: true,
    healthTips: false,
    twoFactor: false,
  });

  const [activeTab, setActiveTab] = useState("profile");

  const handleLogout = () => {
    localStorage.removeItem("authToken");
    localStorage.removeItem("userName");
    router.push("/login");
  };

  const handleProfileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setProfile((prev) => ({ ...prev, [name]: value }));
  };

  const handleSettingChange = (key: keyof typeof settings) => {
    setSettings((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  const handleSaveProfile = () => {
    localStorage.setItem("userName", profile.fullName);
    alert("Profile updated successfully!");
  };

  return (
    <Layout>
      <div className="space-y-8">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Account Settings</h1>
          <p className="text-gray-600 mt-2">Manage your profile and preferences</p>
        </div>

        {/* Tabs */}
        <div className="bg-white border border-gray-200 rounded-lg">
          <div className="flex border-b border-gray-200">
            <button
              onClick={() => setActiveTab("profile")}
              className={`px-6 py-3 font-medium ${
                activeTab === "profile"
                  ? "text-blue-600 border-b-2 border-blue-600"
                  : "text-gray-600 hover:text-gray-900"
              }`}
            >
              <User className="w-5 h-5 inline mr-2" />
              Profile
            </button>
            <button
              onClick={() => setActiveTab("security")}
              className={`px-6 py-3 font-medium ${
                activeTab === "security"
                  ? "text-blue-600 border-b-2 border-blue-600"
                  : "text-gray-600 hover:text-gray-900"
              }`}
            >
              <Shield className="w-5 h-5 inline mr-2" />
              Security
            </button>
            <button
              onClick={() => setActiveTab("notifications")}
              className={`px-6 py-3 font-medium ${
                activeTab === "notifications"
                  ? "text-blue-600 border-b-2 border-blue-600"
                  : "text-gray-600 hover:text-gray-900"
              }`}
            >
              <Bell className="w-5 h-5 inline mr-2" />
              Notifications
            </button>
          </div>

          {/* Tab Content */}
          <div className="p-6">
            {/* Profile Tab */}
            {activeTab === "profile" && (
              <div className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Full Name
                    </label>
                    <input
                      type="text"
                      name="fullName"
                      value={profile.fullName}
                      onChange={handleProfileChange}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Email
                    </label>
                    <input
                      type="email"
                      name="email"
                      value={profile.email}
                      onChange={handleProfileChange}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Phone
                    </label>
                    <input
                      type="tel"
                      name="phone"
                      value={profile.phone}
                      onChange={handleProfileChange}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Date of Birth
                    </label>
                    <input
                      type="date"
                      name="dateOfBirth"
                      value={profile.dateOfBirth}
                      onChange={handleProfileChange}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                </div>

                <button
                  onClick={handleSaveProfile}
                  className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  Save Changes
                </button>
              </div>
            )}

            {/* Security Tab */}
            {activeTab === "security" && (
              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-4">
                    Password
                  </label>
                  <button className="px-4 py-2 bg-gray-100 text-gray-900 rounded-lg hover:bg-gray-200 flex items-center space-x-2">
                    <Lock className="w-5 h-5" />
                    <span>Change Password</span>
                  </button>
                </div>

                <div className="border-t pt-6">
                  <label className="flex items-center space-x-3 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={settings.twoFactor}
                      onChange={() => handleSettingChange("twoFactor")}
                      className="w-5 h-5 text-blue-600 rounded"
                    />
                    <div>
                      <p className="font-medium text-gray-900">Two-Factor Authentication</p>
                      <p className="text-sm text-gray-600">Add extra security to your account</p>
                    </div>
                  </label>
                </div>

                <div className="border-t pt-6">
                  <h3 className="font-semibold text-gray-900 mb-3">Active Sessions</h3>
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <p className="text-sm text-gray-700">This Browser - Current Session</p>
                    <p className="text-xs text-gray-500 mt-1">Last active: Just now</p>
                  </div>
                </div>

                <div className="border-t pt-6">
                  <button className="px-4 py-2 bg-red-100 text-red-600 rounded-lg hover:bg-red-200">
                    Sign Out from All Devices
                  </button>
                </div>
              </div>
            )}

            {/* Notifications Tab */}
            {activeTab === "notifications" && (
              <div className="space-y-4">
                <label className="flex items-center space-x-3 p-4 hover:bg-gray-50 rounded-lg cursor-pointer border border-gray-200">
                  <input
                    type="checkbox"
                    checked={settings.emailNotifications}
                    onChange={() => handleSettingChange("emailNotifications")}
                    className="w-5 h-5 text-blue-600 rounded"
                  />
                  <div>
                    <p className="font-medium text-gray-900">Email Notifications</p>
                    <p className="text-sm text-gray-600">Receive important updates via email</p>
                  </div>
                </label>

                <label className="flex items-center space-x-3 p-4 hover:bg-gray-50 rounded-lg cursor-pointer border border-gray-200">
                  <input
                    type="checkbox"
                    checked={settings.reportReminders}
                    onChange={() => handleSettingChange("reportReminders")}
                    className="w-5 h-5 text-blue-600 rounded"
                  />
                  <div>
                    <p className="font-medium text-gray-900">Report Reminders</p>
                    <p className="text-sm text-gray-600">Get reminders to upload new reports</p>
                  </div>
                </label>

                <label className="flex items-center space-x-3 p-4 hover:bg-gray-50 rounded-lg cursor-pointer border border-gray-200">
                  <input
                    type="checkbox"
                    checked={settings.healthTips}
                    onChange={() => handleSettingChange("healthTips")}
                    className="w-5 h-5 text-blue-600 rounded"
                  />
                  <div>
                    <p className="font-medium text-gray-900">Health Tips</p>
                    <p className="text-sm text-gray-600">Receive personalized health tips</p>
                  </div>
                </label>
              </div>
            )}
          </div>
        </div>

        {/* Danger Zone */}
        <div className="bg-red-50 border border-red-200 rounded-lg p-6">
          <h2 className="text-lg font-semibold text-red-900 mb-4">Danger Zone</h2>
          <div className="space-y-3">
            <button className="w-full px-4 py-2 bg-red-100 text-red-600 rounded-lg hover:bg-red-200 flex items-center justify-between">
              <span>Delete All Data</span>
              <Trash2 className="w-5 h-5" />
            </button>
            <button
              onClick={handleLogout}
              className="w-full px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 flex items-center justify-between"
            >
              <span>Logout</span>
              <LogOut className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </Layout>
  );
}
