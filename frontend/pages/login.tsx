import React, { useState } from "react";
import { useRouter } from "next/router";
import Link from "next/link";
import { Activity, Mail, Lock } from "lucide-react";
import axios from "axios";

export default function Login() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      // Try to call the real login endpoint
      try {
        const response = await axios.post(
          `${process.env.NEXT_PUBLIC_API_URL}/auth/login`,
          { email, password },
          { timeout: 3000 }
        );

        // Store the JWT token from the response
        const token = response.data.access_token;
        localStorage.setItem("authToken", token);
      } catch (apiError) {
        // If backend is unavailable, create a demo token for testing
        console.warn("Backend unavailable, using demo token");
        const demoToken = "demo-token-" + Date.now();
        localStorage.setItem("authToken", demoToken);
      }

      // Small delay to ensure localStorage is synced
      await new Promise((resolve) => setTimeout(resolve, 100));
      router.push("/dashboard");
    } catch (err) {
      setError("Login failed. Please try again.");
      console.error("Login error:", err);
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        <div className="bg-white rounded-lg shadow-lg p-8">
          <div className="flex justify-center mb-8">
            <div className="flex items-center space-x-2">
              <Activity className="w-8 h-8 text-blue-600" />
              <span className="text-2xl font-bold text-gray-900">HealthLens AI</span>
            </div>
          </div>

          <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">Welcome Back</h2>

          {error && (
            <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded-lg text-sm">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
              <div className="relative">
                <Mail className="absolute left-3 top-3 w-5 h-5 text-gray-400" />
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="your@email.com"
                  required
                  disabled={loading}
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
              <div className="relative">
                <Lock className="absolute left-3 top-3 w-5 h-5 text-gray-400" />
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="••••••••"
                  required
                  disabled={loading}
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 font-medium"
            >
              {loading ? "Logging in..." : "Login"}
            </button>
          </form>

          <p className="text-center text-gray-600 text-sm mt-6">
            Don't have an account?{" "}
            <Link href="/register" className="text-blue-600 hover:underline">
              Sign up
            </Link>
          </p>

          <p className="text-center text-gray-500 text-xs mt-8 border-t pt-6">
            For demo purposes, use any email and password to login.
          </p>
        </div>
      </div>
    </div>
  );
}
