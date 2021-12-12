export const GEOCODER_API = 'https://nominatim.openstreetmap.org/search?'
export const OVERPASS_API = 'https://overpass-api.de/api/interpreter'
console.log(process.env.REACT_APP_BACKEND)
export const ROUTING_API = process.env.REACT_APP_BACKEND ? process.env.REACT_APP_BACKEND :'http://localhost:8080/route'
export function REVERSE_GEOCODER_API(latitude, longitude) {
  return `https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${latitude}&lon=${longitude}&zoom=18&addressdetails=1`
}
export function OVERPASS_REQUEST_BODY(radius, longitude1, latitude1, longitude2, latitude2) {
  return `[out:json];way[highway](around:${radius},${longitude1},${latitude1},${longitude2},${latitude2}); (._;>;);out meta;`
}
export function ROUTING_REQUEST_BODY(sourceLat, sourceLon, destinationLat, destinationLon, address, elevationChoice, percent) {
  return {
    start: [sourceLat, sourceLon],
    end: [destinationLat, destinationLon],
    place: address,
    type: elevationChoice,
    percent: percent
  };
}