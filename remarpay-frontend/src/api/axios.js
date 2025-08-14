// src/api/axios.js
import axios from "axios";

// Create base axios instance
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api",
  headers: {
    "Content-Type": "application/json",
  },
});

// Request Interceptor → Attach token to every request
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response Interceptor → Handle token expiration
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Prevent infinite loop
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      const refreshToken = localStorage.getItem("refresh");

      if (refreshToken) {
        try {
          // Request new access token
          const { data } = await axios.post(
            `${import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api"}/token/refresh/`,
            { refresh: refreshToken },
            { headers: { "Content-Type": "application/json" } }
          );

          // Save new token
          localStorage.setItem("access", data.access);

          // Retry original request with new token
          api.defaults.headers.Authorization = `Bearer ${data.access}`;
          originalRequest.headers.Authorization = `Bearer ${data.access}`;
          return api(originalRequest);
        } catch (err) {
          console.error("Token refresh failed", err);
          localStorage.removeItem("access");
          localStorage.removeItem("refresh");
          window.location.href = "/login"; // Redirect to login
        }
      }
    }

    return Promise.reject(error);
  }
);

export default api;