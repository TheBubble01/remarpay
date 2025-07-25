import { useParams } from "react-router-dom";
import { useEffect, useRef, useState } from "react";
import logo from "../../assets/logo.jpg";
import { toPng } from "html-to-image";

export default function Receipt() {
  const { id } = useParams();
  const [receipt, setReceipt] = useState(null);
  const access = localStorage.getItem("access");
  const receiptRef = useRef(null); // Ref for the receipt DOM

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

  const handleDownload = async () => {
    if (receiptRef.current === null) return;

    const dataUrl = await toPng(receiptRef.current);
    const link = document.createElement("a");
    link.download = `remarpay-receipt-${id}.png`;
    link.href = dataUrl;
    link.click();
  };

  const handleShareWhatsApp = async () => {
    if (!navigator.canShare || !navigator.canShare({ files: [] })) {
      alert("Sharing not supported on this device. Please download instead.");
      return;
    }

    const dataUrl = await toPng(receiptRef.current);
    const response = await fetch(dataUrl);
    const blob = await response.blob();
    const file = new File([blob], `remarpay-receipt-${id}.png`, { type: blob.type });

    try {
      await navigator.share({
        title: "RemarPay Receipt",
        text: "Here’s the receipt from RemarPay",
        files: [file],
      });
    } catch (error) {
      console.error("❌ Share failed:", error);
    }
  };

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
    <div className="max-w-md mx-auto mt-6 space-y-4">
      {/* Download & Share Buttons */}
      <div className="flex justify-center gap-4">
        <button
          onClick={handleDownload}
          className="bg-green-700 hover:bg-green-800 text-white px-4 py-2 rounded text-sm"
        >
          Download Receipt
        </button>
        <button
          onClick={handleShareWhatsApp}
          className="bg-yellow-600 hover:bg-yellow-700 text-white px-4 py-2 rounded text-sm"
        >
          Share via WhatsApp
        </button>
      </div>

      {/* Receipt Display */}
      <div
        ref={receiptRef}
        className="bg-white dark:bg-gray-900 rounded-xl shadow-lg p-6 space-y-6 print:bg-white print:text-black"
      >
        <div className="flex flex-col items-center text-center">
          <img src={logo} alt="Remar Logo" className="h-12 mb-2" />
          <h1 className="text-xl font-bold text-green-900 dark:text-green-300">
            Transaction Receipt
          </h1>
          <p className="text-sm text-gray-600 dark:text-gray-400">{created_at}</p>
        </div>

        <div className="border-t border-gray-300 pt-4">
          <h2 className="text-md font-semibold text-gray-700 dark:text-gray-300 mb-1">Depositor</h2>
          <p><strong>Name:</strong> {depositor_name}</p>
          <p><strong>Phone:</strong> {depositor_phone}</p>
        </div>

        <div className="border-t border-gray-300 pt-4">
          <h2 className="text-md font-semibold text-gray-700 dark:text-gray-300 mb-1">Receiver</h2>
          <p><strong>Name:</strong> {receiver?.name || bank_details?.account_name}</p>
          <p><strong>Phone:</strong> {receiver?.phone || depositor_phone}</p>
          {country === "nigeria" ? (
            <>
              <p><strong>Bank:</strong> {bank_details?.bank_name}</p>
              <p><strong>Acct No:</strong> {bank_details?.account_number}</p>
            </>
          ) : (
            <p><strong>NITA Office:</strong> {receiver?.nita_office}</p>
          )}
        </div>

        <div className="border-t border-gray-300 pt-4">
          <h2 className="text-md font-semibold text-gray-700 dark:text-gray-300 mb-1">Transaction</h2>
          <p><strong>Country:</strong> {country.toUpperCase()}</p>
          <p><strong>Amount Sent:</strong> {deposit_amount_dinar} Dinar</p>
          {fee_applied && <p className="text-red-600"><strong>Fee:</strong> 5 Dinar</p>}
          <p><strong>Rate:</strong> {conversion_rate}</p>
          <p><strong>Amount Received:</strong> {converted_amount.toLocaleString()} {country === "nigeria" ? "NGN" : "XAF"}</p>
        </div>

        <div className="text-sm text-gray-600 dark:text-gray-400 text-right mt-6">
          <p><strong>Cashier:</strong> {cashier_name}</p>
          <p><strong>Ref ID:</strong> #{id}</p>
        </div>
      </div>
    </div>
  );
}
