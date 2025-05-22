import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
import re

def get_iss_passes(lat, lon):
    url = "https://heavens-above.com/PassSummary.aspx"
    params = {
        "satid": 25544,
        "lat": lat,
        "lng": lon,
        "alt": 0,
        "tz": "UCT"
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, params=params, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table")
    if not table:
        print("No table found in the page.")
        return []

    passes = []
    for row in table.find_all("tr")[1:]:
        cols = [td.get_text(strip=True) for td in row.find_all("td")]
        if len(cols) >= 10:
            try:
                date_str = cols[0]
                date = datetime.strptime(date_str, "%d %b").replace(year=datetime.now(timezone.utc).year).date()
            except ValueError:
                continue
            passes.append({
                "date": date,
                "magnitude": cols[1],
                "start_time": cols[2],
                "start_altitude": cols[3],
                "start_direction": cols[4],
                "highpoint_time": cols[5],
                "highpoint_altitude": cols[6],
                "highpoint_direction": cols[7],
                "end_time": cols[8],
                "end_altitude": cols[9],
                "end_direction": cols[10]

            })

    return passes

def get_weather_condition(lat, lon, dt):
    dt_hour = dt.replace(minute=0, second=0, microsecond=0)
    time_str = dt_hour.strftime("%Y-%m-%dT%H:%M")

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "weather_code",
        "start": time_str,
        "end": time_str,
        "timezone": "UTC",
        "forecast_days": 14
    }

    response = requests.get(url, params=params)
    data = response.json()

    times = data["hourly"]["time"]
    codes = data["hourly"]["weather_code"]

    if time_str in times:
        index = times.index(time_str)
        weather_code = codes[index]
    else:
        return "Unknown"

    weather_conditions = {
        0: "Clear",
        1: "Mainly Clear",
        2: "Partly Cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing Rime Fog",
        51: "Light Drizzle",
        53: "Moderate Drizzle",
        55: "Dense Drizzle",
        56: "Light Freezing Drizzle",
        57: "Dense Freezing Drizzle",
        61: "Slight Rain",
        63: "Moderate Rain",
        65: "Heavy Rain",
        66: "Light Freezing Rain",
        67: "Heavy Freezing Rain",
        71: "Slight Snow Fall",
        73: "Moderate Snow Fall",
        75: "Heavy Snow Fall",
        77: "Snow Grains",
        80: "Slight Rain Showers",
        81: "Moderate Rain Showers",
        82: "Violent Rain Showers",
        85: "Slight Snow Showers",
        86: "Heavy Snow Showers",
        95: "Thunderstorm",
        96: "Thunderstorm with Slight Hail",
        99: "Thunderstorm with Heavy Hail"
    }

    return weather_conditions.get(weather_code, "Unknown")

def get_coordinates():
    coord_pattern = re.compile(r'^-?(90(\.0+)?|[1-8]?\d(\.\d+)?)$')
    long_pattern = re.compile(r'^-?(180(\.0+)?|(1[0-7]\d|[1-9]?\d)(\.\d+)?)$')

    while True:
        lat_input = input("Enter latitude (e.g. 40.7128 or -33.8688): ").strip()
        if not coord_pattern.match(lat_input):
            print("Invalid latitude format. Please enter a number between -90 and 90.")
            continue

        lon_input = input("Enter longitude (e.g. -74.0060 or 151.2093): ").strip()
        if not long_pattern.match(lon_input):
            print("Invalid longitude format. Please enter a number between -180 and 180.")
            continue

        latitude = float(lat_input)
        longitude = float(lon_input)
        return latitude, longitude



escape = False
while escape == False:
    coordquestion = input("do you wish to provide custom coordinates (y/n)?")
    if coordquestion == "y":
        latitude, longitude = get_coordinates()
        escape = True
    elif coordquestion == "n":
        print("using coordinates from connection IP adress")
        ip_info = requests.get("http://ip-api.com/json/").json()
        latitude = ip_info.get("lat", 0.0000)
        longitude = ip_info.get("lon", 0.0000)
        print(latitude)
        print(longitude)
        escape = True

iss_passes = get_iss_passes(latitude, longitude)
if not iss_passes:
    print("No visible ISS passes found within the next 10 days.")
else:
    print("Possible ISS sightings in the next 10 days")
    for p in iss_passes:
        timelist = (p['start_time']).split(":")
        condition = get_weather_condition(latitude, longitude, datetime((p['date']).year, (p['date']).month, (p['date']).day, int(timelist[0]), int(timelist[1]), tzinfo=timezone.utc))
        print(f"{p['date']}: appears {p['start_time']} at {p['start_direction']} {p['start_altitude']}  → disappears {p['end_time']} at {p['end_direction']} {p['end_altitude']} | Mag {p['magnitude']} | Conditions: {condition} ")
