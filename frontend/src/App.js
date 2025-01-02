import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import TokenList from "./components/TokenList";
import Monitoring from "./components/Monitoring";
import OpenTrades from "./components/OpenTrades";
import "./styles/global.css"; // Reference global styles

const App = () => {
  return (
    <Router>
      <div className="app-container">
        <nav className="navbar">
          <Link to="/">Dashboard</Link>
          <Link to="/monitoring">Monitoring</Link>
          <Link to="/trades">Open Trades</Link>
        </nav>
        <Routes>
          <Route path="/" element={<TokenList />} />
          <Route path="/monitoring" element={<Monitoring />} />
          <Route path="/trades" element={<OpenTrades />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
