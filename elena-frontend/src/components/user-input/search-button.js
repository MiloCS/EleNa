import React from 'react';
import Button from '@mui/material/Button';


export default function Title({algorithm}) {
  return (
    <Button variant="contained" onClick={algorithm}>Find Route</Button>
  );
}
