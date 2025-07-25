import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import logo from "../../assets/logo.jpg"; // Adjust path as needed

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
      .then((res) => res.json())
      .then((data) => setReceipt(data))
      .catch((err) => console.error("❌ Receipt fetch error:", err));
  }, [id]);

  if (!receipt)
    return <div className="text-center py-10 text-lg font-medium">Loading receipt...</div>;

  const {
    country,
    depositor_name,
    depositor_phone,
    deposit_amount_dinar,
    converted_amount,
    conversion_rate,
    fee_applied,
    receiver,
    bank_details,
    cashier_name,
    created_at,
  } = receipt;

  return (
    <div className="max-w-md mx-auto bg-white dark:bg-gray-900 rounded-xl shadow-lg p-6 space-y-6 mt-6 print:bg-white print:text-black print:shadow-none print:p-0">
      <div className="flex flex-col items-center text-center">
        <img src={logo} alt="Remar Logo" className="h-12 mb-2" />
        <h1 className="text-xl font-bold text-green-900 dark:text-green-300">Transaction Receipt</h1>
        <p className="text-sm text-gray-600 dark:text-gray-400">{created_at}</p>
      </div>

      <div className="border-t border-gray-300 pt-4">
        <h2 className="text-md font-semibold text-gray-700 dark:text-gray-300 mb-1">Depositor Details</h2>
        <p><span className="font-medium">Name:</span> {depositor_name}</p>
        <p><span className="font-medium">Phone:</span> {depositor_phone}</p>
      </div>

      <div className="border-t border-gray-300 pt-4">
        <h2 className="text-md font-semibold text-gray-700 dark:text-gray-300 mb-1">Receiver Details</h2>
        <p><span className="font-medium">Name:</span> {receiver?.name || bank_details?.account_name}</p>
        <p><span className="font-medium">Phone:</span> {receiver?.phone || depositor_phone}</p>
        {country === "nigeria" ? (
          <>
            <p><span className="font-medium">Bank:</span> {bank_details?.bank_name}</p>
            <p><span className="font-medium">Account Number:</span> {bank_details?.account_number}</p>
          </>
        ) : (
          <p><span className="font-medium">NITA Office:</span> {receiver?.nita_office}</p>
        )}
      </div>

      <div className="border-t border-gray-300 pt-4">
        <h2 className="text-md font-semibold text-gray-700 dark:text-gray-300 mb-1">Transaction Info</h2>
        <p><span className="font-medium">Country:</span> {country.toUpperCase()}</p>
        <p><span className="font-medium">Amount Sent:</span> {deposit_amount_dinar} Dinar</p>
        {fee_applied && <p><span className="font-medium text-red-600">Fee Applied: 5 Dinar</span></p>}
        <p><span className="font-medium">Rate:</span> {conversion_rate}</p>
        <p><span className="font-medium">Amount Received:</span> {converted_amount.toLocaleString()} {country === "nigeria" ? "NGN" : "XAF"}</p>
      </div>

      <div className="text-sm text-gray-600 dark:text-gray-400 text-right mt-6">
        <p><span className="font-medium">Cashier:</span> {cashier_name}</p>
        <p><span className="font-medium">Ref ID:</span> #{id}</p>
      </div>
    </div>
  );
}
