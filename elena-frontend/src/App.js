import Map from "./components/map/map";
import UserInput from "./components/user-input/user-input"
import Box from '@mui/material/Box';

export default function App() {
  return (
    <div className="App">
      <Box
        sx={{
          display: 'grid',
          bgcolor: 'white',
          gridAutoColumns: '1fr',
        }}
      >
        <Box>
          <UserInput/>
        </Box>
        <Box sx={{ gridColumn: '2 / 4' }}>
          <Map/>
        </Box>
      </Box>
    </div>
  );
}


