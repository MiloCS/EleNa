import React, { useState } from 'react';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import get from '../../get';
import { GEOCODER_API } from '../../Config';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';

export default function DestinationInput({destination, setDestination}) {
  const [geocoderResponse, setGeocoderResponse] = useState({
      data: null,
      loading: true,
      error: null,
  });
  const [loadingText, setLoadingText] = useState('Press enter to search.')
  const handleInputChange = (event) => {
    // user must press enter to send API request
    setGeocoderResponse({
      data: null,
      loading: true,
      error: null,
    })
    setLoadingText("Press enter to search.");
  }

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
    console.log(value)
    setDestination(value);
  };

  return (
    <Box sx={{ marginTop: '30px', width: '80%'  }}>
      <Typography variant="h4" id="distance-percentage-slider" gutterBottom>
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