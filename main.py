try:
  import requests

  def fetch_weather(city):
   try: 
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
        return

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

    return f"""🌍 City: {city.title()}
☁️ Condition: {mausam}
🌡️ Temperature: {temp}°C
💨 Wind Speed: {windspeed} km/h"""
   except Exception as e:
       data = {
           'status':'Undefined',
           "error":"true",
           "message":f'{e}',
           "isDone":False
       }
       print(data)


  while True:
    print('\n-------Welcome To Weather Bot--------\n')
    print("\n=======Build by < YashDevelopers/>===========\n")
    a = input(f'''
          Menu:
           press:
             1 for determining weather of any city 
             2 for exit
''')

    if a=='1':
        city = input('enter city name(In India strictly):')
        city_c = city.capitalize()
        print(fetch_weather(city_c))
        continue
    elif a=='2':
        print('thanks for using.')
        break    
    else:
        print('invalid input')
except Exception as e2:
       data = {
              'status':'Undefined',
              "error":"true",
              "message":f'{e2}',
              "isDone":False
          }
       print(data)