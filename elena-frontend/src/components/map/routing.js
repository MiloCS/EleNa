import { useEffect, useContext } from "react";
import L from "leaflet";
import "leaflet-routing-machine/dist/leaflet-routing-machine.css";
import "leaflet-routing-machine";
import "leaflet-control-geocoder/dist/Control.Geocoder.css";
import "leaflet-control-geocoder/dist/Control.Geocoder.js";
import { useMap } from "react-leaflet";
import {useRoutingContext} from '../../context/routing-context';
// Code from https://codesandbox.io/s/lroutingcontrol-on-react-leaflet-v3-with-hooks-vk6es?file=/package.json:407-428 
L.Marker.prototype.options.icon = L.icon({
  iconUrl: "https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png"
});

export default function Routing() {
  const map = useMap();
  let [routingInfo, setRoutingInfo]= useRoutingContext();
  const geoJSON = routingInfo.geoJSON;
  console.log(routingInfo);
  useEffect(() => {
    if (!map || !geoJSON) return;

    // const routingControl = L.Routing.control({
    //   waypoints: [L.latLng(57.74, 11.94), L.latLng(57.6792, 11.949)],
    //   routeWhileDragging: true,
    // })
    // .on('routesfound', function(e) {
    //     var routes = e.routes;
    //     console.log(routes);
    // })
    // .addTo(map);
    console.log(geoJSON);
    const routingControl = L.geoJSON(geoJSON).addTo(map);

    return () => map.removeControl(routingControl);
  }, [geoJSON, map]);

  return null;
}
