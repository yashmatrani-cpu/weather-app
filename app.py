import streamlit as st
import requests

st.set_page_config(page_title="Weather App", page_icon="🌤️", layout="centered")

st.title("🌤️ Yash's Weather App")
st.write("Kisi bhi city ka current weather check karein. (Built with Python & Streamlit)")

def fetch_weather(city):
    weather_codes = {
        0: "Clear sky ☀️", 1: "Mainly clear 🌤️", 2: "Partly cloudy ⛅", 3: "Cloudy ☁️",
        45: "Fog 🌫️", 51: "Light drizzle 🌦️", 61: "Rain 🌧️", 95: "Thunderstorm ⛈️"
    }
    
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    
    try:
        # TIMEOUT=10 add kiya hai taaki app hang na ho
        geo_response = requests.get(geo_url, timeout=10).json()

        if "results" not in geo_response:
            return {"error": "❌ City not found! Please check spelling."}

        lat = geo_response['results'][0]['latitude']
        lon = geo_response['results'][0]['longitude']

        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_response = requests.get(weather_url, timeout=10).json()

        temp = weather_response['current_weather']['temperature']
        windspeed = weather_response['current_weather']['windspeed']
        code = weather_response['current_weather']['weathercode']
        
        mausam = weather_codes.get(code, "Unknown")

        # RETURN BAHAR HAI
        return {
            "city": city.title(),
            "condition": mausam,
            "temp": temp,
            "wind": windspeed
        }
        
    except Exception as e:
        return {"error": f"⚠️ API Error: {e}"}

city_input = st.text_input("Enter City Name (e.g., Mumbai, Delhi, London):")

if st.button("Get Weather 🔍"):
    if city_input.strip() == "":
        st.warning("Please enter a city name.")
    else:
        with st.spinner(f"Fetching weather for {city_input}..."):
            result = fetch_weather(city_input)
            
            # Check karo ki error dictionary me hai ya nahi
            if "error" in result:
                st.error(result["error"])
            else:
                st.success(f"Weather in {result['city']}")
                col1, col2 = st.columns(2)
                col1.metric(label="Condition", value=result['condition'])
                col2.metric(label="Temperature (°C)", value=f"{result['temp']} °C")
                col3, col4 = st.columns(2)
                col3.metric(label="Wind Speed (km/h)", value=f"{result['wind']} km/h")