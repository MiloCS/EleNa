import React from 'react';
import Typography from '@mui/material/Typography';
import ToggleButton from '@mui/material/ToggleButton';
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup';
import LandscapeIcon from '@mui/icons-material/Landscape';
import DirectionsBikeIcon from '@mui/icons-material/DirectionsBike';
import Box from '@mui/material/Box';

export default function ElevationInput({elevation, setElevation}) {
    const control = {
      value: elevation,
      onChange: (event, elevationChoice) => {
        setElevation(elevationChoice);
      },
      exclusive: true,
    };
  const choices = [
    <ToggleButton value="maxElevation" key="maxElevation">
      <Typography variant="h6" component="div" align='center' style={{ marginRight: '3px' }}>
        Max
      </Typography>
      <LandscapeIcon fontSize='large'/>
    </ToggleButton>,
    <ToggleButton value="minElevation" key="minElevation">
      <Typography variant="h6" component="div" align='center' style={{ marginRight: '3px' }}>
        Min 
      </Typography>
      <DirectionsBikeIcon fontSize='large'/>
    </ToggleButton>,
  ];
  return (
    <Box sx={{ marginTop: '30px', display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
      <Typography variant="h4" id="elevation-choice" gutterBottom>
        Max/Min Route Elevation:
      </Typography>
      <ToggleButtonGroup size="large" {...control}>
        {choices}
      </ToggleButtonGroup>
    </Box>
  );
}