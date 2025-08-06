import { useEffect, useState } from "react";
import axios from "../../api/axios";
import DashboardLayout from "../../layouts/DashboardLayout";

const AssignedRequests = () => {
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchRequests = async () => {
      try {
        const res = await axios.get("/api/payments/assigned/");
        setRequests(res.data);
      } catch (err) {
        console.error("Error fetching assigned requests:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchRequests();
  }, []);

  return (
    <DashboardLayout>
      <div className="p-4">
        <h1 className="text-2xl font-bold mb-4 text-gray-800 dark:text-white">Assigned Payment Requests</h1>

        {loading ? (
          <p className="text-gray-600 dark:text-gray-300">Loading...</p>
        ) : requests.length === 0 ? (
          <p className="text-gray-600 dark:text-gray-300">No assigned requests found.</p>
        ) : (
          <div className="overflow-x-auto bg-white dark:bg-[#014421] rounded shadow">
            <table className="min-w-full text-sm text-gray-800 dark:text-white">
              <thead className="bg-[#041c05ff] text-white">
                <tr>
                  <th className="p-2">#</th>
                  <th className="p-2">Receiver</th>
                  <th className="p-2">Amount</th>
                  <th className="p-2">Date</th>
                  <th className="p-2">Depositor</th>
                  <th className="p-2">Action</th>
                </tr>
              </thead>
              <tbody>
                {requests.map((r, i) => (
                  <tr key={r.id} className="border-b border-gray-300 dark:border-gray-600">
                    <td className="p-2">{i + 1}</td>
                    <td className="p-2">{r.receiver_name}</td>
                    <td className="p-2">{r.deposit_amount_dinar}</td>
                    <td className="p-2">
                      {r.created_at
                        ? new Date(r.created_at).toLocaleString("en-GB", {
                            day: "2-digit",
                            month: "short",
                            year: "numeric",
                            hour: "numeric",
                            minute: "2-digit",
                            hour12: true,
                          })
                        : "—"}
                    </td>
                    <td className="p-2">{r.depositor_name}</td>
                    <td className="p-2">
                      <button className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 text-xs rounded">
                        Confirm
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
};

export default AssignedRequests;
