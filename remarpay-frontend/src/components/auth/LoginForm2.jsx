import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
//import GradientWrapper from "/components/GradientWrapper"; // if used before
import ErrorAlert from "../common/ErrorAlert"; // for error display
import remarLogo from "/logo.jpg"; // Ensure this exists

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const response = await axios.post(
        `${import.meta.env.VITE_API_URL}/accounts/token/`,
        { email, password }
      );
      const { access, refresh, name, role } = response.data;

      localStorage.setItem("access", access);
      localStorage.setItem("refresh", refresh);
      localStorage.setItem("userName", name);
      localStorage.setItem("userRole", role);

      navigate("/dashboard");
    } catch (err) {
      setError("Invalid credentials. Please try again.");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-forest text-white p-4">
      <div className="w-full max-w-md bg-white text-black dark:bg-gray-800 dark:text-white rounded-2xl shadow-lg p-8">
        <div className="flex flex-col items-center mb-6">
          <img src={remarLogo} alt="RemarPay Logo" className="h-16 mb-2" />
          <h1 className="text-2xl font-bold text-forest dark:text-gold">Welcome to RemarPay</h1>
          <p className="text-sm text-gray-600 dark:text-gray-300">Please login to continue</p>
        </div>

        {error && <ErrorAlert message={error} />}

        <form onSubmit={handleLogin} className="space-y-4">
          <div>
            <label className="block mb-1">Email</label>
            <input
              type="email"
              className="w-full px-4 py-2 rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-black dark:text-white"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              autoFocus
            />
          </div>
          <div>
            <label className="block mb-1">Password</label>
            <input
              type="password"
              className="w-full px-4 py-2 rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-black dark:text-white"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button
            type="submit"
            className="w-full py-2 bg-gold text-black font-semibold rounded hover:opacity-90 transition"
          >
            Login
          </button>
        </form>
      </div>
    </div>
  );
}
