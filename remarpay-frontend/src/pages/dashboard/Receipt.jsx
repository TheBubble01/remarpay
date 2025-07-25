import { useParams } from "react-router-dom";
import { useEffect, useRef, useState } from "react";
import logo from "../../assets/logo.jpg";
import { toPng } from "html-to-image";

export default function Receipt() {
  const { id } = useParams();
  const [receipt, setReceipt] = useState(null);
  const access = localStorage.getItem("access");
  const receiptRef = useRef(null);

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/api/payments/cashier/receipt/${id}/`, {
      headers: { Authorization: `Bearer ${access}` },
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
        title: "RemarX Receipt",
        text: "Here’s the receipt from RemarX",
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
      {/* Action Buttons */}
      <div className="flex justify-center gap-4">
        <button
          onClick={handleDownload}
          className="bg-[#033a44] hover:bg-green-950 text-[#e6be8a] border border-[#D4AF37] px-4 py-2 rounded text-sm"
        >
          Download Receipt
        </button>
        <button
          onClick={handleShareWhatsApp}
          className="bg-[#033a44] hover:bg-green-950 text-[#e6be8a] px-4 py-2 rounded text-sm"
        >
          Share via WhatsApp
        </button>
        {/* <a
          href="/dashboard/new-request"
          className="bg-white hover:bg-gray-100 text-[#014421] border border-[#014421] px-4 py-2 rounded text-sm text-center"
          style={{ textDecoration: "none" }}
        >
          + New Payment
        </a> */}
      </div>

      {/* Receipt Card */}
      <div
        ref={receiptRef}
        className="rounded-xl shadow-lg p-6 space-y-6 text-sm"
        style={{
          backgroundColor: "#041c05ff",
          color: "#e6be8a",
          fontFamily: "sans-serif",
        }}
      >
        {/* Logo + Heading */}
        <div className="flex flex-col items-center text-center">
          <img src={logo} alt="RemarPay Logo" className="h-14 mb-2" />
          <h1 className="text-xl font-bold" style={{color: "#ffffff"}}>Transaction Receipt</h1>
          <p className="text-xs text-[#ffffff] opacity-80">{created_at}</p>
        </div>

        {/* Depositor Info */}
        <div className="border-t border-[#ffffff] pt-4">
          <h2 className="text-base font-semibold mb-1">Depositor</h2>
          <p><span className="font-medium">Name:</span> {depositor_name}</p>
          <p><span className="font-medium">Phone:</span> {depositor_phone}</p>
        </div>

        {/* Receiver Info */}
        <div className="border-t border-[#ffffff] pt-4">
          <h2 className="text-base font-semibold mb-1">Receiver</h2>
          <p><span className="font-medium">Name:</span> {receiver?.name || bank_details?.account_name}</p>
          <p><span className="font-medium">Phone:</span> {receiver?.phone || depositor_phone}</p>
          {country === "nigeria" ? (
            <>
              <p><span className="font-medium">Bank:</span> {bank_details?.bank_name}</p>
              <p><span className="font-medium">Acct No:</span> {bank_details?.account_number}</p>
            </>
          ) : (
            <p><span className="font-medium">NITA Office:</span> {receiver?.nita_office}</p>
          )}
        </div>

        {/* Transaction Info */}
        <div className="border-t border-[#fffff] pt-4">
          <h2 className="text-base font-semibold mb-1">Transaction</h2>
          <p><span className="font-medium">Country:</span> {country.toUpperCase()}</p>
          <p><span className="font-medium">Amount Sent:</span> {deposit_amount_dinar} Dinar</p>
          {fee_applied && (
            <p className="text-red-300">
              <span className="font-medium">Fee:</span> 5 Dinar
            </p>
          )}
          <p><span className="font-medium">Rate:</span> {conversion_rate}</p>
          <p>
            <span className="font-medium">Amount Received:</span>{" "}
            {converted_amount.toLocaleString()} {country === "nigeria" ? "NGN" : "XAF"}
          </p>
        </div>

        {/* Footer Info */}
        <div className="text-right text-xs opacity-90 pt-6" style={{ color: "#ffffff" }}>
          <p><span className="font-medium">Cashier:</span> {cashier_name}</p>
          <p><span className="font-medium">Ref ID:</span> #{id}</p>
        </div>
      </div>
    </div>
  );
}
