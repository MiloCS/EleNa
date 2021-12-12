import { useRef, useEffect } from "react";
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip  } from 'recharts';
import { useMap } from "react-leaflet";
import L from "leaflet";
import Box from '@mui/material/Box';
import Loading from './loading';
import Typography from '@mui/material/Typography';
import { useRoutingContext } from '../../context/routing-context';
export default function ElevationGraph({graph, distance, elevation}) {
const map = useMap();
// eslint-disable-next-line
const [routingInfo, setRoutingInfo]= useRoutingContext();
const sent = routingInfo.sent;
const markers = useRef([]);

useEffect(() => {
  if (!graph) {
    markers.current.forEach(marker => {
      map.removeLayer(marker)
    });
    markers.current.length = 0;
  }
}, [map, markers, graph]);
  
const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    markers.current.forEach(marker => {
      map.removeLayer(marker)
    });
    markers.current.length = 0;
    const marker = L.marker([payload[0].payload.y, payload[0].payload.x]).bindPopup(`Elevation: ${payload[0].value} m`);
    marker.elevationMarker = true;
    map.addLayer(marker);
    markers.current.push(marker);
    return (
      <Box sx={{ zIndex: 1001, backgroundColor: 'white', padding: '5px', border: '2px solid gray', borderRadius: '10px'}}>
        <Typography variant="subtitle1">{`Distance from Source: ${label} m`}</Typography>
        <Typography variant="subtitle2">{`Elevation: ${payload[0].value} m`}</Typography>
      </Box>
    );
  }
  return null;
};
  return (
    <div>  
      {!sent ? null :
        <Box sx={{ zIndex: 1000, position: 'absolute', right: 10,  bottom: 15, backgroundColor: '#becfff', width: '525px', height: '250px', border: '2px solid gray', borderRadius: '10px'}}>
          {!graph ? 
          <div style={{ marginTop: '75px' }}>
            <Loading />
          </div> :
          <div>
            <Typography variant="h6" align="center">Elevation change (in meters)</Typography>
            <LineChart width={500} height={200} data={graph.map((obj, index) => {
                return {...obj, dist_from_start: Math.floor(obj.dist_from_start)}
              })}>
              <CartesianGrid stroke="#ccc" />
              <XAxis dataKey="dist_from_start" label={{ value: "Distance from Source (in meters)", position: "insideBottom", dy: 5}}/>
              <YAxis label={{ value: "Elevation (in meters)", position: "center", angle: -90, dx: -10}}/>
              <Tooltip content={<CustomTooltip />} />
              <Line activeDot={{ stroke: '#white', strokeWidth: 4, r: 8, fill: '#ff5f4a'}} dot={{ stroke: '#44c0ff', strokeWidth: 4, r: 2, fill: 'blue'}}  type="monotone" dataKey="elevation" stroke="#8884d8" isElevationActive={false}/>
            </LineChart>
          </div>
          }
        </Box>
      }
    </div>
  )
}