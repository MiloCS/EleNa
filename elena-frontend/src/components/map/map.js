import { MapContainer, TileLayer } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import Routing from "./routing.js";
import { useRoutingContext } from '../../context/routing-context';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';

export default function Map() {
  const position = [51.505, -0.09];
  // eslint-disable-next-line
  const [routingInfo, setRoutingInfo]= useRoutingContext();
  const graph = routingInfo.graph;
  return (
    <MapContainer center={position} zoom={13} style={{ height: "100vh" }}>
      {!graph ? null :
        <Box sx={{ zIndex: 1000, position: 'absolute', right: 0, backgroundColor: 'white', width: '250px', height: '125px', border: '3px solid black'}}>
          <Typography variant="h5" align="center" gutterBottom>
            Route Statistics
          </Typography>
          <Typography variant="h6" align="left" sx={{marginLeft: '4px'}}>
            Distance:
          </Typography>
          <Typography variant="h6" align="left" sx={{marginLeft: '4px'}}>
            Elevation:
          </Typography>
        </Box>
      }
      <TileLayer
        attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <Routing />
    </MapContainer>
  );
}

