import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../api/axios";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const res = await api.post("/accounts/login/", {
        email,
        password,
      });

      localStorage.setItem("access", res.data.access);
      localStorage.setItem("refresh", res.data.refresh);

      // You can also store user info (like name) if it's returned
      // localStorage.setItem("userName", res.data.user.name);

      navigate("/dashboard");
    } catch (err) {
      console.error(err);
      setError("Invalid login credentials.");
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <form
        onSubmit={handleLogin}
        className="bg-white p-8 rounded shadow-md w-full max-w-md"
      >
        <h2 className="text-2xl font-bold mb-6 text-center text-indigo-600">
          RemarPay Login
        </h2>

        {error && (
          <div className="bg-red-100 text-red-700 p-2 mb-4 rounded">{error}</div>
        )}

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full p-3 border mb-4 rounded"
          required
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full p-3 border mb-6 rounded"
          required
        />

        <button
          type="submit"
          className="w-full bg-indigo-600 text-white p-3 rounded hover:bg-indigo-700"
        >
          Login
        </button>
      </form>
    </div>
  );
}
