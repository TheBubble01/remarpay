// src/pages/dashboard/NewRequest.jsx
import React, { useState } from "react";

const COUNTRIES = ["nigeria", "niger", "cameroon"];

export default function NewRequest() {
  const [form, setForm] = useState({
    depositorName: "",
    depositorPhone: "",
    country: "nigeria",
    amount: "",
    note: "",
    // Nigeria
    bankName: "",
    accountNumber: "",
    accountName: "",
    // NITA
    receiverName: "",
    receiverPhone: "",
    nitaOffice: "",
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    alert("Request submitted (simulation). Check console for payload.");
    console.log(form);
  };

  const renderReceiverFields = () => {
    if (form.country === "nigeria") {
      return (
        <>
          <Input label="Bank Name" name="bankName" value={form.bankName} onChange={handleChange} />
          <Input label="Account Number" name="accountNumber" value={form.accountNumber} onChange={handleChange} />
          <Input label="Account Name" name="accountName" value={form.accountName} onChange={handleChange} />
        </>
      );
    } else {
      return (
        <>
          <Input label="NITA Office" name="nitaOffice" value={form.nitaOffice} onChange={handleChange} />
          <Input label="Receiver Full Name" name="receiverName" value={form.receiverName} onChange={handleChange} />
          <Input label="Receiver Phone" name="receiverPhone" value={form.receiverPhone} onChange={handleChange} />
        </>
      );
    }
  };

  const transferFee = form.amount && Number(form.amount) < 500 ? 5 : 0;

  return (
    <div className="max-w-3xl mx-auto bg-white dark:bg-gray-900 dark:text-white shadow-xl rounded-2xl p-6 md:p-8">
      <h2 className="text-2xl font-semibold mb-6 text-indigo-600 dark:text-indigo-400">
        New Payment Request
      </h2>

      <form onSubmit={handleSubmit} className="space-y-5">
        <Input label="Depositor Name" name="depositorName" value={form.depositorName} onChange={handleChange} />
        <Input label="Depositor Phone" name="depositorPhone" value={form.depositorPhone} onChange={handleChange} />

        <div>
          <label className="block text-sm font-medium mb-1">Destination Country</label>
          <select
            name="country"
            value={form.country}
            onChange={handleChange}
            className="w-full px-4 py-3 rounded-xl border border-gray-300 bg-gray-50 dark:bg-gray-800 dark:border-gray-700 focus:outline-none focus:ring-2 focus:ring-indigo-400"
          >
            {COUNTRIES.map((c) => (
              <option key={c} value={c}>
                {c.charAt(0).toUpperCase() + c.slice(1)}
              </option>
            ))}
          </select>
        </div>

        {renderReceiverFields()}

        <Input
          label="Amount (Dinar)"
          name="amount"
          value={form.amount}
          onChange={handleChange}
          type="number"
        />

        {transferFee > 0 && (
          <div className="text-sm text-red-600 dark:text-red-400 font-medium">
            Note: 5 Dinar fee applies for amounts under 500
          </div>
        )}

        <div>
          <label className="block text-sm font-medium mb-1">Optional Note</label>
          <textarea
            name="note"
            value={form.note}
            onChange={handleChange}
            rows="3"
            className="w-full px-4 py-3 rounded-xl border border-gray-300 bg-gray-50 dark:bg-gray-800 dark:border-gray-700 focus:outline-none focus:ring-2 focus:ring-indigo-400"
          ></textarea>
        </div>

        <button
          type="submit"
          className="w-full py-3 rounded-xl text-white font-medium bg-gradient-to-r from-indigo-500 to-teal-500 hover:scale-[1.02] transition-transform"
        >
          Submit Request
        </button>
      </form>
    </div>
  );
}

function Input({ label, name, value, onChange, type = "text" }) {
  return (
    <div>
      <label className="block text-sm font-medium mb-1">{label}</label>
      <input
        type={type}
        name={name}
        value={value}
        onChange={onChange}
        className="w-full px-4 py-3 rounded-xl border border-gray-300 bg-gray-50 dark:bg-gray-800 dark:border-gray-700 focus:outline-none focus:ring-2 focus:ring-indigo-400"
        required
      />
    </div>
  );
}
