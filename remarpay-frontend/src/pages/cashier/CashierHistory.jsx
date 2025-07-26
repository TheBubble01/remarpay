// src/pages/cashier/CashierHistory.jsx

import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

const API_URL = "http://127.0.0.1:8000/api/payments/cashier/history/";

export default function CashierHistory() {
  const [payments, setPayments] = useState([]);
  const [filters, setFilters] = useState({
    receiver: "",
    depositor_phone: "",
    start_date: "",
    end_date: "",
    is_paid: "",
    is_cancelled: "",
  });
  const [page, setPage] = useState(1);
  const [count, setCount] = useState(0);

  const access = localStorage.getItem("access");

  useEffect(() => {
    const params = new URLSearchParams({ page, ...filters });

    fetch(`${API_URL}?${params}`, {
      headers: {
        Authorization: `Bearer ${access}`,
      },
    })
      .then((res) => res.json())
      .then((data) => {
        setPayments(data.results || []);
        setCount(data.count || 0);
      })
      .catch((err) => console.error("Error fetching history:", err));
  }, [filters, page]);

  const handleInputChange = (e) => {
    setFilters({ ...filters, [e.target.name]: e.target.value });
    setPage(1);
  };

  const handleCancel = (id) => {
    const reason = prompt("Reason for cancellation?");
    if (!reason) return;

    fetch(`http://127.0.0.1:8000/api/payments/cashier/cancel/${id}/`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${access}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ reason }),
    })
      .then((res) => res.json())
      .then(() => {
        alert("Cancelled successfully");
        setPayments((prev) =>
          prev.map((p) =>
            p.id === id ? { ...p, is_cancelled: true } : p
          )
        );
      });
  };

  return (
    <div className="max-w-6xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4 text-[#D4AF37]">Transaction History</h1>

      {/* Filters */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <input
          name="receiver"
          placeholder="Receiver name/phone"
          value={filters.receiver}
          onChange={handleInputChange}
          className="px-3 py-2 rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#D4AF37]"
        />
        <input
          name="depositor_phone"
          placeholder="Depositor phone"
          value={filters.depositor_phone}
          onChange={handleInputChange}
          className="px-3 py-2 rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#D4AF37]"
        />
        <input
          type="date"
          name="start_date"
          value={filters.start_date}
          onChange={handleInputChange}
          className="px-3 py-2 rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#D4AF37]"
        />
        <input
          type="date"
          name="end_date"
          value={filters.end_date}
          onChange={handleInputChange}
          className="px-3 py-2 rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#D4AF37]"
        />
        <select name="is_paid" onChange={handleInputChange} className="px-3 py-2 rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#D4AF37]"
 value={filters.is_paid}>
          <option value="">All Status</option>
          <option value="true">Paid</option>
          <option value="false">Unpaid</option>
        </select>
        <select name="is_cancelled" onChange={handleInputChange} className="px-3 py-2 rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#D4AF37]"
 value={filters.is_cancelled}>
          <option value="">All</option>
          <option value="false">Active</option>
          <option value="true">Cancelled</option>
        </select>
      </div>

      {/* Table */}
      <div className="overflow-x-auto rounded-lg shadow-lg bg-white dark:bg-[#041c05ff]">
        <table className="min-w-full text-sm text-gray-900 dark:text-white">
            <thead className="bg-[#041c05ff] text-white uppercase text-xs tracking-wider">
            <tr>
                <th className="px-4 py-3 text-left">#</th>
                <th className="px-4 py-3 text-left">Receiver</th>
                <th className="px-4 py-3 text-left">Amount (Dinar)</th>
                <th className="px-4 py-3 text-left">Date</th>
                <th className="px-4 py-3 text-left">Status</th>
                <th className="px-4 py-3 text-left">Actions</th>
            </tr>
            </thead>
            <tbody>
            {payments.map((p, i) => (
                <tr
                key={p.id}
                className={`border-b dark:border-[#1a5233] ${
                    i % 2 === 0 ? "bg-gray-50 dark:bg-[#014421]" : "bg-white dark:bg-[#025932]"
                } hover:bg-gray-100 dark:hover:bg-[#027d4f] transition`}
                >
                <td className="px-4 py-3">{(page - 1) * 10 + i + 1}</td>
                <td className="px-4 py-3">{p.receiver_name}</td>
                <td className="px-4 py-3">{p.deposit_amount_dinar}</td>
                <td className="px-4 py-3">{p.created_at.toLocaleDateString()}</td>
                <td className="px-4 py-3">
                    {p.is_cancelled ? (
                    <span className="inline-block bg-red-600 text-white text-xs px-3 py-1 rounded-full font-medium">
                        Cancelled
                    </span>
                    ) : p.is_paid ? (
                    <span className="inline-block bg-green-700 text-white text-xs px-3 py-1 rounded-full font-medium">
                        Paid
                    </span>
                    ) : (
                    <span className="inline-block bg-yellow-400 text-black text-xs px-3 py-1 rounded-full font-medium">
                        Unpaid
                    </span>
                    )}
                </td>
                <td className="px-4 py-3 space-x-2 flex items-center">
                    <Link
                    to={`/dashboard/receipt/${p.id}`}
                    className="inline-block bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded-md text-xs font-medium transition"
                    >
                    View
                    </Link>
                    {!p.is_paid && !p.is_cancelled && (
                    <button
                        onClick={() => handleCancel(p.id)}
                        className="inline-block bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded-md text-xs font-medium transition"
                    >
                        Cancel
                    </button>
                    )}
                </td>
                </tr>
            ))}
            </tbody>
        </table>
      </div>
        
      {/* Pagination */}
      <div className="flex justify-center mt-6">
        {Array.from({ length: Math.ceil(count / 10) }, (_, i) => (
          <button
            key={i}
            onClick={() => setPage(i + 1)}
            className={`px-3 py-1 mx-1 rounded ${
              i + 1 === page
                ? "bg-[#D4AF37] text-white"
                : "bg-gray-200 dark:bg-gray-700"
            }`}
          >
            {i + 1}
          </button>
        ))}
      </div>
    </div>
  );
}
