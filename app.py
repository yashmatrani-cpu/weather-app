import streamlit as st
import requests

# Page ka basic setup
st.set_page_config(page_title="Weather App", page_icon="🌤️", layout="centered")

# Title aur Header
st.title("🌤️ Yash's Weather App")
st.write("Kisi bhi city ka current weather check karein. (Built with Python & Streamlit)")



def fetch_weather(city):

    weather_codes = {
    0: "Clear sky ☀️",
    1: "Mainly clear 🌤️",
    2: "Partly cloudy ⛅",
    3: "Cloudy ☁️",
    45: "Fog 🌫️",
    51: "Light drizzle 🌦️",
    61: "Rain 🌧️",
    95: "Thunderstorm ⛈️"
}
    keys = weather_codes.keys()
    print(f"fetching the weather of city {city}")
    """Fetching longitude and lattitudes of city"""
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"

    geo_response = requests.get(geo_url).json()

    if "results" not in geo_response:
        print('city not found')
      
    geo_lat = geo_response['results'][0]['latitude']  
    geo_lon = geo_response['results'][0]["longitude"] 
    ##geo_response mai se 0th index nikaalo usme se lattitude key nikaalo kyuki result 


    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={geo_lat}&longitude={geo_lon}&current_weather=true"

    weather_response = requests.get(weather_url).json()

    temp = weather_response['current_weather']['temperature']
    windspeed = weather_response['current_weather']['windspeed']
    code = weather_response['current_weather']['weathercode']
    if code in keys:
        mausam =  (weather_codes[code])
    else:
        mausam = "weather code can't determinded"    

    return {
            "city": city.title(),
            "condition": mausam,
            "temp": temp,
            "wind": windspeed
        }



  

city_input = st.text_input("Enter City Name (e.g., Mumbai, Delhi, London):")

if st.button("Get Weather 🔍"):
    if city_input.strip() == "":
        st.warning("Please enter a city name.")
    else:
        with st.spinner(f"Fetching weather for {city_input}..."):
            result = fetch_weather(city_input)
            
            if "error" in result:
                st.error(result["error"])
            else:
                
                st.success(f"Weather in {result['city']}")
                
                col1, col2 = st.columns(2)
                col1.metric(label="Condition", value=result['condition'])
                col2.metric(label="Temperature (°C)", value=f"{result['temp']} °C")
                
                col3, col4 = st.columns(2)
                col3.metric(label="Wind Speed (km/h)", value=f"{result['wind']} km/h")