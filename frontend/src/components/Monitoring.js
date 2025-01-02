import React from "react";

const Monitoring = () => {
  const [monitoringTokens, setMonitoringTokens] = React.useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/api/monitoring")
      .then((res) => res.json())
      .then((data) => setMonitoringTokens(data));
  }, []);

  return (
    <div className="monitoring">
      <h2>Monitoring Tokens</h2>
      <ul>
        {monitoringTokens.map((token) => (
          <li key={token.id}>
            {token.name} - Status: {token.status}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Monitoring;
