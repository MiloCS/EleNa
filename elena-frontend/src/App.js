import Map from "./components/map/map";
import UserInput from "./components/user-input/user-input"
import Box from '@mui/material/Box';
import {RoutingContextProvider} from './context/routing-context';

export default function App() {
  return (
    <div className="App">
      <Box
        sx={{
          display: 'grid',
          bgcolor: '#becfff',
          gridAutoColumns: '1fr'
        }}
      >
        <RoutingContextProvider>
          <Box>
            <UserInput/>
          </Box>
          <Box sx={{ gridColumn: '2 / 4' }}>
            <Map/>
          </Box>
        </RoutingContextProvider>
      </Box>
    </div>
  );
}


