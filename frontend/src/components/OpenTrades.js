import React, { useEffect, useState } from "react";

const OpenTrades = () => {
  const [openTrades, setOpenTrades] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/api/open-trades")
      .then((res) => res.json())
      .then((data) => setOpenTrades(data));
  }, []);

  return (
    <div className="open-trades">
      <h2>Open Trades</h2>
      <ul>
        {openTrades.map((trade) => (
          <li key={trade.id}>
            {trade.tokenName} - Quantity: {trade.quantity} - Status: {trade.status}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default OpenTrades;
