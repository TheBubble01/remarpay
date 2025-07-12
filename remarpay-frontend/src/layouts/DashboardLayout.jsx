import React, { useState } from "react";
import { Link, Outlet } from "react-router-dom";

export default function DashboardLayout() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const username = localStorage.getItem("userName") || "User";
  // const role = localStorage.getItem("userRole") || "guest";

  const handleLogout = () => {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    window.location.href = "/login";
  };

  const navItems = [
    { name: "Home", to: "/dashboard" },
    // { name: "New Request", to: "/dashboard/cashier/new-request" },
    // ... add based on role
  ];

  return (
    <div className="flex h-screen overflow-hidden">
      {/* Sidebar */}
      <div
        className={`
          fixed inset-y-0 left-0 transform bg-white shadow-lg 
          ${sidebarOpen ? "translate-x-0" : "-translate-x-full"} 
          md:relative md:translate-x-0 transition-transform duration-300
          w-64
        `}
      >
        <div className="p-4 font-bold text-xl text-indigo-600">RemarPay</div>
        <nav className="mt-6">
          {navItems.map((item) => (
            <Link
              key={item.to}
              to={item.to}
              className="block px-4 py-2 text-gray-700 hover:bg-indigo-100"
            >
              {item.name}
            </Link>
          ))}
        </nav>
      </div>

      {/* Main content */}
      <div className="flex-1 flex flex-col md:pl-64">
        {/* Top bar */}
        <header className="flex items-center justify-between bg-white shadow p-4">
          <button
            className="md:hidden"
            onClick={() => setSidebarOpen((o) => !o)}
          >
            {sidebarOpen ? "✖" : "☰"}
          </button>
          <div className="flex items-center space-x-4">
            <span className="text-gray-700">Hello, {username}</span>
            <button
              onClick={handleLogout}
              className="p-1 rounded hover:bg-gray-100"
            >
              Logout
            </button>
          </div>
        </header>

        {/* Page content */}
        <main className="flex-1 overflow-y-auto bg-gray-50 p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
