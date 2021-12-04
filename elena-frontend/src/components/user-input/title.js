import React from 'react';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

export default function Title() {
  return (
    <Box sx={{ display: 'grid', gridTemplateRows: 'repeat(2)' }}>
      <Typography sx={{fontFamily: "Segoe UI"}} variant="h2" component="div" align='center'>
        EleNa
      </Typography>
      <Typography sx={{fontFamily: "Segoe UI"}} variant="h5" gutterBottom component="div" align='center'>
        Elevation-based Navigation
      </Typography>
    </Box>
  );
}
