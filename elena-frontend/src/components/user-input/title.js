import React from 'react';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

export default function Title() {
  return (
    <Box sx={{ display: 'grid', gridTemplateRows: 'repeat(2)' }}>
      <Typography variant="h2" component="div" align='center'>
        EleNa
      </Typography>
      <Typography variant="h5" gutterBottom component="div" align='center'>
        Elevation-based Navigation
      </Typography>
    </Box>
  );
}
