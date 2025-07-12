import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import ErrorAlert from "../common/ErrorAlert";

export default function LoginForm() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) =>
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/api/accounts/login/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Invalid credentials");

      const tokenPayload = JSON.parse(atob(data.access.split('.')[1]));
      localStorage.setItem("access", data.access);
      localStorage.setItem("refresh", data.refresh);
      localStorage.setItem("userName", tokenPayload.name);
      localStorage.setItem("userRole", tokenPayload.role);
      navigate("/dashboard");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="w-full max-w-md bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-inner hover:shadow-2xl transition duration-300 transform hover:scale-[1.01]"
    >
      <h2 className="text-3xl font-semibold text-indigo-600 dark:text-indigo-300 text-center mb-8">
        Remar Exchange
      </h2>

      <ErrorAlert message={error} />

      {/* Email */}
      <div>
        <label htmlFor="email" className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-1">
          Email
        </label>
        <input
          id="email"
          name="email"
          type="email"
          autoComplete="email"
          required
          value={formData.email}
          onChange={handleChange}
          className="w-full px-4 py-3 rounded-xl border border-gray-200 bg-gray-50 shadow-inner focus:outline-none focus:ring-2 focus:ring-indigo-300 dark:bg-gray-700 dark:text-white dark:border-gray-600"
          placeholder="mdederi@example.com"
        />
      </div>

      {/* Password */}
      <div className="mt-4">
        <label htmlFor="password" className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-1">
          Password
        </label>
        <input
          id="password"
          name="password"
          type="password"
          autoComplete="current-password"
          required
          value={formData.password}
          onChange={handleChange}
          className="w-full px-4 py-3 rounded-xl border border-gray-200 bg-gray-50 shadow-inner focus:outline-none focus:ring-2 focus:ring-indigo-300 dark:bg-gray-700 dark:text-white dark:border-gray-600"
          placeholder="••••••••"
        />
        <div className="text-right mt-2">
          <button
            type="button"
            onClick={() => navigate("/forgot-password")}
            className="text-sm text-indigo-500 hover:underline focus:outline-none"
          >
            Forgot password?
          </button>
        </div>
      </div>

      {/* Submit */}
      <button
        type="submit"
        disabled={loading}
        className={`w-full mt-6 py-3 rounded-xl text-white font-medium transition-transform bg-gradient-to-r from-indigo-500 to-teal-400 hover:scale-105 transform ${
          loading ? "opacity-50 cursor-not-allowed" : ""
        }`}
      >
        {loading ? "Logging in…" : "Login"}
      </button>
    </form>
  );
}
