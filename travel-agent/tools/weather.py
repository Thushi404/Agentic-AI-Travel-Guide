import requests          # used to send HTTP Get requests to the Open-Meteo API.


WEATHER_CODES = {                 # open metro returns a weather code  and it converts the code to a human readable format.
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    95: "Thunderstorm",
}


def geocode_city(city: str) -> dict:        # converta a city name to latitude and longitude using the Open-Meteo Geocoding API.
    url = "https://geocoding-api.open-meteo.com/v1/search"         

    try:
        response = requests.get(
            url,
            params={
                "name": city,
                "count": 1,
                "language": "en",
                "format": "json",
            },
            timeout=15,
        )
        response.raise_for_status()   # raises an exception if the request was unsuccessful.
        data = response.json()         # converts the response to a python dictionary.

        results = data.get("results", [])           # gets the results from the response, if there are no results it returns an empty list.
        if not results:
            return {"error": f"Could not find location: {city}"}

        place = results[0]                   # gets the first result from the results list.
        return {
            "name": place.get("name"),
            "country": place.get("country"),
            "latitude": place.get("latitude"),
            "longitude": place.get("longitude"),
            "timezone": place.get("timezone", "auto"),
        }
 
    except requests.RequestException as error:                        
        return {"error": f"Geocoding failed: {str(error)}"}


def get_weather(location: str, day: str = "today") -> dict:                # gets the weather for a given location and day and this is the main function.
    place = geocode_city(location)

    if "error" in place:
        return place

    day_index = 1 if day.lower() == "tomorrow" else 0

    url = "https://api.open-meteo.com/v1/forecast"

    try:
        response = requests.get(
            url,
            params={                           # these tell the API which location to grt weather for.
                "latitude": place["latitude"],
                "longitude": place["longitude"],
                "current": "temperature_2m,precipitation,rain,weather_code,wind_speed_10m",
                "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum",
                "timezone": "auto",
                "forecast_days": 3,
            },
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()               # converts the response to a python dictionary.

        daily = data.get("daily", {})         # gets the daily weather data from the response.
        current = data.get("current", {})     # gets the current weather data from the response.

        if not daily.get("time"):
            return {"error": "Weather data is not available."}

        weather_code = daily["weather_code"][day_index]          # gets the weather code for the requested day.
        rain_sum = daily["precipitation_sum"][day_index]         # gets the total precipitation for the requested day.

        return {                                                      # returns the final weather report.
            "location": f"{place['name']}, {place['country']}",     
            "requested_day": day,
            "date": daily["time"][day_index],
            "condition": WEATHER_CODES.get(weather_code, "Unknown weather condition"),
            "max_temperature_c": daily["temperature_2m_max"][day_index],
            "min_temperature_c": daily["temperature_2m_min"][day_index],
            "precipitation_mm": rain_sum,
            "umbrella_needed": rain_sum > 0,
            "current_temperature_c": current.get("temperature_2m"),
            "current_wind_speed_kmh": current.get("wind_speed_10m"),
        }

    except requests.RequestException as error:                   # error handling.
        return {"error": f"Weather API failed: {str(error)}"}