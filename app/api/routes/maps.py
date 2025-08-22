from fastapi import APIRouter, HTTPException
import httpx
from app.config import settings

router = APIRouter()


@router.get("/geocode")
async def geocode_address(address: str):
    """Geocode address using Yandex Maps API"""
    
    if not settings.yandex_maps_api_key:
        raise HTTPException(status_code=500, detail="Yandex Maps API key not configured")
    
    url = "https://geocode-maps.yandex.ru/1.x/"
    params = {
        "apikey": settings.yandex_maps_api_key,
        "geocode": address,
        "format": "json",
        "results": 1
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Extract coordinates from response
            if "response" in data and "GeoObjectCollection" in data["response"]:
                geo_objects = data["response"]["GeoObjectCollection"]["featureMember"]
                if geo_objects:
                    pos = geo_objects[0]["GeoObject"]["Point"]["pos"]
                    lon, lat = map(float, pos.split())
                    return {
                        "latitude": lat,
                        "longitude": lon,
                        "address": address
                    }
            
            raise HTTPException(status_code=404, detail="Address not found")
            
        except httpx.HTTPError:
            raise HTTPException(status_code=500, detail="Geocoding service unavailable")


@router.get("/static-map")
async def get_static_map(lat: float, lon: float, zoom: int = 15, width: int = 600, height: int = 400):
    """Generate static map URL using Yandex Maps API"""
    
    if not settings.yandex_maps_api_key:
        raise HTTPException(status_code=500, detail="Yandex Maps API key not configured")
    
    # Yandex Static Maps API URL
    url = f"https://static-maps.yandex.ru/1.x/?apikey={settings.yandex_maps_api_key}&l=map&size={width},{height}&z={zoom}&pt={lon},{lat},pm2rdm"
    
    return {
        "map_url": url,
        "latitude": lat,
        "longitude": lon,
        "zoom": zoom
    }


@router.get("/route")
async def get_route(start_lat: float, start_lon: float, end_lat: float, end_lon: float):
    """Get route between two points using Yandex Maps API"""
    
    if not settings.yandex_maps_api_key:
        raise HTTPException(status_code=500, detail="Yandex Maps API key not configured")
    
    url = "https://api.routing.yandex.net/v2/route"
    params = {
        "apikey": settings.yandex_maps_api_key,
        "waypoints": f"{start_lon},{start_lat}|{end_lon},{end_lat}",
        "mode": "driving"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if "route" in data:
                route = data["route"]
                return {
                    "distance": route.get("distance", {}).get("value", 0),
                    "duration": route.get("duration", {}).get("value", 0),
                    "start_point": {"lat": start_lat, "lon": start_lon},
                    "end_point": {"lat": end_lat, "lon": end_lon}
                }
            
            raise HTTPException(status_code=404, detail="Route not found")
            
        except httpx.HTTPError:
            raise HTTPException(status_code=500, detail="Routing service unavailable")
