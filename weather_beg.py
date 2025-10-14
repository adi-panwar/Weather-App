import requests

api_key = "cf93c77b0562af9a26934aeed48fb095"  
base_url = "https://api.openweathermap.org/data/2.5/weather"

city = input("Enter city name: ")

params = {"q": city, "appid": api_key, "units": "metric"}
response = requests.get(base_url, params=params)

if response.status_code == 200:
    data = response.json()
    print(f"\nWeather in {city}:")
    print(f"Temperature: {data['main']['temp']}°C")
    print(f"Humidity: {data['main']['humidity']}%")
    print(f"Condition: {data['weather'][0]['description'].title()}")
else:
    print("City not found .")
