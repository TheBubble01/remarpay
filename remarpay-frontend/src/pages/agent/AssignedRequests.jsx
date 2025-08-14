// src/pages/agent/AssignedRequests.jsx
import { useEffect, useMemo, useState, useRef } from "react";
import { Link } from "react-router-dom";
import axios from "../../api/axios";

// Brand colors
const BRAND = {
  green: "#014421",
  gold: "#D4AF37",
};

const PAGE_SIZE = 10;

export default function AssignedRequests() {
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [page, setPage] = useState(1);
  const errRef = useRef(null);

  useEffect(() => {
    let isMounted = true;
    setLoading(true);
    setError("");

    // IMPORTANT: axios baseURL should already include '/api'.
    // Endpoint from your urls.py: path('agent/requests/', AssignedRequestsListView.as_view(), name='agent-requests')
    axios
      .get("/payments/agent/requests/")
      .then((res) => {
        if (!isMounted) return;
        setRequests(Array.isArray(res.data) ? res.data : []);
      })
      .catch((err) => {
        if (!isMounted) return;
        console.error("❌ Error fetching assigned requests:", err);
        setError(
          err?.response?.data?.detail ||
            err?.message ||
            "Failed to load assigned requests."
        );
      })
      .finally(() => isMounted && setLoading(false));

    return () => {
      isMounted = false;
    };
  }, []);

  useEffect(() => {
    if (error && errRef.current) {
      errRef.current.focus();
    }
  }, [error]);

  // Client-side pagination
  const totalPages = Math.max(1, Math.ceil(requests.length / PAGE_SIZE));
  const pageSafe = Math.min(page, totalPages);
  const paged = useMemo(() => {
    const start = (pageSafe - 1) * PAGE_SIZE;
    return requests.slice(start, start + PAGE_SIZE);
  }, [requests, pageSafe]);

  const gotoPage = (n) => setPage(Math.min(Math.max(1, n), totalPages));

  const formatDate = (isoOrDateLike) => {
    if (!isoOrDateLike) return "—";
    // Accept ISO or already Date-like string; rely on Date parsing.
    const d = new Date(isoOrDateLike);
    if (isNaN(d.getTime())) return "—";
    const day = d.toLocaleString("en-GB", { day: "2-digit" });
    const month = d.toLocaleString("en-GB", { month: "short" });
    const year = d.getFullYear();
    const time = d.toLocaleString("en-GB", {
      hour: "numeric",
      minute: "2-digit",
      hour12: true,
    });
    return `${day} ${month} ${year}, ${time}`;
  };

  return (
    <div className="w-full px-4 sm:px-6 lg:px-8 mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mt-2 mb-4">
        <h1
          className="text-xl sm:text-2xl font-bold"
          style={{ color: BRAND.green }}
        >
          Assigned Payment Requests
        </h1>

        <div className="flex items-center gap-2">
          <button
            onClick={() => window.location.reload()}
            className="rounded-lg px-3 py-2 text-sm font-medium border"
            style={{
              borderColor: BRAND.green,
              color: BRAND.green,
            }}
            aria-label="Refresh list"
          >
            Refresh
          </button>
        </div>
      </div>

      {/* Error */}
      {error && (
        <div
          ref={errRef}
          tabIndex={-1}
          className="mb-4 rounded-lg border border-red-300 bg-red-50 p-3 text-red-700"
          role="alert"
          aria-live="assertive"
        >
          {error}
        </div>
      )}

      {/* Loading */}
      {loading && (
        <div className="rounded-xl p-4 bg-white dark:bg-gray-900 shadow">
          <SkeletonTable />
        </div>
      )}

      {/* Empty */}
      {!loading && !error && requests.length === 0 && (
        <div className="rounded-xl p-8 bg-white dark:bg-gray-900 text-center shadow">
          <p className="text-gray-700 dark:text-gray-200">
            No assigned requests found.
          </p>
          <p className="text-sm text-gray-500 mt-1">
            New requests will show up here automatically.
          </p>
        </div>
      )}

      {/* Table */}
      {!loading && !error && requests.length > 0 && (
        <div className="rounded-2xl overflow-hidden shadow bg-white dark:bg-gray-900">
          <div className="overflow-x-auto">
            <table
              className="min-w-full text-sm"
              aria-label="Assigned requests table"
            >
              <thead
                className="text-left"
                style={{ backgroundColor: BRAND.green, color: "white" }}
              >
                <tr>
                  <Th>#</Th>
                  <Th>Receiver</Th>
                  <Th>Amount (Dinar)</Th>
                  <Th>Date</Th>
                  <Th>Depositor</Th>
                  <Th>Status</Th>
                  <Th className="text-right pr-4">Actions</Th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 dark:divide-gray-800">
                {paged.map((r, i) => (
                  <tr
                    key={r.id}
                    className="hover:bg-gray-50 dark:hover:bg-gray-800/60 transition-colors"
                  >
                    <Td>{(pageSafe - 1) * PAGE_SIZE + i + 1}</Td>
                    <Td className="font-medium">{r.receiver_name || "—"}</Td>
                    <Td className="tabular-nums">
                      {Number(r.deposit_amount_dinar)?.toLocaleString() ?? "—"}
                    </Td>
                    <Td>{formatDate(r.created_at)}</Td>
                    <Td>{r.depositor_name || "—"}</Td>
                    <Td>
                      {r.is_cancelled ? (
                        <Badge color="red">Cancelled</Badge>
                      ) : r.is_paid ? (
                        <Badge color="green">Paid</Badge>
                      ) : (
                        <Badge color="amber">Pending</Badge>
                      )}
                    </Td>
                    <Td className="text-right pr-4">
                      <div className="flex justify-end gap-2">
                        {/* View → use cashier style for consistency */}
                        <Link
                          to={`/dashboard/receipt/${r.id}`}
                          className="inline-flex items-center rounded-lg px-3 py-2 text-xs font-semibold"
                          style={{
                            backgroundColor: BRAND.green,
                            color: "white",
                          }}
                        >
                          View
                        </Link>

                        {/* Confirm – we’ll wire to the confirm page/modal next step */}
                        {!r.is_paid && !r.is_cancelled && (
                          <Link
                            to={`/dashboard/agent/confirm/${r.id}`}
                            className="inline-flex items-center rounded-lg px-3 py-2 text-xs font-semibold"
                            style={{
                              border: `1px solid ${BRAND.green}`,
                              color: BRAND.green,
                            }}
                          >
                            Confirm
                          </Link>
                        )}
                      </div>
                    </Td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          <div className="flex items-center justify-between px-4 py-3">
            <span className="text-xs sm:text-sm text-gray-600 dark:text-gray-300">
              Showing {(pageSafe - 1) * PAGE_SIZE + 1}–
              {Math.min(pageSafe * PAGE_SIZE, requests.length)} of{" "}
              {requests.length}
            </span>

            <div className="flex items-center gap-2">
              <button
                onClick={() => gotoPage(pageSafe - 1)}
                disabled={pageSafe === 1}
                className="rounded-md px-3 py-2 text-sm font-medium disabled:opacity-50"
                style={{
                  border: `1px solid ${BRAND.green}`,
                  color: BRAND.green,
                }}
              >
                Prev
              </button>
              <span className="text-sm tabular-nums">
                {pageSafe} / {totalPages}
              </span>
              <button
                onClick={() => gotoPage(pageSafe + 1)}
                disabled={pageSafe === totalPages}
                className="rounded-md px-3 py-2 text-sm font-medium disabled:opacity-50"
                style={{
                  border: `1px solid ${BRAND.green}`,
                  color: BRAND.green,
                }}
              >
                Next
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

/* ---------- Small presentational helpers ---------- */

function Th({ children, className = "" }) {
  return (
    <th
      scope="col"
      className={`px-4 py-3 text-xs sm:text-sm font-semibold whitespace-nowrap ${className}`}
    >
      {children}
    </th>
  );
}

function Td({ children, className = "" }) {
  return (
    <td className={`px-4 py-3 align-middle whitespace-nowrap ${className}`}>
      {children}
    </td>
  );
}

function Badge({ color = "gray", children }) {
  const map = {
    green: "bg-green-600 text-white",
    red: "bg-red-600 text-white",
    amber: "bg-amber-400 text-black",
    gray: "bg-gray-200 text-gray-800",
  };
  return (
    <span className={`px-2 py-1 rounded text-[10px] sm:text-xs ${map[color]}`}>
      {children}
    </span>
  );
}

function SkeletonTable() {
  return (
    <div className="animate-pulse">
      <div className="h-6 w-48 mb-4 rounded" style={{ background: "#e5e7eb" }} />
      <div className="space-y-2">
        {[...Array(6)].map((_, i) => (
          <div
            key={i}
            className="h-10 w-full rounded"
            style={{ background: "#f3f4f6" }}
          />
        ))}
      </div>
    </div>
  );
}
