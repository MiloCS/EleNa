import React from 'react';
import Button from '@mui/material/Button';
import RouteIcon from '@mui/icons-material/Route';
import DirectionsIcon from '@mui/icons-material/Directions';

export default function Title({algorithm}) {
  return (
    <Button sx={{width: '50%' }} variant="contained" size="large" startIcon={<RouteIcon />} endIcon={<DirectionsIcon />}onClick={algorithm}>
      Find Route
    </Button>
  );
}
