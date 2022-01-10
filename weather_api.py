import requests

api_key = "6988fcfff7b2d9b8879d1bc6e0e43467"
city_name = "seoul"

body = {}

weather_url = "http://api.openweathermap.org/data/2.5/weather?q=%s&units=metric&lang=kr&appid=%s" % (city_name, api_key)
forecast_url = "http://api.openweathermap.org/data/2.5/forecast?q=%s&units=metric&limit=1&lang=kr&appid=%s" % (city_name, api_key)

try:
    response = requests.get(weather_url)
    body["weather"] = response.json()
    print(response.json())

    print("=================================")
    response = requests.get(forecast_url)
    body["forecast"] = response.json()
    print(response.json())

except:
    print("Connnection error")

print(body)

text_response = "The weather in "+ body["forecast"]["city"]["name"] +" is "+ str(body["weather"]["main"]["temp"]) +\
                " ℃ and feels like "+ str(body["weather"]["main"]["feels_like"]+" ℃")
print(text_response)
