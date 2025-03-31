import requests

def get_command(question):
    print(question)
    city="Pune"
    country="India"
    bounding_box =get_bounding_box(city,country)
    # Extract bounding box values (min lat, max lat, min lon, max lon)
    max_latitude=get_max_latitude(bounding_box)
    max_longitude = get_max_longitude(bounding_box)
    return max_latitude, max_longitude

def get_max_latitude(bounding_box):
    max_latitude = float(bounding_box[1])  # Maximum latitude is the second value
    return max_latitude


def get_max_longitude(bounding_box):
    max_longitude = float(bounding_box[3])  # Maximum longitude is the 4th value
    return max_longitude


# Extract bounding box values (min lat, max lat, min lon, max lon)
def get_bounding_box(city, country):
    """Fetches the maximum latitude of the bounding box for a given city and country using Nominatim API."""

    base_url = "https://nominatim.openstreetmap.org/search"
    headers = {
        "User-Agent": "MyGeocoderApp/1.0 (your_email@example.com)"  # Replace with your email
    }

    params = {
        "q": f"{city}, {country}",
        "format": "json",
        "limit": 1,
        "addressdetails": 1,
        "extratags": 1,
        "bounded": 1,
    }

    try:
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()  # Raise an error for HTTP issues
        data = response.json()

        if data:
            # Extract bounding box values (min lat, max lat, min lon, max lon)
            bounding_box = data[0]["boundingbox"]
            print(bounding_box)
            return bounding_box
        else:
            print("City not found in Nominatim API.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


"""# Fetch max latitude for Addis Ababa, Ethiopia
city = "Chengdu"
country = "China"
max_lat = get_max_latitude(city, country)

# if max_lat is not None:
print(f"Maximum latitude of the bounding box for {city}, {country}: {max_lat}")"""

if __name__ == "__main__":
    print(get_bounding_box("Pune", "India"))
