import React, { useState } from 'react';
import Title from './title.js';
import ElevationInput from './elevation-input.js';
import DistanceInput from './distance-input.js';
import Box from '@mui/material/Box';

export default function UserInput() {
  // "maxElevation" user wants maximum elevation, "minElevation" if user wants minimum elevation for path
  const [elevation, setElevation] = useState('maxElevation');
  // Distance percentage from shortest path
  const [distancePercentage, setDistancePercentage] = useState(25);
  
  return (
    <div>
      <Title/>
      <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
        <ElevationInput elevation={elevation} setElevation={setElevation}/>
        <DistanceInput distancePercentage={distancePercentage} setDistancePercentage={setDistancePercentage}/>
      </Box>
    </div>
  );
}

