import React from 'react';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Slider from '@mui/material/Slider';
import Grid from '@mui/material/Grid';
import Input from '@mui/material/Input';

export default function DistanceInput({distancePercentage, setDistancePercentage}) {
  function valuetext(value) {
    return `${value}%`;
  }

  const handleSliderChange = (event, newValue) => {
    setDistancePercentage(newValue);
  };

  const handleInputChange = (event) => {
    setDistancePercentage(event.target.value === '' ? '' : Number(event.target.value));
  };

  const handleBlur = () => {
    if (distancePercentage < 0) {
      setDistancePercentage(0);
    } else if (distancePercentage > 100) {
      setDistancePercentage(100);
    }
  };

  return (
    <Box sx={{ marginTop: '30px' }}>
      <Typography sx={{fontFamily: "Segoe UI"}} variant="h6" id="distance-percentage-slider" gutterBottom>
        Percentage of Shortest Path:
      </Typography>
       <Grid container spacing={2} alignItems="center">
        <Grid item xs>
          <Slider sx={{
              color: 'white',
              '& .MuiSlider-thumb': {
                borderRadius: '1px',
              }
            }}
            
            
            aria-label="x% of the shortest path"
            value={distancePercentage}
            onChange={handleSliderChange}
            getAriaLabel={valuetext}
            getAriaValueText={valuetext}
            valueLabelFormat={valuetext}
            valueLabelDisplay="auto"
            size="medium"
            step={1}
            min={100}
            max={200}
          />
        </Grid>
        <Grid item style={{ display: 'inherit'}}>
          <Input
            style={{ width: '50px', color: 'black'}}
            value={distancePercentage}
            onChange={handleInputChange}
            onBlur={handleBlur}
            inputProps={{
              step: 1,
              min: 100,
              max: 200,
              type: 'number',
              'aria-labelledby': 'input-slider',
            }}
          />
          <Typography sx={{fontFamily: "Segoe UI"}} variant="h6" id="distance-percentage-slider">
            % 
          </Typography>
        </Grid>
      </Grid>
    </Box>
  );
}