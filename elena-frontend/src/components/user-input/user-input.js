import React, { useState } from 'react';
import Title from './title.js';
import ElevationInput from './elevation-input.js';
import DistanceInput from './distance-input.js';
import Box from '@mui/material/Box';
import SourceInput from './source-input';
import DestinationInput from './destination-input';
import SearchButton from './search-button';
import { OVERPASS_API, OVERPASS_REQUEST_BODY } from '../../Config';
import post from '../../http-request-helpers/post';
import graphFromOsm from 'graph-from-osm';
import {useRoutingContext} from '../../context/routing-context';


export default function UserInput() {
  // "maxElevation" user wants maximum elevation, "minElevation" if user wants minimum elevation for path
  const [elevation, setElevation] = useState('maxElevation');
  // Distance percentage from shortest path
  const [distancePercentage, setDistancePercentage] = useState(125);
  const [source, setSource] = useState('');
  const [destination, setDestination] = useState('');
  // finds nodes and ways
  // eslint-disable-next-line
  const [overpassAPIResponse, setOverpassAPIResponse] = useState({
      data: null,
      loading: true,
      error: null,
  });
  // eslint-disable-next-line
  const [routingInfo, setRoutingInfo] = useRoutingContext();

  const algorithm = () => {

    const onError = (err) => {
      console.log(err);
    }
    const onSuccess = (resp) => {
      const graph = graphFromOsm.osmDataToGraph(resp.data);
      setRoutingInfo((prev) => ({
        ...prev,
        geoJSON: graph
      }))
    }

    post(setOverpassAPIResponse, OVERPASS_API, onError, onSuccess, OVERPASS_REQUEST_BODY(50, source.lat, source.lon, destination.lat, destination.lon))
  }

  return (
    <div>
      <Title/>
      <hr></hr>
      <Box align="left" sx={{ padding: '2em', paddingTop: '0', display: 'flex', flexDirection: 'column', alignItems: 'left'}}>
        <SourceInput source={source} setSource={setSource} />
        <DestinationInput destination={destination} setDestination={setDestination} />
        <ElevationInput elevation={elevation} setElevation={setElevation}/>
        <DistanceInput distancePercentage={distancePercentage} setDistancePercentage={setDistancePercentage}/>
      
      </Box>
      <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
        <SearchButton algorithm={algorithm} />
      </Box>
    </div>
  );
}

