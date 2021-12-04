import { createContext, useContext,useState } from 'react';

const RoutingContext = createContext();
function RoutingContextProvider({children}) {
  const routing_info = useState({
    geoJson: null
  });
  return <RoutingContext.Provider value={routing_info}>{children}</RoutingContext.Provider>;
};
function useRoutingContext() {
  return useContext(RoutingContext);
}

export {RoutingContextProvider, useRoutingContext}