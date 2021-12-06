import React, { useState } from 'react';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import get from '../../http-request-helpers/get';
import { GEOCODER_API, REVERSE_GEOCODER_API } from '../../Config';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import {useRoutingContext} from '../../context/routing-context';

export default function DestinationInput({destination, setDestination}) {
  const [geocoderResponse, setGeocoderResponse] = useState({
    data: null,
    loading: true,
    error: null,
  });
  // eslint-disable-next-line
  const [reverseGeocoderResponse, setReverseGeocoderResponse] = useState({
    data: null,
    loading: true,
    error: null,
  });
  const [loadingText, setLoadingText] = useState('Press enter to search.')
  // eslint-disable-next-line
  const [routingInfo, setRoutingInfo] = useRoutingContext();
  const handleInputChange = (event) => {
    // user must press enter to send API request
    setGeocoderResponse({
      data: null,
      loading: true,
      error: null,
    })
    setLoadingText("Press enter to search.");
  }

  // search for place using geocoder after user selects enter
  const handleEnter = (event) => {
    const onError = () => {

    }
    const onSuccess = (resp) => {

    }
    
    if (event.target.value.trim() !== '') {
      setLoadingText("Loading results");
      const query = `q=${event.target.value}&format=jsonv2`
      get(setGeocoderResponse, GEOCODER_API + query, onError, onSuccess)
    }
  };


  const handleUserSelect= (event, value, reason) => {
    setDestination(value);
    setRoutingInfo((prev) => ({
      ...prev,
      destination: [value.lat, value.lon]
    }))
    const onError = () => {

    }
    const onSuccess = (resp) => {
      setDestination({
        ...value,
        ...resp.data
        }
      );
      console.log(value)
      console.log(resp.data)
      console.log({
        ...value,
        ...resp.data
        })
    }
    // search for address name to store
    get(setReverseGeocoderResponse, REVERSE_GEOCODER_API(value.lat, value.lon), onError, onSuccess)
  };

  return (
    <Box sx={{ marginTop: '10px', width: '80%'  }}>
      <Typography sx={{fontFamily: "Segoe UI"}} variant="h6" id="distance-percentage-slider" gutterBottom>
        Destination:
      </Typography>
        <Autocomplete
          id="destination-search"
          disableClearable
          onChange={handleUserSelect}
          options={geocoderResponse.data ? geocoderResponse.data : []}
          loadingText={loadingText}
          loading={geocoderResponse.loading}
          noOptionsText="No results found."
          getOptionLabel={option => option.display_name}
          filterOptions={(options) => options}
          renderInput={(params) => (
            <TextField
              {...params}
              label="Destination"
              value={destination}
              onChange={handleInputChange}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                    handleEnter(e)
                }
              }}
              InputProps={{
                ...params.InputProps,
                type: 'search',
              }}
            />
          )}
        />
    </Box>
  );
}