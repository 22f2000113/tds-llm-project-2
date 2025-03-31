import requests
import json
from bs4 import BeautifulSoup

def get_command(question):
    location_id=get_location_id('Kuwait')
    print('location_id',location_id)
    return_value=get_weather_forecast(location_id)
    print("get_weather_forecast", return_value)
    return return_value


def get_weather_forecast(location_id):
    """Fetch multi-day weather forecast from BBC and return formatted JSON."""
    url = f"https://weather-broker-cdn.api.bbci.co.uk/en/forecast/aggregated/{location_id}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # DEBUG: Print keys to understand structure
        print("Top-level keys in response:", data.keys())

        forecasts = data.get("forecasts", [])
        #print("Forecasts preview:", forecasts[:1])  # Show 1st item for structure

        # Extract from summary.report (which has daily overview)
        weather_dict = {
            forecast["summary"]["report"]["localDate"]: forecast["summary"]["report"][
                "enhancedWeatherDescription"
            ]
            for forecast in forecasts
            if "summary" in forecast and "report" in forecast["summary"]
        }
        print('weather_dict',weather_dict)
        return weather_dict

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def get_location_id(city_name):
    """Fetch locationId from BBC Locator API."""
    url = (
        "https://locator-service.api.bbci.co.uk/locations"
        "?api_key=AGbFAKx58hyjQScCXIYrxuEwJh2W2cmv"
        "&stack=aws"
        "&locale=en"
        "&filter=international"
        "&place-types=settlement,airport,district"
        "&order=importance"
        f"&s={city_name}"
        "&format=json"
    )

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    print("get_location_id", data)
    locations = data.get("response", {}).get("locations", [])

    if not locations:
        raise ValueError(f"No locationId found for city: {city_name}")

    # Return the first matching locationId
    return locations[0]["id"]

if __name__ == "__main__":
    location_id_1=get_location_id("Kuwait")
    get_weather_forecast(location_id_1)
