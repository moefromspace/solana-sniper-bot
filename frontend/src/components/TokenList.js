import React, { useState, useEffect } from "react";

const TokenList = () => {
  const [tokens, setTokens] = useState([]);

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/ws/tokens");

    ws.onmessage = (event) => {
      const newToken = JSON.parse(event.data);
      setTokens((prevTokens) => [newToken, ...prevTokens]);
    };

    ws.onclose = () => console.log("WebSocket closed");
    return () => ws.close();
  }, []);

  return (
    <div className="token-list">
      <h2>New Tokens</h2>
      <ul>
        {tokens.map((token, index) => (
          <li key={index}>{token.name} - {token.symbol}</li>
        ))}
      </ul>
    </div>
  );
};

export default TokenList;
