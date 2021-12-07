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
      if (elevationChoice !== null) {
        setElevation(elevationChoice);
      }
    },
    exclusive: true,
  };

  const choices = [
    <ToggleButton size="large" value="max" key="max">
      <Typography sx={{fontFamily: "Segoe UI"}} variant="h7" component="div" align='center' style={{ marginRight: '3px' }}>
        Max
      </Typography>
      <LandscapeIcon fontSize='medium'/>
    </ToggleButton>,
    <ToggleButton size="large" value="min" key="min">
      <Typography sx={{fontFamily: "Segoe UI"}} variant="h7" component="div" align='center' style={{ marginRight: '3px' }}>
        Min 
      </Typography>
      <DirectionsBikeIcon fontSize='medium'/>
    </ToggleButton>,
  ];

  return (
    <Box sx={{ marginTop: '30px', display: 'flex', flexDirection: 'column', alignItems: 'left'}}>
      <Typography sx={{fontFamily: "Segoe UI"}} variant="h6" id="elevation-choice" gutterBottom>
        Max/Min Route Elevation:
      </Typography>
      <ToggleButtonGroup color="secondary" size="large" {...control}>
        {choices}
      </ToggleButtonGroup>
    </Box>
  );
}