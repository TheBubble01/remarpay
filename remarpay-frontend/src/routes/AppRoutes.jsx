import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";

// Public pages
import Login from "../pages/auth/Login";

// Protected components
import ProtectedRoute from "../components/common/ProtectedRoute";
import DashboardLayout from "../layouts/DashboardLayout";
import Dashboard from "../pages/dashboard/Dashboard";

// Cashier pages
import NewRequest from "../pages/cashier/NewRequest";
import Receipt from "../pages/dashboard/Receipt";
import CashierHistory from "../pages/cashier/CashierHistory";

// Fallback
import NotFound from "../pages/shared/NotFound";

export default function AppRoutes() {
  return (
    <Routes>
      {/* Public Route */}
      <Route path="/login" element={<Login />} />

      {/* Protected Routes */}
      <Route element={<ProtectedRoute />}>
        <Route path="/dashboard" element={<DashboardLayout />}>
          <Route index element={<Dashboard />} />
          <Route path="cashier/new-request" element={<NewRequest />} />
          <Route path="/dashboard/receipt/:id" element={<Receipt />} />
          <Route path="cashier/history" element={<CashierHistory />} />
        </Route>
      </Route>

      {/* Redirect root to login */}
      <Route path="/" element={<Navigate to="/login" replace />} />

      {/* 404 */}
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}

