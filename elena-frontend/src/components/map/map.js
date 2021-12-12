import { MapContainer, TileLayer } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import Routing from "./routing.js";
import { useRoutingContext } from '../../context/routing-context';
import RouteInfo from './route-info';
import ElevationGraph from './elevation-graph';

export default function Map() {
  const position = [51.505, -0.09];
  // eslint-disable-next-line
  const [routingInfo, setRoutingInfo]= useRoutingContext();
  const graph = routingInfo.graph;
  const distance = routingInfo.distance;
  const elevation = routingInfo.elevation;

  return (
    <MapContainer center={position} zoom={13} style={{ height: "100vh" }}>
      <div> 
        <RouteInfo graph={graph} distance={distance} elevation={elevation}/>
        <ElevationGraph graph={graph} />
      </div>
      <TileLayer
        attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <Routing />
    </MapContainer>
  );
}

