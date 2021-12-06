import { useEffect } from "react";
import L from "leaflet";
import "leaflet-routing-machine/dist/leaflet-routing-machine.css";
import "leaflet-routing-machine";
import "leaflet-control-geocoder/dist/Control.Geocoder.css";
import "leaflet-control-geocoder/dist/Control.Geocoder.js";
import { useMap } from "react-leaflet";
import {useRoutingContext} from '../../context/routing-context';

L.Marker.prototype.options.icon = L.icon({
  iconUrl: "https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png"
});

// icons from https://github.com/pointhi/leaflet-color-markers
const sourceIcon = L.icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

const destinationIcon = L.icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

export default function Routing() {
  const map = useMap();
  // eslint-disable-next-line
  let [routingInfo, setRoutingInfo]= useRoutingContext();
  const geoJSON = routingInfo.geoJSON;
  const sourceCoords = routingInfo.source;
  const destinationCoords = routingInfo.destination;

  console.log(routingInfo);
  // add optimal route onto map
  useEffect(() => {
    if (!map || !geoJSON) return;
    console.log(geoJSON);
    const routingControl = L.geoJSON(geoJSON).addTo(map);
    return () => map.removeControl(routingControl);
  }, [geoJSON, map]);

  // auto-focus map
  useEffect(() => {
    const boundary = [];
    if (sourceCoords) {
      L.marker(sourceCoords, {icon: sourceIcon}).addTo(map);
      boundary.push(sourceCoords)
    }
    if (destinationCoords) {
      L.marker(destinationCoords, {icon: destinationIcon}).addTo(map);
      boundary.push(destinationCoords)
    }
    if (boundary.length !== 0) {
      map.fitBounds(L.latLngBounds([boundary]));
    }
  }, [sourceCoords, destinationCoords, map]);

  return null;
}
