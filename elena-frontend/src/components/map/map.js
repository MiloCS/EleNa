import { MapContainer, TileLayer } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import Routing from "./routing.js";
import { useRoutingContext } from '../../context/routing-context';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Loading from './loading'

export default function Map() {
  const position = [51.505, -0.09];
  // eslint-disable-next-line
  const [routingInfo, setRoutingInfo]= useRoutingContext();
  const sent = routingInfo.sent;
  const graph = routingInfo.graph;
  const distance = routingInfo.distance;
  const elevation = routingInfo.elevation;

  return (
    <MapContainer center={position} zoom={13} style={{ height: "100vh" }}>
      {!sent ? null :
        <Box sx={{ zIndex: 1000, position: 'absolute', right: 10,  top: 10, backgroundColor: '#becfff', width: '200px', height: '120px', border: '2px solid gray', borderRadius: '10px'}}>
          <Typography variant="h5" align="center" gutterBottom sx={{fontFamily: "Segoe UI",}}>
            Route Info
          </Typography>
          {!graph ? 
            <Loading></Loading>
            :
            <div>
              <Typography variant="body1" align="center" sx={{fontFamily: "Segoe UI", marginLeft: '4px'}}>
                Distance: {distance > 1000 ? `${Math.floor(distance) / 1000} km` : `${Math.floor(distance)} m`}
              </Typography>
              <Typography variant="body1" align="center" sx={{fontFamily: "Segoe UI", marginLeft: '4px'}}>
                Elevation: {Math.floor(elevation)} meters
              </Typography>
            </div>
          }
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

