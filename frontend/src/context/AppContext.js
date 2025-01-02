import React, { createContext, useContext, useState } from "react";

const AppContext = createContext();

export const AppProvider = ({ children }) => {
  const [tokens, setTokens] = useState([]);

  return (
    <AppContext.Provider value={{ tokens, setTokens }}>
      {children}
    </AppContext.Provider>
  );
};

export const useAppContext = () => useContext(AppContext);
