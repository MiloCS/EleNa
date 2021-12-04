export const GEOCODER_API = 'https://nominatim.openstreetmap.org/search?'
export const OVERPASS_API = 'http://overpass-api.de/api/interpreter'
export function OVERPASS_REQUEST_BODY(radius, longitude1, latitude1, longitude2, latitude2) {
  return `[out:json];way[highway](around:${radius},${longitude1},${latitude1},${longitude2},${latitude2}); (._;>;);out meta;`
}