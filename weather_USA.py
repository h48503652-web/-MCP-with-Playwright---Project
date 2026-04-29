from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather-USA")

NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"


async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {"User-Agent": USER_AGENT, "Accept": "application/geo+json"}
    # Netfree SSL
    transport = httpx.AsyncHTTPTransport(verify=False)
    
    async with httpx.AsyncClient(transport=transport) as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}


def format_alert(feature: dict) -> str:
    """Format an alert feature into a readbale string"""
    props = feature["properties"]
    return f"""
Event: {props.get("event", "Unknown")}
Area: {props.get("areaDesc","Unknown")}
Severity:{props.get("severity","Unknown")}
Description:{props.get("description", "No description available")}
Instructions:{props.get("instructions", "No specific instructions provided")}
"""


@mcp.tool()
async def get_alerts_in_USA(state: str) -> str:
    """Get weather alerts for a USA state

    Args:
        state: Two-letter USA state code (e.g. CA, NY)
    """
    
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)
    
    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."
    
    if not data["features"]:
        return "No Active alerts for this state."
    
    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)

@mcp.tool()
async def get_forecast_in_USA(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location in USA.
    
    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)
    
    if not points_data:
        return "Unable to fetch forecast data for this location " + points_url
    
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)
    
    if not forecast_data:
        return "Unable to fetch detailed forecast"
    
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:
        forecast = f"""
        {period["name"]}:
        Temperture:{period["temperature"]}°{period["temperatureUnit"]}
        Wind: {period["windSpeed"]}  {period["windDirection"]}
        Forecast:{period["detailedForecast"]}
        """
        forecasts.append(forecast)
        
    return "\n---\n".join(forecasts)

def main():
    mcp.run(transport="stdio")
    
if __name__ == "__main__":
    main()