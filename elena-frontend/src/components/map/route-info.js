import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Loading from './loading'
import { useRoutingContext } from '../../context/routing-context';

export default function RouteInfo({graph, distance, elevation}) {
  // eslint-disable-next-line
  const [routingInfo, setRoutingInfo]= useRoutingContext();
  const sent = routingInfo.sent;

  return (
    <div>  
      {!sent ? null :
        <Box sx={{ zIndex: 1000, position: 'absolute', right: 10,  top: 10, backgroundColor: '#becfff', width: '200px', height: '120px', border: '2px solid gray', borderRadius: '10px'}}>
          <Typography variant="h5" align="center" gutterBottom sx={{fontFamily: "Segoe UI",}}>
            Route Info
          </Typography>
          {!graph ? 
            <Loading />
            :
            <div>
              <Typography variant="body1" align="center" sx={{fontFamily: "Segoe UI", marginLeft: '4px'}}>
                Distance: {distance > 1000 ? `${Math.floor(distance) / 1000} km` : `${Math.floor(distance)} m`}
              </Typography>
              <Typography variant="body1" align="center" sx={{fontFamily: "Segoe UI", marginLeft: '4px'}}>
                Elevation: {Math.floor(elevation)} meters
              </Typography>
            </div>
          }
        </Box>
      }
    </div>
  )
}