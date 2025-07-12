import React from "react";

export default function ErrorAlert({ message }) {
  if (!message) return null;
  return (
    <div className="mb-4 px-4 py-2 bg-red-100 text-red-700 rounded-lg dark:bg-red-800 dark:text-white" role="alert" aria-live="assertive">
      {message}
    </div>
  );
}
