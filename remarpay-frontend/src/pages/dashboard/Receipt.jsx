import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";

export default function Receipt() {
  const { id } = useParams();
  const [receipt, setReceipt] = useState(null);
  const access = localStorage.getItem("access");

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/api/payments/cashier/receipt/${id}/`, {
      headers: {
        Authorization: `Bearer ${access}`,
      },
    })
      .then(res => res.json())
      .then(data => setReceipt(data))
      .catch(err => console.error("❌ Receipt fetch error:", err));
  }, [id]);

  if (!receipt) return <div className="text-center p-4">Loading receipt...</div>;

  return (
    <div className="p-4 max-w-xl mx-auto">
      <h2 className="text-xl font-bold mb-2">Receipt</h2>
      <pre className="bg-muted p-4 rounded">{JSON.stringify(receipt, null, 2)}</pre>
    </div>
  );
}
