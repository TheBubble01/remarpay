import React from "react";

export default function Dashboard() {
  const role = localStorage.getItem("userRole") || "guest";
  const name = localStorage.getItem("userName") || "User";

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold text-gray-800 dark:text-white">
        Welcome, <strong>{name}</strong>!
      </h1>
      <p className="text-gray-600 dark:text-gray-300">
        You are logged in as a <strong>{role}</strong>.
      </p>

      {/* Simple role-based UI (will later split by route if needed) */}
      {role === "cashier" && <div>📥 Cashier Dashboard</div>}
      {role === "agent" && <div>💸 Agent Dashboard</div>}
      {role === "manager" && <div>📊 Manager Dashboard</div>}
      {role === "tech-admin" && <div>🛠️ Tech Admin Dashboard</div>}
    </div>
  );
}
