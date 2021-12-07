import React, { useState } from 'react';
import Title from './title.js';
import ElevationInput from './elevation-input.js';
import DistanceInput from './distance-input.js';
import Box from '@mui/material/Box';
import SourceInput from './source-input';
import DestinationInput from './destination-input';
import SearchButton from './search-button';
import { ROUTING_API, ROUTING_REQUEST_BODY } from '../../Config';
import post from '../../http-request-helpers/post';
import {useRoutingContext} from '../../context/routing-context';


export default function UserInput() {
  // "max" user wants maximum elevation, "min" if user wants minimum elevation for path
  const [elevation, setElevation] = useState('max');
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
      console.log(resp.data)
      setRoutingInfo((prev) => ({
        ...prev,
        graph: resp.data
      }))
    }
    function address(){
      //
      let address = ''
      if (source.address.city) {
        address = `${source.address.city},`
      } else if (source.address.town) {
        address = `${source.address.town},`
      } else if (source.address.municipality) {
        address = `${source.address.municipality},`
      } else if (source.address.village) {
        address = `${source.address.village},`
      }
      if (source.address.state) {
        address += ` ${source.address.state}`
      } else if (source.address.county) {
        address += ` ${source.address.county}`
      } else if (source.address.region) {
        address += ` ${source.address.region}`
      } else if (source.address.state_district) {
        address += ` ${source.address.state_district}`
      }
      return address;
    }
    post(setOverpassAPIResponse, ROUTING_API, onError, onSuccess, ROUTING_REQUEST_BODY(source.lat, source.lon, destination.lat, destination.lon, address(), elevation, distancePercentage ))
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

