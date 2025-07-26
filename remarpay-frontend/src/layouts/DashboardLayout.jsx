import React, { useState } from "react";
import { Link, Outlet } from "react-router-dom";
import remarLogo from "/logo.jpg";

export default function DashboardLayout() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const username = localStorage.getItem("userName") || "User";
  const role = localStorage.getItem("userRole") || "guest";

  const roleNavs = {
    cashier: [
      { name: "Home", to: "/dashboard" },
      { name: "New Request", to: "/dashboard/cashier/new-request" },
      { name: "Order History", to: "/dashboard/cashier/history" },
    ],
    agent: [
      { name: "Home", to: "/dashboard" },
      { name: "Pending Payments", to: "/dashboard/agent/pending" },
      { name: "Payment History", to: "/dashboard/agent/history" },
    ],
    manager: [
      { name: "Home", to: "/dashboard" },
      { name: "All Transactions", to: "/dashboard/manager/transactions" },
      { name: "Manage Users", to: "/dashboard/manager/users" },
    ],
    "tech-admin": [
      { name: "Home", to: "/dashboard" },
      { name: "System Settings", to: "/dashboard/admin/settings" },
      { name: "User Control", to: "/dashboard/admin/users" },
    ],
  };

  const navItems = roleNavs[role] || [];

  const handleLogout = () => {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    window.location.href = "/login";
  };

  return (
    <div className="relative min-h-screen bg-white dark:bg-gray-900 text-black dark:text-white">
      {/* Sidebar */}
      <aside
        className={`fixed top-0 left-0 z-50 h-full w-64 bg-[#041c05ff] shadow-lg transition-transform duration-300 ease-in-out
        ${sidebarOpen ? "translate-x-0" : "-translate-x-full"}`}
      >
        <div className="p-4 border-b border-white/20 flex justify-between items-center">
          <img src={remarLogo} alt="RemarPay Logo" className="h-10" />
          <button
            className="text-white"
            onClick={() => setSidebarOpen(false)}
            aria-label="Close sidebar"
          >
            ✖
          </button>
        </div>

        <nav className="mt-6 space-y-1 px-2">
          {navItems.map((item) => (
            <Link
              key={item.to}
              to={item.to}
              className="block px-4 py-2 rounded hover:bg-[#D4AF37] hover:text-black"
              onClick={() => setSidebarOpen(false)}
            >
              {item.name}
            </Link>
          ))}
        </nav>
      </aside>

      {/* Backdrop overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-40 bg-black bg-opacity-40"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Main layout */}
      <div className="flex flex-col min-h-screen">
        {/* Topbar */}
        <header className="flex items-center justify-between px-6 py-4 bg-[#041c05ff] text-white shadow z-30">
          <div className="flex items-center gap-4">
            <button
              onClick={() => setSidebarOpen((prev) => !prev)}
              className="text-2xl"
              aria-label="Toggle sidebar"
            >
              ☰
            </button>
            <img src={remarLogo} alt="Logo" className="h-8" />
          </div>
          <div className="flex items-center gap-4">
            <span>Hello, {username}</span>
            <button
              onClick={handleLogout}
              className="px-3 py-1 rounded bg-[#D4AF37] text-black hover:opacity-90"
            >
              Logout
            </button>
          </div>
        </header>

        {/* Scrollable content */}
        <main className="flex-1 overflow-y-auto p-6">
          <div className="max-w-6xl mx-auto">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
}
