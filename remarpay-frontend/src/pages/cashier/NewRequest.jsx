import React from "react";
export default function NewRequest() {
  return (
    <div className="max-w-3xl mx-auto bg-white dark:bg-gray-800 p-6 rounded-xl shadow-lg">
      <h2 className="text-2xl font-bold text-indigo-600 dark:text-indigo-400 mb-6">
        New Payment Request
      </h2>
      <p className="text-gray-600 dark:text-gray-300">
        This is where the cashier can initiate a new payment request. We'll build out the full form next.
      </p>
    </div>
  );
}

