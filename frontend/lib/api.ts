import axios, { AxiosInstance } from "axios";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

const api: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("authToken");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle errors - don't auto-redirect, let pages handle it
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Only redirect if user is not already on login/register page
      const currentPath = typeof window !== "undefined" ? window.location.pathname : "";
      if (currentPath !== "/login" && currentPath !== "/register") {
        localStorage.removeItem("authToken");
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

export default api;
